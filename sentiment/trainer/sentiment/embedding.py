#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import numpy as np
from data_helper import *
import logging

class Embedding:
    word2idx = ""
    wordlist = ""
    weight = ""
    data_dir = ""
    word_size = 2000000
    process = "filter"

    def __init__(self, process, fn, fn_raw="", word_size=2000000):
        self.data_dir = fn
        self.fn_raw = fn_raw
        self.data_dir = fn
        if warn_file_not_exist(self.data_dir):
            os.mkdir(self.data_dir)
        self.process = process
        self.word_size = word_size

    def __getitem__(self, word):
        if word in self.word2idx:
            return self.weight[self.word2idx[word]]
        else:
            return self.weight[0]

    def load(self):
        self.load_filter()

    def load_filter(self):
        fn_wordlist = os.path.join(self.data_dir, "wordlist_{}.npy".format(self.word_size))
        fn_word2idx = os.path.join(self.data_dir, "word2idx_{}.pp".format(self.word_size))
        fn_weight = os.path.join(self.data_dir, "weight_{}.npy".format(self.word_size))
        logging.info('Starting to load the numpy arrays : ' + fn_wordlist + ' , ' + fn_weight + ' , ' + fn_word2idx)
        self.wordlist = np.load(fn_wordlist,allow_pickle=True)
        logging.info('Loaded: fn_wordlist')
        self.weight = np.load(fn_weight,allow_pickle=True)
        logging.info('Loaded: fn_weight')
        self.word2idx = pickle_file(fn_word2idx)
        logging.info('Loaded: fn_word2idx')