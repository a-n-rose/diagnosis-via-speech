'''
uploads previously saved ANN model, specific for the English-German MFCC ANN model
runs the model with "new" data and prints accuracy
'''
from keras.models import model_from_json
import pandas as pd
import numpy as np
import sqlite3
from sqlite3 import Error
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

def table2dataframe(c,table,lim = None):
    try:
        if lim:
            limit = str(lim)
            c.execute("SELECT * FROM "+table+" LIMIT " + limit)
            data = c.fetchall()
            df = pd.DataFrame(data)
            return df
        else:
            c.execute("SELECT * FROM "+table)
            data = c.fetchall()
            df = pd.DataFrame(data)
            return df
    except Error as e:
        print(e)
    
    return None

start = time.time()

print("connecting to database")
conn = create_connection('sp_mfcc_new.db')
c = create_cursor(conn)

# load json and create model
file_weights = 'engerm_annweights_13mfcc_100epochs_1000000'
file_model = 'engerm_annmodel_13mfcc_100epochs_1000000' 
json_file = open(file_model+'.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(file_weights+".h5")
print("Loaded model from disk")



#import new data
try:
    #get new MFCC data
    print("collecting new data --> df")
    df_new = table2dataframe(c,'mfcc_13')


except Exception as e:
    print(e)

df_new[14] = 0
x1 = df_new.as_matrix()
x = x1[:,2:]
X = x[:,:-1]
y = x[:,-1]

# evaluate loaded model on new data
try:
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    score = loaded_model.evaluate(X, y, verbose=0)
    print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
except Exception as e:
    print(e)
    
    
y_pred = loaded_model.predict(X)
y_pred = (y_pred > 0.5)
from sklearn.metrics import confusion_matrix
y_test=y.astype(bool)
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)
