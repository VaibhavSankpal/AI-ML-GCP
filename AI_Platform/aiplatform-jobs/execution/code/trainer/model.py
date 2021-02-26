import os
import numpy as np
import pandas as pd
import sys
import json
import logging
import joblib
from google.cloud import bigquery
from trainer.helper import gcshelper, bqhelper

predictiontable = 'prd-65343-datalake-bd-88394358.modelmgmt_65343_ds.census_pred_results'

# Specify default parameters.
BUCKET_NAME = None
OUTPUT_DIR = None
LOCAL_PATH = '/tmp'

def run():
    # Download the model from GCS bucket
    gcshelper.download_from_bucket(BUCKET_NAME, OUTPUT_DIR, LOCAL_PATH)
    
    # load model
    model = joblib.load(LOCAL_PATH + '/model.joblib')
    logging.info("Model loaded from bucket")
    
    # load the input data from bigquery
    df = bqhelper.read_from_bqtable('SELECT age, workclass, functional_weight, education, education_num, marital_status, occupation, relationship, race, sex, capital_gain, capital_loss, hours_per_week, native_country FROM `prd-65343-datalake-bd-88394358.modelmgmt_65343_ds.census_test_data`')
    logging.info("Batch data loaded from Bigquery to dataframe")
    
    # PREDICT your model
    preds = model.predict(df)
    logging.info("Batch prediction completed")
    
    # add result column
    df['prediction_result'] = preds
    
    # create a schema for the output BQ table
    # Note: This is an optional argument. Use this only if you want to pass your own schema and add this variable as an argument to below function.
    varbqschema=[
        bigquery.SchemaField(name="age", field_type="INTEGER"),
        bigquery.SchemaField(name="workclass", field_type="STRING"),
        bigquery.SchemaField(name="functional_weight", field_type="INTEGER"),
        bigquery.SchemaField(name="education", field_type="STRING"),
        bigquery.SchemaField(name="education_num", field_type="INTEGER"),
        bigquery.SchemaField(name="marital_status", field_type="STRING"),
        bigquery.SchemaField(name="occupation", field_type="STRING"),
        bigquery.SchemaField(name="relationship", field_type="STRING"),
        bigquery.SchemaField(name="race", field_type="STRING"),
        bigquery.SchemaField(name="sex", field_type="STRING"),
        bigquery.SchemaField(name="capital_gain", field_type="INTEGER"),
        bigquery.SchemaField(name="capital_loss", field_type="INTEGER"),
        bigquery.SchemaField(name="hours_per_week", field_type="INTEGER"),
        bigquery.SchemaField(name="native_country", field_type="STRING"),
        bigquery.SchemaField(name="prediction_result", field_type="BOOLEAN")
    ]
    #write the results and the input data to a new BQ table
    bqhelper.write_to_bqtable(df, predictiontable)
    logging.info("Prediction results stored into Bigquery successfully")
