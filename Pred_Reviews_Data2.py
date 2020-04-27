# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 11:15:25 2020

@author: pedro
"""

import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.text import Text
import string, re
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from nltk.tokenize import ToktokTokenizer
from nltk.classify import NaiveBayesClassifier

from nltk.tokenize import ToktokTokenizer
toktok = ToktokTokenizer()
import time
from nltk.classify import NaiveBayesClassifier

def remove_punctuation(sentence):
    for i in string.punctuation + string.digits:
        sentence = sentence.replace(
            i,"")
    return sentence

def remove_stopwords(sentence):
    return[w for w in sentence if not w in stop_words]

reviews = pd.read_csv("Breviews.csv")
Sreviews = pd.read_csv("Sreviews.csv")
Hotel = pd.read_csv("Datafiniti_Hotel_Reviews.csv")
pd.set_option("display.max.columns", None)


reviews = pd.concat([reviews, Sreviews])
reviews = pd.DataFrame(reviews).astype('str').reset_index(drop = True)

comments = reviews['comments']
comments = comments.str.cat()


sentences = sent_tokenize(comments)
cleaned_sentences = [remove_punctuation(i) for i in sentences]
sentences_words = [word_tokenize(sentence) for sentence in cleaned_sentences]

stop_words = list(set(stopwords.words('english')))
filtered_words = [remove_stopwords(i) for i in sentences_words]

POS = [nltk.pos_tag(tokenized_sent) for tokenized_sent in filtered_words]




















































