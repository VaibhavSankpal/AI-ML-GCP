import base64
import logging as log
import json
import io
import re
import pandas
from google.cloud import bigquery, storage
from google.cloud.exceptions import NotFound
from pathlib import Path
import os

def download_blob(bucket_name, blob_path, local_path):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    # Construct a client side representation of a blob.
    blob = bucket.blob(blob_path)
    blob.download_to_filename(local_path)
    log.info("Blob {} downloaded to {}.".format(blob_path, local_path))

def rename_file(bucket_name, file_name, new_blob_name):
    """Rename file in GCP bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name) 
    blob = bucket.blob(file_name)
    bucket.rename_blob(blob, new_name=new_blob_name)
    return f'{file_name} renamed to {new_blob_name}.'

def get_bq_schema(bucket_name, file_name, path_file_name):
    local_path = '/tmp/'+file_name
    log.debug('Local path: {}'.format(local_path))
    
    # Download the file in temp location
    download_blob(bucket_name, path_file_name, local_path)
    
    # read file with single row
    df = pandas.read_csv(local_path, nrows=1)
    
    # replace special characters and make column names lower
    df.rename(columns=lambda x:re.sub('\\_+', '_', re.sub('\\W+', '_', x)).lower(), inplace= True)
    # deduplicate the same column names with _1, _2 etc
    cols=pandas.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [dup + '_' + str(i) if i != 0 else dup for i in range(sum(cols == dup))]
    df.columns=cols

    # Working with column fields and generating a bq_schema
    bq_schema = []
    for x in df.columns.to_list(): bq_schema.append({"name":x,"type":"string"})
    return bq_schema
    
def entry_point(request):
    log.info(('Extracting information from request {}').format(request))
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        event = request.get_json(silent=True)
    elif content_type == 'application/octet-stream':
        event = request.data
    elif content_type == 'text/plain':
        event = request.data
    elif content_type == 'application/x-www-form-urlencoded':
        event = request.form.get('name')
    else:
        raise ValueError("Unknown content type: {}".format(content_type))

    log.info('CONTENT_TYPE {}'.format(content_type))
    log.info('REQUEST {}'.format(event))

    try:
        bucket_name = event['message']['attributes']['bucketId']
        file_name = event['message']['attributes']['objectId']
        log.info("Attributes are: BUCKET NAME {} -- FILE NAME {}".format(bucket_name, file_name))

        # Do not process any file uploaded at any level in the bucket
        if(len(file_name.split('/')) <= 2):
            log.info("Invalid path for processing - It should be <bucketname>/dataset/datasource/fileXYZ.csv !!")
            return "Invalid path for processing - It should be <bucketname>/dataset/datasource/fileXYZ.csv !!"

        # Check if the object is from the archived location, if yes, DO NOT PROCESS
        if(file_name.split('/')[-2] == 'archive'):
            log.info("Archive File - Not Processed !!")
            return "Archive File - Not Processed !!"
        
        if file_name.endswith('.csv'):
            project_id= os.environ.get("BQ_PROJECT_ID")
            dataset_name=os.environ.get("BQ_DATASET_NM")
            
            blob_path=file_name
            path_file_name = file_name
            file_name = file_name[file_name.rfind('/')+1:]
            log.info('Processing file: {}'.format(file_name))
            log.info('Processing path file: {}'.format(path_file_name))
            
            bq_schema=get_bq_schema(bucket_name, file_name, path_file_name)

            # Check if files can be appended together in one table
            if "_part_" in file_name:
                table_name = file_name.rsplit('_',2)[0]
                table_id = "{}.{}.{}".format(project_id, dataset_name, table_name)
                log.info("Table name is {}".format(table_id))
            else:
                table_name = Path(file_name).stem
                table_id = "{}.{}.{}".format(project_id, dataset_name, table_name)
                log.info("Table name is {}".format(table_id))
            
            # listing table names
            # Construct a BigQuery client object
            data_file = 'gs://{}/{}'.format(bucket_name, path_file_name)
            client = bigquery.Client(project=project_id, location = 'US')
            dataset_ref = client.get_dataset(dataset_name)
            table_ref = dataset_ref.table(table_name)
            log.info('Data file path: {}'.format(data_file))
            log.info('Table reference is: {}'.format(table_ref))

            try:
                client.get_table(table_id)  # Make an API request
                log.info("Table {} already exists.".format(table_id))
            except NotFound:
                log.info("Table {} is not found.".format(table_id))

            job_config = bigquery.LoadJobConfig()          
            job_config.schema = bq_schema
            job_config.source_format = bigquery.SourceFormat.CSV
            job_config.skip_leading_rows = 1
            job_config.field_delimiter = ','
            job_config.create_disposition = 'CREATE_IF_NEEDED'
            job_config.write_disposition = 'WRITE_APPEND'
            load_job = client.load_table_from_uri(data_file, table_ref, job_config=job_config)
            log.info('The job ID for BQ load is {}'.format(load_job.job_id))
            
            # Wait for job to finish
            load_job.result()
            
            # Validate the destination table and row counts
            destination_table = client.get_table(table_ref)  # Make an API request.
            log.info("Loaded {} rows.".format(destination_table.num_rows))
            
            # Move the file to archive
            new_blob_name = path_file_name[0:path_file_name.rfind('/')+1] + 'archive/' + file_name
            rename_file(bucket_name, path_file_name, new_blob_name)       
            log.info('SUCECSSFULLY COMPLETED !!!')

        else:
            log.info('The file is not in CSV format! Please use Comma Seperated Value file to load the data into BigQuery.')
            
    except Exception as e:
        log.error(e.message)
        pass