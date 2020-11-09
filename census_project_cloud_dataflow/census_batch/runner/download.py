import os
import logging
from google.cloud import storage

LOGGER = logging.getLogger(__name__)

def download_blob(bucket_name, source_path, destination_path):    
    # Create this folder locally
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    LOGGER.info(bucket)
    blobs=list(bucket.list_blobs(prefix=source_path))
    LOGGER.info(blobs)
    
    for blob in blobs:
        LOGGER.info(blob.name.replace(source_path, ''))
        if(not blob.name.endswith("/")):
            if(blob.name.replace(source_path, '').find("/") == -1):
                blob.download_to_filename(destination_path + '/' + blob.name.replace(source_path, ''))
            else:
                if not os.path.exists(destination_path + '/' + blob.name.replace(source_path, '')[0:blob.name.replace(source_path, '').find("/")]):
                    os.makedirs(destination_path + '/' + blob.name.replace(source_path, '')[0:blob.name.replace(source_path, '').find("/")])
                blob.download_to_filename(destination_path + '/' + blob.name.replace(source_path, ''))
                LOGGER.info(blob.name.replace(source_path, '')[0:blob.name.replace(source_path, '').find("/")])

    LOGGER.info('Blob {} downloaded to {}.'.format(source_path,destination_path))