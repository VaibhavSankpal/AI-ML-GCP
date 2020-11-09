#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import argparse
from argparse import RawTextHelpFormatter
import logging
from keras.utils.np_utils import *
from keras.layers import *
from keras.layers.convolutional import *
from keras.preprocessing import sequence
from keras.models import *
from keras.utils import layer_utils

from data_helper import *
#import ConfigParser

##PVV# adding a missing function - potential issue with keras
import numpy as np
def categorical_probas_to_classes(objp):
    return np.argmax(objp, axis=1)
##PVV# end of code for missing function

## set globle variables ##
APP_DIR = os.path.split(os.path.abspath(__file__))[0]
APP_NAME = os.path.split(os.path.splitext(__file__)[0])[1]

LOGGER = logging.getLogger(__name__)
DESCRIPTION = ""
EPILOG = ""

#CONFIG_PATH = os.path.join(APP_DIR, "config.ini")

#CONFIG = ConfigParser.ConfigParser()
#CONFIG.readfp(open(CONFIG_PATH, "rb"))


def eval(params, string):
    o_emb, model, stpwrd, objle, graph = params

    word2idx = o_emb.word2idx
    max_sequence_length = 50
    token = en_token(clean(parseText(string)), stopwords=stpwrd)

    if token == []:
        return "neutral"
    objx = sen2idx((token, word2idx, max_sequence_length, stpwrd))
    with graph.as_default():
        pred = model.predict(objx.reshape((1, max_sequence_length)))
        pred_label = objle.inverse_transform(categorical_probas_to_classes(pred))

    if pred_label[0] == "negative":
        if pred[0][0] > 0.68:
            result = "negative"
        else:
            result = "neutral"
    elif pred_label[0] == "positive":
        if pred[0][2] > 0.55:
            result = "positive"
        else:
            result = "neutral"
    else:
        result = "neutral"

    resultlist = [result, pred]
    return resultlist

def parseArg():
    fn_embedding = '/tmp/language_model.emb'
    fn_out = '/tmp/senti.dtm'
    max_nb_words = '850000'
    stopwords_path = '/tmp/stopwords'
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    return fn_embedding, fn_out, max_nb_words, stopwords_path

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description=DESCRIPTION, epilog=EPILOG, formatter_class=RawTextHelpFormatter)
    PARSER.add_argument('--embedding', dest='fn_embedding', help='input file name.')
    PARSER.add_argument('-o', '--output', dest='fn_out', help='output file name.', default="output.txt")
    PARSER.add_argument('-w', '--stopwords', dest='stopwords_path', help='input stopwords path.')
    PARSER.add_argument('--MAX_NB_WORDS', dest='MAX_NB_WORDS', help='', type=int, default=1000000)
    OP = PARSER.parse_args()
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    LOGGER.info('main >> runing {} with parameters: {}'.format(APP_NAME, OP))
    eval(parseArg(), "hello!")
