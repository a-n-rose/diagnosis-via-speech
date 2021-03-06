#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script pulls data from sqlite3 database and applies ANN to 12 MFCC columns and a binary label column
saves model to "engerm_annmodel_13mfcc_(num epochs)epochs.json" with weights saved to "engerm_annweights_13mfcc_(num epochs)epochs.hd"

This particular model uses 100 batch_size and 10 epochs
"""

 
import pandas as pd
import sqlite3
from sqlite3 import Error
import numpy as np
import time


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return None

def create_cursor(conn):
    try:
        return conn.cursor()
    except Error as e:
        print(e)

def table2dataframe(c,table,lim = 10):
    try:
        limit = str(lim)
        c.execute("SELECT * FROM "+table+" LIMIT " + limit)
        data = c.fetchall()
        df = pd.DataFrame(data)
        return df
    except Error as e:
        print(e)
    
    return None


start = time.time()
batch_size = 100
epochs = 100
num_rows = 1000

print("connecting to database")
conn = create_connection('sp_mfcc.db')
c = create_cursor(conn)


try:
    #get English MFCC data
    print("collecting English data --> df")
    #limit number of rows retrieved to specified number
    df_e = table2dataframe(c,'mfcc13_English',num_rows)

    #get German MFCC data
    print("collecting German data --> df")
    df_g = table2dataframe(c,'mfcc_13',num_rows)

except Exception as e:
    print(e)
    
    
print("combining data and preparing it for training the ann")

#identify German as 1
df_g[14] = 1
#identify English as 0
df_e[14] = 0

comb_df = pd.concat([df_g,df_e])

x1 = comb_df.as_matrix()
#remove filename and first mfcc coefficient (only refers to noise level)
x = x1[:,2:]


#separating into dependent and independent variables:
X = x[:,:-1]
y = x[:,-1]

dataprep_time = time.time()
print("Data is prepared. Time total: ", dataprep_time-start, " sec")

print("Now creating ann classifier")
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation


# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

num_labels = len(np.unique(y))
if num_labels == 2:
    num_labels =1

filter_size = 2
num_inputs = X.shape[1]

#build model
print("Building classifier model")
#initialize model:
classifier = Sequential()
#used the average between number of input features and output labels: (12+1)/2 --> appx. 6
num_outputs = num_labels
av_inout = int((num_inputs+num_outputs)/2)

#add input layer and first hidden layer:
classifier.add(Dense(activation="relu", units=av_inout, input_dim=num_inputs, kernel_initializer="uniform"))

#add second hidden layer:
classifier.add(Dense(activation = 'relu', units = av_inout, kernel_initializer = 'uniform'))

#add the output layer:
classifier.add(Dense(activation = 'sigmoid', units = num_outputs, kernel_initializer = 'uniform'))  

#compile ANN
#'binary_crossentropy' for binary output label
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy',metrics = ['accuracy'])




print("Model complete. Now training it on the data with batchsize of ", batch_size, " and ", epochs, " epochs")
classifier.fit(X_train,y_train,batch_size = batch_size, epochs = epochs)

model_time = time.time()
print("Training model complete")

y_pred = classifier.predict(X_test)
y_pred = (y_pred > 0.5)
from sklearn.metrics import confusion_matrix
y_test=y_test.astype(bool)
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)


print("Saving model and weights")
# serialize model to JSON
model_json = classifier.to_json()
with open("engerm_annmodel_13mfcc_"+str(epochs)+"epochs_"+str(num_rows)+".json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
classifier.save_weights("engerm_annweights_13mfcc_"+str(epochs)+"epochs_"+str(num_rows)+".h5")
print("Saved model to disk")

total_time = time.time()

print("Time to prepare data: ", dataprep_time-start, " sec" )
print("Time to train model: ", model_time-start, " sec")
print("Time to complete program and save models and weights: ", total_time-start, " sec")
