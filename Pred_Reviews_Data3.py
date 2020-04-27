# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:38:56 2020

@author: pedro
"""

import numpy as np
import pandas as pd
import seaborn as sns
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string, re
sid = SentimentIntensityAnalyzer()

reviews = pd.read_csv("Breviews.csv")
Sreviews = pd.read_csv("Sreviews.csv")


reviews = pd.concat([reviews, Sreviews])
reviews = pd.DataFrame(reviews).astype('str').reset_index(drop = True)
r = reviews
reviews = reviews[['listing_id','id','comments']]


##Example

#a = sid.polarity_scores(reviews['comments'][0])

#remove stopwords and punctuation

for j in range(len(reviews)):  
    for i in string.punctuation + string.digits:
        reviews['comments'][j] = reviews['comments'][j].replace(i,"")


#base toda  
a = []
reviews['pos'] = ''
reviews['neg'] = ''
reviews['neu'] = ''
reviews['compound'] = ''
for i in range(len(reviews)):
    a = sid.polarity_scores(reviews['comments'][i])
    reviews['pos'][i] = a['pos']
    reviews['neg'][i] = a['neg']
    reviews['neu'][i] = a['neu']
    reviews['compound'][i] = a['compound'] 

reviews = pd.read_csv("reviews_sentiment.csv")

reviews = reviews.groupby('listing_id').sum().reset_index()



















































