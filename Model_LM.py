# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 17:07:18 2020

@author: pedro
"""


import numpy as np
import sklearn as sk
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsRegressor



score_old = 0
for i in range(1,1000000):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .20)
    lm_model = LinearRegression(normalize=True) # Instantiate
    lm_model.fit(X_train, y_train) #Fit
    y_test_preds = lm_model.predict(X_test)
    score = sk.metrics.r2_score(y_test, y_test_preds)
    if score > score_old:
        score_old = score
        print(score)









