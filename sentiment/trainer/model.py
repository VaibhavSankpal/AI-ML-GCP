import datetime
import sys
import pandas as pd
import numpy as np
import json
import logging
from helper import gcshelper, bqhelper
from google.cloud import bigquery

varinputbqtable = None
varoutputbqtable = None
varmodelgcsbucketname = None
varmodelgcsbucketpath = None
varlocalpath = '/tmp'

def run():
    start = datetime.datetime.now()
    logging.info("Start: " + str(start))

    startdownload = datetime.datetime.now()
    gcshelper.download_from_bucket(varmodelgcsbucketname, varmodelgcsbucketpath, varlocalpath)
    enddownload = datetime.datetime.now()
    logging.info("Time to download the model: " + str(enddownload-startdownload))

    startimport = datetime.datetime.now()
    from sentiment import sentiment
    endimport = datetime.datetime.now()
    logging.info("Time to import custom sentiment library: " + str(endimport-startimport))

    startload = datetime.datetime.now()
    objsentiment = sentiment.isentiment_pred()
    endload = datetime.datetime.now()
    logging.info("Time to load sentiment model in memory for execution: " + str(endload-startload))

    startreaddata = datetime.datetime.now()
    dfsurvey = bqhelper.read_from_bqtable('sb-bigdata-4985-da852265', 'SELECT SentimentText FROM `sb-bigdata-4985-da852265.modelmanagement.insentiment` limit 100')
    endreaddata = datetime.datetime.now()
    logging.info("Time to read the big query table: " + str(endreaddata-startreaddata))

    cnt = 0
    objresult = []
    objposscore = []
    objnegscore = []
    objneuscore = []

    for row in dfsurvey.itertuples():
        obj = {"tweetContent": row.SentimentText, "result": "error", "negscore": str(0.0), "neuscore": str(0.0), "posscore": str(0.0)}
        objmodelresult = json.dumps(obj)
        
        try:
            objmodelresult = objsentiment.predict(str(row.SentimentText))
        except:
            logging.info("Error : " + row.SentimentText)
        objparsedresult = json.loads(objmodelresult)
        objresult.append(objparsedresult['result'])
        objposscore.append(objparsedresult['posscore'])
        objneuscore.append(objparsedresult['neuscore'])
        objnegscore.append(objparsedresult['negscore'])
        cnt = cnt + 1
        if cnt%1000==0:
            logging.info(cnt)

    logging.info("Number of calls made to Sentiment Model: " + str(cnt))

    dfsurvey['capresult'] = objresult
    dfsurvey['capnegscore'] = objnegscore
    dfsurvey['capposscore'] = objposscore
    dfsurvey['capneuscore'] = objneuscore

    logging.info("Length of output dataset: " + str(len(dfsurvey)))
    logging.info("Interim timestamp before writing output to bq: " + str(datetime.datetime.now()))

    varbqschema=[
        bigquery.SchemaField(name="SentimentText", field_type="STRING"),
        bigquery.SchemaField(name="capresult", field_type="STRING"),
        bigquery.SchemaField(name="capnegscore", field_type="STRING"),
        bigquery.SchemaField(name="capposscore", field_type="STRING"),
        bigquery.SchemaField(name="capneuscore", field_type="STRING")
    ]

    bqhelper.write_to_bqtable('sb-bigdata-4985-da852265', varoutputbqtable, varbqschema, dfsurvey)
    logging.info("timestamp after writing output to bq: " + str(datetime.datetime.now()))

    end = datetime.datetime.now()
    logging.info("End: " + str(end))
    logging.info("Total execution time: " + str(end-start))