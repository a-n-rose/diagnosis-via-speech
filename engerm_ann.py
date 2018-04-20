#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 09:57:43 2018

@author: airos

script pulls data from sqlite3 database and applies ANN to 12 MFCC columns and a binary label column
saves model to "engerm_annmodel_13mfcc.json" with weights saved to "engerm_annweights_13mfcc.hd"

This particular model uses 100 batch_size and 500 epochs
"""


import pandas as pd
import sqlite3
import numpy as np
import time

start = time.time()
batch_size = 100
epochs = 500

conn = sqlite3.connect("sp_mfcc.db")
c = conn.cursor()

#get English MFCC data
c.execute("SELECT * FROM mfcc13_English") 
data_English = c.fetchall()

#get German MFCC data
c.execute("SELECT * FROM mfcc_13") 
data_German = c.fetchall()


#put in pandas dataframe
df_g = pd.DataFrame(data_German)
df_e = pd.DataFrame(data_English)
#identifying German as 1
df_g[14] = 1
#identifying English as 0
df_e[14] = 0

#match row length
rows_g = df_g.shape[0]
rows_e = df_e.shape[0]
min_rows = min(rows_g,rows_e)
df_g2 = df_g.iloc[:min_rows]
df_e2 = df_e.iloc[:min_rows]
comb_df = pd.concat([df_g2,df_e2])

x1 = comb_df.as_matrix()
#remove filename and first mfcc coefficient (only deals with noise level)
x = x1[:,2:]


#separating into dependent and independent variables:
X = x[:,:-1]
y = x[:,-1]


dataprep_time = time.time()

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
#from keras.optimizers import Adam
#from sklearn import metrics


# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
# from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

if len(y.shape) > 1:
    num_labels = y.shape[1]
else:
    num_labels = len(y.shape)

filter_size = 2
num_inputs = X.shape[1]

#build model
model = Sequential()
#used the average between number of input features and output labels: (12+1)/2 --> appx. 6
num_outputs = 1
av_inout = int((num_inputs+num_outputs)/2)
model.add(Dense(av_inout,input_shape = (num_inputs,) ))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(av_inout))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(num_labels))
#since output labels are binary, use sigmoid here. Otherwise, softmax
model.add(Activation('sigmoid'))
#'binary_crossentropy' for binary output label
model.compile(loss = 'binary_crossentropy',metrics = ['accuracy'], optimizer = 'adam')

model.fit(X_train,y_train,batch_size = batch_size, epochs = epochs)

y_pred = model.predict(X_test)
y_pred = (y_pred > 0.5)

model_time = time.time()

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_pred)
print("ANN applied with batch size of "+batch_size+" and "+ epochs+ " epochs")
print(cm)


# serialize model to JSON
model_json = model.to_json()
with open("engerm_annmodel_13mfcc.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("engerm_annweights_13mfcc.h5")
print("Saved model to disk")

total_time = time.time()

print("Time to prepare data: ", dataprep_time, " sec" )
print("Time to train model: ", model_time, " sec")
print("Time to complete program and save models and weights: ", total_time, " sec")
