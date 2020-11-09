from __future__ import absolute_import
import json
import numpy
import os
import sys
import logging
import csv
import time
import datetime
import threading
from runner import download

import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import storage
from sklearn.externals import joblib

LOGGER = logging.getLogger(__name__)

# Specify default parameters.
# As a best practice, pass the required and optional parameters while executing your Dataflow job
PUBSUB_TOPIC = 'projects/<PROJECT-NAME>/topics/<TOPIC-NAME>'
BQ_DATASET = '<DATASET-NAME>'
BQ_TABLE = BQ_DATASET + '.<TABLE_NAME>'

MODEL_BUCKET = '<BUCKET-NAME>'
MODEL_PATH = '<PATH-TO-MODEL>'
LOCAL_PATH = '/tmp'

class model_predict:
    objmodel = None
    model = None
    
    @staticmethod
    def getInstance():
        # Static access method.
        if model_predict.objmodel == None:
            LOGGER.info('Downloading the models to ' + LOCAL_PATH)
            download.download_blob(MODEL_BUCKET, MODEL_PATH, LOCAL_PATH)
            model_predict()
        return model_predict.objmodel

    def __init__(self):
        if model_predict.objmodel != None:
            raise Exception('This class is singleton!')
        else:
            ###### initialization
            self.model = self.load_models()
            model_predict.objmodel=self

    def load_models(self):           
        # load model (please specify your custom model-name)
        LOGGER.info('Loading model.joblib')
        model = joblib.load(LOCAL_PATH + '/model.joblib')
        LOGGER.info('load_model completed model.joblib')
        return model


    def predict(self, string):
        obj = {}
        pred = self.model.predict(string)
        obj = {"data": string, "result": str(pred[0])}
        jsonstr = json.dumps(obj)
        return jsonstr

class Prediction(beam.DoFn):

    def process(self, element, *args, **kwargs):
        objmodel = model_predict.getInstance()
        objmodelresult = objmodel.predict([element['data'].split(",")])
        objparsedresult = json.loads(objmodelresult)
        out = [{'data':element['data'],'result':objparsedresult['result'],'publishtime':element['timestamp'],'processedtime':str(datetime.datetime.now())}]
        return out

def format_message(message, timestamp=beam.DoFn.TimestampParam):    
    LOGGER.info(message)
    formatted_message = {
        'data': message,
        'attributes': str(message),
        'timestamp': str(datetime.datetime.now())
    }
    return formatted_message

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_topic', dest='input_topic', required=False,
        help='Input PubSub topic of the form "/topics/<PROJECT>/<TOPIC>".',
        default=PUBSUB_TOPIC)

    parser.add_argument('--bq_table', dest='output', required=False,
                        help='Output BQ table to write results to.',
                        default=BQ_TABLE)

    # Parse arguments from the command line.
    known_args, pipeline_args = parser.parse_known_args(argv)

    p = beam.Pipeline(options=PipelineOptions(pipeline_args))

    (p
     | 'Read data as a stream of messages' >> beam.io.ReadFromPubSub(known_args.input_topic)
     | 'Format input message with timestamp' >> beam.Map(format_message)
     | 'Perform model prediction' >> beam.ParDo(Prediction())
     | 'Write output to BigQuery' >> beam.io.gcp.bigquery.WriteToBigQuery(
         known_args.output,
         schema='data:STRING,result:STRING,publishtime:TIMESTAMP,processedtime:TIMESTAMP',
         create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
         write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
         batch_size=500)
    )
    p.run()

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()