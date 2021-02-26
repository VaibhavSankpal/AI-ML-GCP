import os
import logging
from google.cloud import storage
import warnings

# Filter the warnings related to cloud SDK authentication
warnings.filterwarnings("ignore")

# create logger
logger = logging.getLogger(__name__)

def upload_to_bucket_sdk(local_path, bucket_name, blob_path):
    """
    This function will upload a BLOB to GCS bucket. Use this function in Python SDK which would use a USER account to authenticate for GCS service usage.
    
    Parameters:
    bucket_name: name of the destination bucket
    blob_path: path within the bucket where the object will get uploaded
    local_path: source path such as local directory where the object is available for upload
    
    Returns: 
    blob.public_url: the destination location of the uploaded object
    """
    bucket = storage.Client().bucket(bucket_name)
    blob = bucket.blob(blob_path)
    blob.upload_from_filename(local_path)
    logger.info('Blob {} uploaded to {}.'.format(local_path, blob_path))
    return blob.public_url

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

def download_from_bucket_sdk(bucket_name, blob_path, local_path):
    """
    This function will download a BLOB from GCS bucket. Use this function in Python SDK which would use a USER account to authenticate for GCS service usage.
    Parameters: 
    bucket_name: name of the source bucket
    blob_path: path within the bucket where the object is available for download
    local_path: destination path such as local directory where the object will be downloaded
    
    Returns: 
    Blob downloaded to the destination directory.
    """
    # Create this folder locally
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    logging.info(bucket)
    blobs=list(bucket.list_blobs(prefix=blob_path))
    logging.info(blobs)

    startloc = 0 
    for blob in blobs:
        startloc = 0
        folderloc = findOccurrences(blob.name.replace(blob_path, ''), '/') 
        #print folderloc
        logging.info(blob.name.replace(blob_path, ''))
        if(not blob.name.endswith("/")):
            #print( blob.name.replace(blob_path, ''))
            if(blob.name.replace(blob_path, '').find("/") == -1):
                downloadpath=local_path + '/' + blob.name.replace(blob_path, '')
                #print downloadpath
                logging.info(downloadpath)
                blob.download_to_filename(downloadpath)
            else:
                for folder in folderloc:
                    
                    if not os.path.exists(local_path + '/' + blob.name.replace(blob_path, '')[startloc:folder]):
                        create_folder=local_path + '/' +blob.name.replace(blob_path, '')[0:startloc]+ '/' +blob.name.replace(blob_path, '')[startloc:folder]
                        startloc = folder + 1
                        os.makedirs(create_folder)
                        #print ('Folder Created : ' + create_folder)
                        logging.info('Folder Created : ' + create_folder)
                    
                downloadpath=local_path + '/' + blob.name.replace(blob_path, '')
                logging.info(downloadpath)

                blob.download_to_filename(downloadpath)
                logging.info(blob.name.replace(blob_path, '')[0:blob.name.replace(blob_path, '').find("/")])

    logger.info('Blob {} downloaded to {}.'.format(blob_path, local_path))
    
def upload_to_bucket(local_path, bucket_name, blob_path):
    """
    This function will upload a BLOB to GCS bucket. Use this function while using Notebook service account to authenticate for GCS service usage.
    
    Parameters: 
    bucket_name: name of the destination bucket
    blob_path: path within the bucket where the object will get uploaded
    local_path: source path such as local directory where the object is available for upload
    
    Returns: 
    blob.public_url: the destination location of the uploaded object
    """
    command = "gsutil cp -r {localpath} gs://{bucketname}/{blobpath}".format(localpath = local_path, bucketname = bucket_name, blobpath = blob_path)
    print(command)
    os.system(command)
    logger.info('Blob {} uploaded to {}.'.format(local_path, blob_path))
    return None
def download_from_bucket(bucket_name, blob_path, local_path):
    """
    This function will download a BLOB from a GCS bucket. Use this function while using Notebook service account to authenticate for GCS service usage.
    Parameters: 
    bucket_name: name of the source bucket
    blob_path: path within the bucket where the object is available for download
    local_path: destination path such as local directory where the object will be downloaded
    
    Returns: 
    Blob downloaded to the destination directory.
    """
    command = "gsutil cp -r gs://{bucketname}/{blobpath} {localpath}".format(bucketname = bucket_name, blobpath = blob_path, localpath = local_path)
    print(command)
    os.system(command)
    logger.info('Blob {} downloaded to {}.'.format(blob_path, local_path))
    return None