# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 11:17:13 2020

@author: 561527
"""

from sklearn.model_selection import train_test_split
from FraudDependencyParser import FraudDependencyParser
import pandas as pd 

obj = FraudDependencyParser()

def preprocess(df):
    
    # Treating the input dataset to have a standardised data
    df = df[df['gender'].isin(['M','F'])]
    df = df[df['age'].isin(['1','2','3','4','5','6'])]
    df['age'] = df['age'].astype(int)
    
    return df

def convertcat_to_intVar(df):
    # copy dataframe for preliminary decision tree
    df_fi = df[obj.col_names_data]
    # Selecting Columns whose values are categorical (in practice, the strings)
    col_categorical = df_fi.select_dtypes(include= ['object']).columns
    # Converting data-type as 'category;
    for col_name in col_categorical:
        df_fi[col_name+'_encoded'] = df_fi[col_name].astype('category')
    #Converting categorical entries to integers
    col_categorical1 = df_fi.select_dtypes(include= ['category']).columns
    df_fi[col_categorical1] = df_fi[col_categorical1].apply(lambda x: x.cat.codes)
        
    return df_fi[col_categorical1]


def splitDataset(df):
    
    # Declaring 'data-dataframe'  and 'target-dataframe'
    X = df[obj.col_encoded_data]
    y = df[obj.col_name_target]
    ## Model Selection
    trainX, testX, trainY, testY = train_test_split(X, y, test_size = 0.2, random_state = 42)

    return trainX, testX, trainY, testY

def preprocess_testdata(df):
    ## combine the training data with the test data so as to get correct Label encoding values
    train_df=pd.read_csv(obj.inpath+'Input_dataset.csv')
    train_df= preprocess(train_df)
    train_df['train'] = 1
    df['train'] = 0
    combined = pd.concat([train_df, df])
    ## convert Categorical variables to Integer Variables
    df_fi = pd.concat([combined, convertcat_to_intVar(combined)],axis=1)
    test_df = df_fi[df_fi['train']==0]
    
    return test_df
    