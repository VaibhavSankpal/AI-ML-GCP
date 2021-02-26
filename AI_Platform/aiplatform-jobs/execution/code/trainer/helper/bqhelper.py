import os
import logging
from google.cloud import bigquery
import warnings

# Filter the warnings related to cloud SDK authentication
warnings.filterwarnings("ignore")

# create logger
logger = logging.getLogger(__name__)

def read_from_bqtable(bq_query):
    """
    This function will read the data from a BQ table
    
    Parameters: 
    bq_query: BigQuery query to be executed
    
    Returns: 
    bq_data: Pandas dataframe for bigquery table
    """
    client = bigquery.Client()
    bq_data = client.query(bq_query).to_dataframe()
    logger.info('data read from BQ table')
    return bq_data

def write_to_bqtable(datadf, bq_tablename, disposition_type = 'WRITE_APPEND', bq_schemaname = False):
    """
    This function will write the data to a BQ table. Table columns Fields must contain only letters, numbers, and underscores, start with a letter or underscore, and be at most 128 characters long.
    
    Parameters: 
    bq_query: BigQuery query to be executed
    
    Returns: 
    bq_data: Pandas dataframe for bigquery table
    """
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = disposition_type
    if bq_schemaname:
        job_config.schema = bq_schemaname   # require manual schema definition
    else:
        job_config.autodetect = True        # to auto-detect the schema
        
    job = client.load_table_from_dataframe(datadf, bq_tablename, job_config=job_config)
    logger.info('data loaded into BQ table')
    
    # Wait for the load job to complete.
    job.result()