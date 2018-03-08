'''
uploads previously saved ANN model, specific for the English-German MFCC ANN model
runs the model with "new" data and prints accuracy
'''
from keras.models import model_from_json
import pandas as pd
import numpy as np



# load json and create model
json_file = open('engerm_model_ann.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("engerm_weights_ann.h5")
print("Loaded model from disk")


#import "test" data (same data as from before... this is just to show it works)
sp_df = pd.read_csv("engerm_mfcc_ml.csv",index_col = "Unnamed: 0")
X = np.array(sp_df.ix[:,:-1])
y = np.array(sp_df.ix[:,-1])

# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(X, y, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
