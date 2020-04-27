# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:51:50 2020

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

#nltk.download()
def remove_stopword(sentence):
    return [w for w in sentence if not w in stop_words]


# Create set related to positive and negative review
def word_feats(words):
    return dict([(word, True) for word in words])

def word_cleaner(data):
    words = word_tokenize(data)
    words = [toktok.tokenize(sent) for sent in sent_tokenize(data)]
    wordsFiltered = []
    if not words:
        pass
    else:
        for w in words[0]:
            if w not in stopWords:
                wordsFiltered.append(w)
                end=time.time()
    return wordsFiltered





reviews = pd.read_csv("Breviews.csv")
Sreviews = pd.read_csv("Sreviews.csv")
Hotel = pd.read_csv("Datafiniti_Hotel_Reviews.csv")
pd.set_option("display.max.columns", None)




reviews = pd.concat([reviews, Sreviews])
reviews = pd.DataFrame(reviews).astype('str').reset_index(drop = True)


#cleaning separations and tokenization
comments = reviews['comments']

#comments = comments.'str.replace('/.|/,|/!|/?' ,'').astype("str")
#tcomments = [nltk.word_tokenize(str(sentence)) for sentence in comments]
#tcomments = tcomments.str.replace(',','')


############################### hotel data for training

Hotel = Hotel[['reviews.rating', 'reviews.text']].where(Hotel[
    'primaryCategories'] == 'Accommodation & Food Services').dropna().reset_index(
        drop = True)

Hotel['Positive'] = 0
Hotel['Negative'] = 0
Hotel['Neutral'] = 0

Hotel.loc[Hotel['reviews.rating'] > 3, "Positive"] = 1
Hotel.loc[Hotel['reviews.rating'] < 3, "Negative"] = 1
Hotel.loc[Hotel['reviews.rating'] == 3, "Neutral"] = 1


## removing punctuation and digits
for i in string.punctuation + string.digits:
    Hotel['reviews.text'] = Hotel['reviews.text'].str.replace(
        i,"")

for i in string.punctuation + string.digits:
    comments = comments.str.replace(
        i,"")   



# Stopwords, numbers and punctuation to remove
remove_punct_and_digits = dict([(ord(punct), ' ') for punct 
                                in string.punctuation + string.digits])
stopWords = set(stopwords.words('english'))




# Example
Positive = Hotel['reviews.text'].where(Hotel['Positive']==1).dropna().reset_index(
    drop = True)
Negative = Hotel['reviews.text'].where(Hotel['Negative']==1).dropna().reset_index(
    drop = True)
wordsFiltered = word_cleaner(Positive[1])
print(Positive[1])
print(wordsFiltered)


neg_set=[(word_feats(word_feats(word_cleaner(Negative[i]))), 0)
         for i in range(len(Negative))]

pos_set=[(word_feats(word_feats(word_cleaner(Positive[i]))), 1)
         for i in range(len(Positive))]

comments_set = [(word_feats(word_feats(word_cleaner(comments[i]))), 0)
         for i in range(len(comments))]

# Finally some Machine is Learning!
# Train the model and use CV to test accuracy

negcutoff = int(len(neg_set)*3/4)
poscutoff = int(len(pos_set)*3/4)
trainfeats = neg_set[:negcutoff] + pos_set[:poscutoff]
testfeats = neg_set[negcutoff:] + pos_set[poscutoff:]
classifier = NaiveBayesClassifier.train(trainfeats)
print( 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats))

# Builds the dataframe of words with respective sentiment and score

cpdist = classifier._feature_probdist
word=[]
score=[]
sentiment=[]

for (fname, fval) in classifier.most_informative_features(300):
            def labelprob(l):
                return cpdist[l, fname].prob(fval)

            labels = sorted([l for l in classifier._labels
                             if fval in cpdist[l, fname].samples()],
                            key=labelprob)
            if len(labels) == 1:
                continue
            l0 = labels[0]
            l1 = labels[-1]
            if cpdist[l0, fname].prob(fval) == 0:
                ratio = 'INF'
            else:
                ratio = '%8.1f' % (cpdist[l1, fname].prob(fval) /
                                   cpdist[l0, fname].prob(fval))
            sentiment.append(int(l1))
            word.append(fname)
            score.append(float(ratio))

word_scores=pd.DataFrame({'word':word,'sentiment':sentiment,'score':score})
neg_word_scores=word_scores[word_scores.sentiment==0]
pos_word_scores=word_scores[word_scores.sentiment==1]
print(word_scores[word_scores['sentiment']==1].head())
print(word_scores[word_scores['sentiment']==0].head())


# I want to create two new columns, one that will give a positive and one a negative score
# Sums positive and negative scores for a given review
def pos_sentiment_sum(review):
    pos=0
    asd=word_cleaner(review)
    set_w=set(pos_word_scores.word)-set(['no','negative','positive'])
    
    for word in asd:
        if word in set_w:
            pos+=pos_word_scores[pos_word_scores['word']==word].score.iloc[0]
    
    return pos

def neg_sentiment_sum(review):
    neg=0
    asd=word_cleaner(review)
    set_w=set(neg_word_scores.word)-set(['no','negative','positive'])
    
    for word in asd:
        if word in set_w:
            neg+=neg_word_scores[neg_word_scores['word']==word].score.iloc[0]
    
    return neg

# TEST
for i in range(0,100):
    print('negative score:', neg_sentiment_sum(comments[i]),\
          'positive score:', pos_sentiment_sum(comments[i]))
    
# VERY SLOW! AROUND 45min for full database
# I comment it out so it does not need to run when I submit

# This is the final step where we get the additional columns 
# Produce the pos and neg colums in database

#=================
pos_col=[]
for i in range(len(comments)):
    pos_col.append(pos_sentiment_sum(comments[i]))
comments['pos_score'] = pos_col

neg_col=[]
for i in range(len(comments)-1):
    neg_col.append(neg_sentiment_sum(comments[i]))
comments['neg_score'] = neg_col
#=================