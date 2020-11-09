import os
import logging
from google.cloud import storage

def upload_to_bucket(bucket_name, blob_path, local_path):
    bucket = storage.Client().bucket(bucket_name)
    blob = bucket.blob(blob_path)
    blob.upload_from_filename(local_path)
    return blob.public_url

def download_from_bucket(bucket_name, blob_path, local_path):    
    # Create this folder locally
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    logging.info(bucket)
    blobs=list(bucket.list_blobs(prefix=blob_path))
    logging.info(blobs)
    
    for blob in blobs:
        logging.info(blob.name.replace(blob_path, ''))
        if(not blob.name.endswith("/")):
            if(blob.name.replace(blob_path, '').find("/") == -1):
                blob.download_to_filename(local_path + '/' + blob.name.replace(blob_path, ''))
            else:
                if not os.path.exists(local_path + '/' + blob.name.replace(blob_path, '')[0:blob.name.replace(blob_path, '').find("/")]):
                    create_folder=local_path + '/' + blob.name.replace(blob_path, '')[0:blob.name.replace(blob_path, '').find("/")]
                    os.makedirs(create_folder)
                    logging.info('Folder Created : ' + create_folder)
                blob.download_to_filename(local_path + '/' + blob.name.replace(blob_path, ''))
                logging.info(blob.name.replace(blob_path, '')[0:blob.name.replace(blob_path, '').find("/")])

    logging.info('Blob {} downloaded to {}.'.format(blob_path, local_path))