#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os, sys, argparse, glob, subprocess, logging, re
import time
from datetime import datetime
from multiprocessing  import Pool
import numpy as np
import pandas as pd
import pickle
#from pycorenlp import StanfordCoreNLP
from pattern.en import parse

## set globle variables ##
APP_DIR= os.path.split(os.path.abspath(__file__))[0]
APP_NAME= os.path.split(os.path.splitext(__file__)[0])[1]

logger = logging.getLogger(__name__)
description=""
epilog=""

def warn_file_not_exist( file ):
    flag= True
    if not os.path.exists(file):
        logger.warning('warn_file_not_exist >> file {} not found!'.format( file))
    else:
        flag= False
    return(flag)

def warn_file_exist( file ):
    flag= True
    if os.path.exists(file):
        logger.warning('warn_file_exist >> file {} found!'.format( file))
    else:
        flag= False
    return(flag)

def pickle_file(path="", y="", force=False):
    if y== "":
        #logger.info('pp >> load {}'.format( path ))
        return pickle.load( open( path, "rb"  )  )
    else:
        if os.path.exists(path):
            logger.warning("pp >> pp file exist! {}".format(path))
            if not force:
                return
        pickle.dump( y, open( path, "wb"  )  )
        #logger.info("pp >> write file {} finished!".format(path))

def sen2idx(params):
    sen, word2idx, MAX_SEQUENCE_LENGTH,stopwords = params
    vec= np.zeros(MAX_SEQUENCE_LENGTH)
    i= 0
    for word in sen:
        if word in stopwords.keys():
            continue
        #if tag(word)[0][1] in ["NN","IN"]:
        #    continue
        if word in word2idx:
            vec[i]= word2idx[word]
            i = i+1
            if i>= MAX_SEQUENCE_LENGTH:
                return vec
    return vec


#def coreNLP_sentiment(input_string):
   #nlp = StanfordCoreNLP('http://localhost:9000')
     #parse_string = parseText(input_string)
    #nlp_pred = nlp.annotate(parse_string.decode("utf8").encode("utf8"), properties={
    #    'annotators': 'sentiment',
     #   'outputFormat': 'json'})["sentences"][0]['sentiment']

    #return nlp_pred

def parseText(text):
    eyes = "[8:=;]"
    nose = "['`\\-]?"
    text = '%s' % text.lower()
    text = text.replace(":)","<SMILE>")
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", "\"") \
        .replace("&apos;", "\'").replace("<br /><br />"," ")
    text = re.sub(r"2nd|3rd|[4-9]th","<NUMBER>",text)
    text = re.sub(r'1st',"first",text)
    text = re.sub(r'\[.{0,}\]',"",text)
    text=re.sub("https?://\\S+\\b|www\\.(\\w+\\.)+\\S*|https?:\\S+","<URL>",text).replace("/", " / ")
    text=re.sub("@\\w+","<USER>",text)
    text=re.sub(''+eyes+nose+"[)d]+|[)d]+"+nose+eyes+'/i',"<SMILE>",text)
    text=re.sub(''+eyes + nose + "p+/i","<LOL FACE>",text)

    text=re.sub(''+eyes+nose+"\\(+|\\)+"+nose+eyes+'',"<SAD FACE>",text)
    text=re.sub(" lol","<LAUGH>",text)
    text=re.sub(''+eyes+nose+"[\\/|l*]","<NEUTRAL FACE>",text)
    text=re.sub("<3","<LOVE>",text)
    text=re.sub("[-+]?[.\\d]*[\\d]+[:,.\\d]*","<NUMBER>",text)
    text=re.sub("#\\S+","<HASH TAG>",text)
    text = text.replace(":-D","<big smile>").replace(":D","<big smile>").replace(":-(","<sad>").replace(":(","<sad>")\
        .replace(":-P","<smiley with tongue out>").replace("B-)","<cool>").replace(":-*","<throw someone a kiss>")\
        .replace(";-)","<winking>").replace(";)","<winking>").replace(":-x","<my lips are sealed>").replace("<.","<bouquet>")\
        .replace(":-O","<suprised>").replace(":O","<suprised>").replace("$_$","<money eyes>").replace("@_@","<puzzled>")\
        .replace(">_<","<go crazy>").replace("T_T","<crying>").replace("= =b","<sweating>").replace(">3<","<kiss>")
