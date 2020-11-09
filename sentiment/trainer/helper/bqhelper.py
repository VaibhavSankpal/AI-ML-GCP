import os
import logging
from google.cloud import bigquery

def read_from_bqtable(bq_projectname, bq_query):
    client = bigquery.Client(bq_projectname)
    bq_data = client.query(bq_query).to_dataframe()
    return bq_data

def write_to_bqtable(bq_projectname, bq_tablename, bq_schemaname, datadf):
    client = bigquery.Client(bq_projectname)
    # Since string columns use the "object" dtype, pass in a (partial) schema
    # to ensure the correct BigQuery data type.
    job_config = bigquery.LoadJobConfig()
    job_config.schema = bq_schemaname
    
    job = client.load_table_from_dataframe(datadf, bq_tablename, job_config=job_config)
    # Wait for the load job to complete.
    job.result()