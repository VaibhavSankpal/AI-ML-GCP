import json
import numpy
import os
import sys
import logging
import csv
import time
import datetime
import threading
import ConfigParser
from keras.models import *
import tensorflow as tf

from data_helper import *
from embedding import Embedding
from cnn import eval, parseArg

DESCRIPTION = ""
EPILOG = ""

class isentiment_pred:
    fn_embedding = ""
    fn_out = ""
    max_nb_words = ""
    stopwords_path = ""
    max_sequence_length = 50
    embed_dim = 300
    params = ""

    def __init__(self):
        ###### initialization
        self.fn_embedding, self.fn_out, self.max_nb_words, self.stopwords_path = parseArg()
        self.params = self.load_params()

    def load_params(self):
        # load embedding
        o_emb = Embedding("filter", self.fn_embedding, "", self.max_nb_words)
        o_emb.load()
        name = self.fn_out
        if not self.fn_out.endswith(".dtm"):
            name = os.path.split(os.path.splitext(self.fn_out)[0])[1] +".dtm"
        fn_model = os.path.join(name, "model.h5")
        fn_le = os.path.join(name, "le.pp")
        model = load_model(fn_model)
        graph = tf.get_default_graph()
        objle = pickle_file(fn_le)

        stpwrd = loadStopwords(self.stopwords_path)
        params = (o_emb, model, stpwrd, objle, graph)
        logging.info('Done initialization, ready to work.')

        return params

    def predict(self, string):
        obj = {}
        pred = eval(self.params, string)
        if isinstance(pred[1], numpy.ndarray):
            obj = {"tweetContent": string, "result": pred[0], "negscore": str(pred[1][0][0]), "neuscore": str(pred[1][0][1]), "posscore": str(pred[1][0][2])}
        else:
            obj = {"tweetContent": string, "result": pred[0], "negscore": str(0.0), "neuscore": str(0.0), "posscore": str(0.0)}
        jsonstr = json.dumps(obj)
        return jsonstr

if __name__ == "__main__":
    OBJSENTIMENT = isentiment_pred()
    logging.info(OBJSENTIMENT.predict("hello"))