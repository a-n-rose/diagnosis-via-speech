import os
import logging.handlers
import time

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix

from collect_SQL_data_debug import does_db_exist, Extract_Data
from my_logger import start_logging, get_date

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        start_time = time.time()
        
        ####################################################
        #######################################################
        #######################################################
        
        #MAKE SURE THESE VARIABLES ARE CORRECT!!!!!
        #define variables:
        script_purpose = 'trainmfcc' #will name logfile - generally don't need to change this unless training something other than MFCCs
        current_filename = os.path.basename(__file__)
        session_name = get_date() #make sure this session has a unique identifier - link to model name and logging information
        table = 'table' 
        variable_train = ['German_noise_matched_train_22050','English_noise_matched1_48kHz_16bit']
        variable_test = ['German_noise_matched_test_22050','English_noise_matched1_44.1kHz_16bit']
        gen_notes = 'General notes about the current session' #whatever you'd like to note down/document
        
        rowstart_train = 0  #the row to start pulling data from database
        rowlim_train = 1000000  #limit the number of rows
        rowstart_test = 0
        rowlim_test = 1000000
        num_mfcc = 13  #up to 40 (depending on the data)
        include_1stMFCC = False  #True includes 1st coefficient, which is correlated with loudness of speech
        language = ['English','German']
        int_classifier = [i for i in range(len(language))]
        langint_dict = dict(zip(int_classifier, language))
        
        #for initializing (keras) model/classifier:
        classifier = 'Sequential()'
        activation_layer = 'relu'
        kernel_initializer = 'uniform'
        activation_output = 'sigmoid'
        optimizer = 'adam'
        loss = 'binary_crossentropy'
        metrics = ['accuracy']
        
        #for training the model:
        batch_size = 10
        epochs = 100
        num_rows = 2000000
        
        #names to save modoel:
        model_name = 'dl_{}_{}_{}'.format(session_name,script_purpose,num_rows)
        
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        
        start_logging(script_purpose)
        logging.info("Running script: {}".format(current_filename))
        logging.info("Session: {}".format(session_name))
        logging.info("Language and classifier pairs: {}".format(langint_dict))
        logging.info("Integer label: {}".format(int_classifier))
        logging.info("Table: {}".format(table))
        logging.info("Variable for training: {}".format(variable_train))
        logging.info("Variable for testing: {}".format(variable_test))
        logging.info("Row start (train): {}\nRow limit (train): {}".format(rowstart_train,rowlim_train))
        logging.info("Row start (test): {}\nRow limit (test): {}".format(rowstart_test,rowlim_test))
        logging.info("MFCC number: {}".format(num_mfcc))
        logging.info("1st MFCC included? {}".format(include_1stMFCC))
        logging.info("Notes: {}".format(gen_notes))
        
        
        ########### Starting Program ############
        
        db_name = 'db_name'
        if does_db_exist(db_name):
            currdb = Extract_Data(db_name)
            column = currdb.get_depvar_colname(table)
            
            #prep data for training
            for j in range(len(variable_train)):
                if j > 0:
                    df_temp = currdb.prep_df(table,column,variable_train[j],rowstart_train,rowlim_train,num_mfcc,langint_dict)
                    df_train = df_train.append(df_temp)
                else:
                    df_train = currdb.prep_df(table,column,variable_train[j],rowstart_train,rowlim_train,num_mfcc,langint_dict)
            
                
            x1_train = df_train.as_matrix()
            startcol_train = currdb.get_startcol(x1_train,include_1stMFCC)
            x_train = x1_train[:,startcol_train:]
            
            X_train = x_train[:,:-1]
            y_train = x_train[:,-1]
            
            #prep test data 
            for j in range(len(variable_test)):
                if j > 0:
                    df_temp = currdb.prep_df(table,column,variable_test[j],rowstart_test,rowlim_test,num_mfcc,langint_dict)
                    df_test = df_test.append(df_temp)
                else:
                    df_test = currdb.prep_df(table,column,variable_test[j],rowstart_test,rowlim_test,num_mfcc,langint_dict)
            
            x1_test = df_test.as_matrix()
            startcol_test = currdb.get_startcol(x1_test,include_1stMFCC)
            x_test = x1_test[:,startcol_test:]
            
            X_test = x_test[:,:-1]
            y_test = x_test[:,-1]
            
            #should be same number of labels for both train and test data, so only take values from one or the other
            num_labels = len(np.unique(y_train))
            if num_labels == 2:
                num_labels = 1
            
            filter_size = 2
            num_inputs = X_train.shape[1]
            
            ###### Building Classifier ######
            
            classifier = Sequential()
            num_outputs = num_labels
            #used the average between number of input features and output labels
            av_inout = int((num_inputs+num_outputs)/2)
            
            #add input layer and first hidden layer:
            classifier.add(Dense(activation, units=av_inout, input_dim=num_inputs, kernel_initializer))
            
            #add second hidden layer:
            classifier.add(Dense(activation, units = av_inout, kernel_initializer))
            
            #add the output layer:
            classifier.add(Dense(activation, units = num_outputs, kernel_initializer))
            
            #compile ANN
            #'binary_crossentropy' for binary output label
            classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy',metrics = ['accuracy'])
            
            
            #Document in loggin system:
            logging.info("classifier = {}\nnum_outputs = {}\nav_inout = int(({}+{})/2)\nclassifier.add(Dense(activation={}, units=av_inout, input_dim=num_inputs, kernel_initializer={}))\nclassifier.add(Dense(activation = {}, units = av_inout, kernel_initializer = {}))\nclassifier.add(Dense(activation = {}, units = num_outputs, kernel_initializer = {}))\nclassifier.compile(optimizer = {}, loss = {},metrics = {})".format(classifier,num_labels,num_inputs,num_outputs, activation_layer, kernel_initializer, activation_layer, kernel_initializer, activation_output, kernel_initializer, optimizer, loss, metrics))
            
            
            #training model
            classifier.fit(X_train,y_train,batch_size,epochs)
            
            y_pred = classifier.predict(X_test)
            y_pred = (y_pred > 0.5)
            
            for lang in language:
                #calculate accuracy
                pass
            
            y_test=y_test.astype(bool)
            cm = confusion_matrix(y_test, y_pred)
            logging.info("Confusion Matrix for {}:\n{}".format(language,cm))
            acc = "%s: %.2f%%" % (classifier.metrics_names[1], score[1]*100)
            logging.info(acc)
            print("Model Evaluation:")
            print(acc)
            
            logging.info("Saving model and weights as: \n{}.json\n{}.h5".format(model_name,model_name))
            
            model_json = classifier.to_json()
            with open(model_name+'.json',w) as json_file:
                json_file.write(model_json)
            classifier.save_weights(model_name+'.h5')
            
            
            end_time = time.time()
            
            total_duration = (end_time - start_time)/3600
            logging.info("Total time to complete task: {} hours".format(total_duration))
            print("Finished training model - model and weights are saved.")

        
    except Exception as e:
        logging.exception("Error occurred: %s" % e)
        
    finally:
        if currdb.conn:
            currdb.conn.close()
            logging.info("Database successfully closed")
