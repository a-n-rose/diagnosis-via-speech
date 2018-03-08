'''
takes in .csv with speaker, 40 columns for mfcc, and label (English, German) and turns it to machine learning friendly format
'''
import pandas as pd
df = pd.read_csv("sp_df_Eng_Germ2.csv")
ml_df = df.ix[:,"0":"39"]
#one-hot-encode English and German
ml_df["language"] = df["label"]=="English"
ml_df.to_csv("engerm_mfcc_ml.csv")
