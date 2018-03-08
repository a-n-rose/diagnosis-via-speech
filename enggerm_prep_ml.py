'''
takes in .csv with speaker, 40 columns for mfcc, and label (English, German) and turns it to machine learning friendly format
'''
import pandas as pd
file = pd.read_csv("sp_df_Eng_Germ2.csv")
ml_file = file.ix[:,"0":"39"]
#one-hot-encode English and German
ml_file["language"] = file["language"]
ml_file.to_csv("engerm_mfcc_ml.csv")
