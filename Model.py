# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 17:07:18 2020

@author: pedro
"""

'''
import numpy as np
import sklearn as sk
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsRegressor
'''

score_old = 0
for i in range(1,1000):
    X_train, X_test, y_train,y_test = train_test_split(X, y, test_size = 0.3)
    knn = KNeighborsClassifier(algorithm = 'brute')
    
    knn.fit(X_train, y_train)
    
    y_pred = knn.predict(X_test)
    score = metrics.accuracy_score(y_test,y_pred)
    if score > score_old:
        score_old = score
        print(score)
    



print([y_pred])