#        .replace("=_=#","<angry>").replace("(××","<dizzy>").replace("|(-_-)|","<unheard>")\
#        .replace("(.^.)","<dissatisfied>").replace("(=^_^=)","<loveliness>").replace("[{(>_<)]}","<shuddering>")\
 #       .replace("0_0","<fishy>").replace(".(...).","<helpless>").replace("*\(^_^)/*","<good luck>")\
  #      .replace("*\(^_^)/*","<good luck>").replace("b.....d","<thumbs-up>").replace("^(oo)^","<pig's head>")

    text=re.sub("[^\\x20-\\x7e]+","",text).replace("@","").replace("#", "").replace("&amp;", "&").strip(' ')

    return text

def clean(sentence):
    input = '%s' % sentence
    input = re.sub(r"/", " ", input)
    input = re.sub(r"\s", " ", input)
    input  = re.sub(r'[^\x00-\x7F]+',"", input) #replace non-ascii with " "
    input = input.lower()

    input = re.sub(r'^rt',"",input) # remove RT at begining
    input = re.sub(r"'s"," ",input)
    input = re.sub(r'\$acn',"",input)
    input = re.sub(r"[()?,.;:*%$&~^\\\"\/|#=`]","",input) #remove &amp
    input = re.sub(r'<user>|<hash tag>|<url>|<number>',"",input)
    input = re.sub(r'[<>-]'," ",input)
    return input

def hca_clean(sentence,qid):
    #print qid
    input = '%s' % sentence
    input
    input = re.sub(r"/", " ", input)
    input = re.sub(r"\s", " ", input)
    input  = re.sub(r'[^\x00-\x7F]+',"", input) #replace non-ascii with " "
    input = input.lower()

    input = re.sub(r'^rt',"",input) # remove RT at begining
    input = re.sub(r"'s"," ",input)
    input = re.sub(r'\$acn',"",input)
    input = re.sub(r"[()?,.;:*%$&~^\\\"\/|#=`]","",input) #remove &amp
    input = re.sub(r'<user>|<hash tag>|<url>|<number>',"",input)
    input = re.sub(r'[<>-]'," ",input)
    if qid ==1:
        input = re.sub(r'no comment.{0,}|no commits|nothing to mention|no commands|'
                       r'no inputs|nope|nill|nothing|none|nil|'
                       r'not applicable|not sure|no idea|^no$|no suggestion|na$|'
                       r'no one$|no concerns|no action|no actions',"negative",input)
    if qid ==2:
        input = re.sub(r'no comment.{0,}|no commits|nothing to mention|no commands|ok$|^no.{1,5}challenge.{0,1}|'
                       r' no.{1,15}challeng.{1,3}|n\'t.{1,15}challenge.{0,1}|no inputs|nope|nill$|none$|nil$|not any|'
                       r'not applicable|^not sure$|no idea|no suggestion|na$|nothing|^no$|non$|^not.{1,5}yet|n/a|'
                       r'no concerns|no.{1,10}issue.{0,1}'," happy great good ",input)
    if qid ==3:
        input = re.sub(r'no comment.{0,}|no commits|nothing to mention|no commands|'
                       r'no inputs|nope|nill|nothing|none|nil|nothing|'
                       r'not applicable|^not sure$|no idea|no$|no suggestion|na$|'
                       r'no one$|no concerns|no action|no actions',"neutral",input)

    return input


def en_token(sentence, idx=-1, lower=True, stopwords= {}):
    word= []
    if lower:
        sentence= sentence.lower()
    try:
        for sen in parse(sentence, lemmata=True).split():
            for w in sen:
                word.append(w[idx])
    except Exception as e:
        logger.error(u"{} : {}".format(e, sentence))
    sep = []
    for i in word:
        if i in stopwords.keys():
            continue
        else:
            sep.append(i)
    return sep


def loadStopwords(stopwords_path):
    if (stopwords_path is None) or (os.path.exists(stopwords_path) is False):
        return {}
    else:
        stopwords = {}
        with open(stopwords_path) as f:
            for i in f.readlines():
                stopwords[i.strip()] = ''
        #print stopwords
        return stopwords
