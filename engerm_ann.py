'''
script applies ANN to file with 40 MFCC columns and a binary label column
saves model to "engerm_model_ann.json" with weights saved to "engerm_weights_ann.hd"

'''

import os
import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt





sp_df = pd.read_csv("engerm_mfcc_ml.csv")
X = np.array(sp_df.ix[:,:-1])
y = np.array(sp_df.ix[:,-1])


import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import Adam
from keras.utils import np_utils
from sklearn import metrics


# Splitting the dataset into the Training set and Test set
from sklearn.cross_validation import train_test_split
# from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

if len(y.shape) > 1:
    num_labels = y.shape[1]
else:
    num_labels = len(y.shape)

filter_size = 2

#build model
model = Sequential()
#used the average between number of input features and output labels: (40+1)/2 --> appx. 20
model.add(Dense(20,input_shape = (40,) ))
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(20))
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

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test,y_pred)
print("ANN applied with batch size of "+batch_size+" and "+ epochs+ " epochs")
print(cm)


# serialize model to JSON
model_json = model.to_json()
with open("engerm_model_ann.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("engerm_weights_ann.h5")
print("Saved model to disk")
