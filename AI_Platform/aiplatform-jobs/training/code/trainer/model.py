#!/usr/bin/env python
import datetime
import pandas as pd
from google.cloud import storage
from google.cloud import bigquery
from trainer.helper import gcshelper, bqhelper
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelBinarizer
import json
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import logging

# TODO: REPLACE 'YOUR_BUCKET_NAME' with your GCS Bucket name. 
OUTPUT_DIR = None
BUCKET_NAME = None

# Construct a BigQuery client object.
client = bigquery.Client()

def train_and_evaluate(args):
    
    # ---------------------------------------
    # 1. Add code to download the data from GCS (in this case, using the publicly hosted data).
    # AI Platform will then be able to use the data when training your model.
    # ---------------------------------------
    
    # [START download-data] ---------------------------------------
#     Public bucket holding the census data
#     bucket = storage.Client().bucket('cloud-samples-data')
    
#     # Path to the data inside the public bucket
#     blob = bucket.blob('ml-engine/sklearn/census_data/adult.data')
#     # Download the data
#     blob.download_to_filename('adult.data')

#     QUERY = ('SELECT * FROM `sb-bigdata-4985-da852265.modelmanagement.composer_census_data`')
#     query_job = client.query(QUERY)  # API request
#     df = query_job.result().to_dataframe()  # Waits for query to finish

    df = bqhelper.read_from_bqtable('prd-65343-modelmgmt-d-607e8a85', 'SELECT age, workclass, functional_weight, education, education_num, marital_status, occupation, relationship, race, sex, capital_gain, capital_loss, hours_per_week, native_country, income_bracket FROM `prd-65343-datalake-bd-88394358.65343_modelmgmt_ds.census_adult_data`')
    logging.info("data loaded from bigquery!")

    # [END download-data] ---------------------------------------

    # Create and run a BigQuery query
    # wppdata_query = bq.Query('SELECT * FROM `<projectname>.<datasetname>.<tablename>`')
    # output_options = bq.QueryOutput.table(use_cache=True)
    # result = wppdata_query.execute(output_options=output_options).result()
    # df = result.to_dataframe()

    # ---------------------------------------
    # This is where your model code would go. Below is an example model using the census dataset.
    # ---------------------------------------
    # [START define-and-load-data]
    # Define the variable column names
    DEPENDENTVARIABLE = 'income_bracket'

    # Define the format of your input data including unused columns (These are the columns from the census data files)
    ALL_COLUMNS = (
        'age',
        'workclass',
        'fnlwgt',
        'education',
        'education-num',
        'marital-status',
        'occupation',
        'relationship',
        'race',
        'sex',
        'capital-gain',
        'capital-loss',
        'hours-per-week',
        'native-country',
        'income_bracket'
    )
    
    # Categorical columns are columns that need to be turned into a numerical value to be used by scikit-learn
    CATEGORICAL_COLUMNS = (
        'workclass',
        'education',
        'marital-status',
        'occupation',
        'relationship',
        'race',
        'sex',
        'native-country'
    )

#     # Load the training census dataset
#     with open('./composer_census_data', 'r') as train_data:
#         raw_training_data = pd.read_csv(train_data, header=None, names=ALL_COLUMNS)

    # Remove the column we are trying to predict ('income-level') from our features list
    # Convert the Dataframe to a lists of lists
    train_features = df.drop(DEPENDENTVARIABLE, axis=1).values.tolist()

    # Create our training labels list, convert the Dataframe to a lists of lists
    train_labels = (df[DEPENDENTVARIABLE] == ' >50K').values.tolist()
    # [END define-and-load-data]


    # [START categorical-feature-conversion]
    # Since the census data set has categorical features, we need to convert
    # them to numerical values. We'll use a list of pipelines to convert each
    # categorical column and then use FeatureUnion to combine them before calling
    # the RandomForestClassifier.
    categorical_pipelines = []

    # Each categorical column needs to be extracted individually and converted to a numerical value.
    # To do this, each categorical column will use a pipeline that extracts one feature column via
    # SelectKBest(k=1) and a LabelBinarizer() to convert the categorical value to a numerical one.
    # A scores array (created below) will select and extract the feature column. The scores array is
    # created by iterating over the COLUMNS and checking if it is a CATEGORICAL_COLUMN.
    for i, col in enumerate(ALL_COLUMNS[:-1]):
        if col in CATEGORICAL_COLUMNS:
            # Create a scores array to get the individual categorical column.
            # Example:
            #  data = [39, 'State-gov', 77516, 'Bachelors', 13, 'Never-married', 'Adm-clerical', 
            #         'Not-in-family', 'White', 'Male', 2174, 0, 40, 'United-States']
            #  scores = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            # Returns: [['State-gov']]      
            # Build the scores array.
            scores = [0] * len(ALL_COLUMNS[:-1]) 
            # This column is the categorical column we want to extract.
            scores[i] = 1  
            skb = SelectKBest(k=1)
            skb.scores_ = scores
            # Convert the categorical column to a numerical value
            lbn = LabelBinarizer()
            r = skb.transform(train_features)
            lbn.fit(r)
            # Create the pipeline to extract the categorical feature
            categorical_pipelines.append(
                ('categorical-{}'.format(i), Pipeline([
                    ('SKB-{}'.format(i), skb),
                    ('LBN-{}'.format(i), lbn)])))
    # [END categorical-feature-conversion]

    # [START create-pipeline]
    # Create pipeline to extract the numerical features
    skb = SelectKBest(k=6)
    # From COLUMNS use the features that are numerical
    skb.scores_ = [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0]
    categorical_pipelines.append(('numerical', skb))

    # Combine all the features using FeatureUnion
    preprocess = FeatureUnion(categorical_pipelines)

    # Create the classifier
    classifier = RandomForestClassifier()

    # Transform the features and fit them to the classifier
    classifier.fit(preprocess.transform(train_features), train_labels)

    # Create the overall model as a single pipeline
    pipeline = Pipeline([
        ('union', preprocess),
        ('classifier', classifier)
    ])
    logging.info("Training completed successfully!")
    # [END create-pipeline]

    # ---------------------------------------
    # 2. Export and save the model to GCS
    # ---------------------------------------
    # [START export-to-gcs]
    # Export the model to a file
    print(" bucket name : ", args.model_bucket)
    print(" output dir : ", args.output_dir)
    model = 'model.joblib'
    joblib.dump(pipeline, model)

    # Upload the model to GCS
    model_url = upload_to_bucket(BUCKET_NAME,'{}/{}'.format(OUTPUT_DIR,model), model)
    logging.info("model uploaded to GCS bucket!")
    
def upload_to_bucket(bucket_name, blob_path, local_path):
    bucket = storage.Client().bucket(bucket_name)
    blob = bucket.blob(blob_path)
    blob.upload_from_filename(local_path)
    return blob.public_url