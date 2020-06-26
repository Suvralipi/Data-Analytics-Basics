# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 17:57:19 2020

@author: 561527
"""
import pandas as pd
import numpy as np
from math import sqrt

# Classifier Libraries
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost.sklearn import XGBClassifier
from FraudDependencyParser import FraudDependencyParser
# Other Libraries
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, average_precision_score
from sklearn.metrics import log_loss, mean_squared_error
import visualizedata as vd
import pickle
from FraudDependencyParser import FraudDependencyParser

import warnings
warnings.filterwarnings("ignore")

import gc
gc.enable()


obj = FraudDependencyParser()


def createOutParam(modelName, testX, testY, predY, pred_prob):
    AUPRC = average_precision_score(testY, pred_prob[:, 1])
    accuracy= accuracy_score(testY, predY)
    precision= precision_score(testY, predY)
    recall =  recall_score(testY, predY)
    f1score = f1_score(testY, predY)
    accuracy = accuracy_score(testY, predY)
    logloss = log_loss(testY, predY)
    mse = mean_squared_error(testY, predY)
    rmse = sqrt(mean_squared_error(testY, predY))
    model_perf = {'ModelName': modelName,
                  'precision': precision,
                  'recall': recall,
                  'f1_score': f1score,
                  'accuracy' : accuracy,
                  'Avg_precision_recall':AUPRC,
                  'log_loss':logloss,
                  'mse':mse,
                  'rmse':rmse
                 }        
    return model_perf
    
def FraudLogisticRegression(trainX, trainY, testX, testY):
    log_cfl = LogisticRegression(C=0.1)
    log_cfl.fit(trainX, trainY)
    predY_lr = log_cfl.predict(testX)
    pred_prob = log_cfl.predict_proba(testX)
    modelName = 'LogisticRegression'
    model_perf = createOutParam(modelName, testX, testY, predY_lr, pred_prob)
    
    logistic_pkl_filename = obj.model_path + '/LogisticRegression_20200202.pkl'
    # Open the file to save as pkl file
    logistic_model_pkl = open(logistic_pkl_filename, 'wb')
    pickle.dump(log_cfl, logistic_model_pkl)
    # Close the pickle instances
    logistic_model_pkl.close()
        
    return model_perf
        
def FraudDecisionTree(trainX, trainY, testX, testY):   
    dt = DecisionTreeClassifier(criterion="entropy", max_depth=5)
    dt.fit(trainX, trainY)
    #Predict the response for test dataset
    predY = dt.predict(testX)
        
    # sorted-feature importances from the preliminary decision tree
    dt_feature_importance = pd.Series(dt.feature_importances_ , 
                        index = obj.col_names_data).sort_values(ascending= False)
        
    pred_prob = dt.predict_proba(testX)
    modelName = 'DecisionTree'
    model_perf = createOutParam(modelName, testX, testY, predY, pred_prob)
    
    
    vd.plot_feature_importance(dt_feature_importance)
    #vd.generate_DecisionTreeGraph(dt)
    
    decisiontree_pkl_filename = obj.model_path + '/DecisionTree_20200202.pkl'
    # Open the file to save as pkl file
    decisiontree_model_pkl = open(decisiontree_pkl_filename, 'wb')
    pickle.dump(dt, decisiontree_model_pkl)
    # Close the pickle instances
    decisiontree_model_pkl.close()
        
    return model_perf     
    
def FraudXGB(trainX, trainY, testX, testY):
    # Long computation in this cell (~1.8 minutes)
    clf_xgb = XGBClassifier(max_depth=7, learning_rate=0.05, n_estimators=400, 
                                objective="binary:hinge", booster='gbtree', 
                                n_jobs=-1, nthread=None, gamma=0, min_child_weight=1, max_delta_step=0, 
                                subsample=1, colsample_bytree=1, colsample_bylevel=1, reg_alpha=0, reg_lambda=1, 
                                scale_pos_weight=1, base_score=0.5, random_state=42)
        
    pred_prob = clf_xgb.fit(trainX, trainY).predict_proba(testX)
    predY_xgb = clf_xgb.predict(testX) 
    modelName = 'XGBoostClassifier'
    model_perf = createOutParam(modelName, testX, testY, predY_xgb, pred_prob)
    XGBoostClassifier_pkl_filename = obj.model_path + '/XGBoostClassifier_20200202.pkl'
    # Open the file to save as pkl file
    XGBoostClassifier_model_pkl = open(XGBoostClassifier_pkl_filename, 'wb')
    pickle.dump(clf_xgb, XGBoostClassifier_model_pkl)
    # Close the pickle instances
    XGBoostClassifier_model_pkl.close()
    
    return model_perf
    
def FraudRandomForest(trainX, trainY, testX, testY):
    ## Random Forest with Tuned parameters
    rf_cfl = RandomForestClassifier(n_estimators = 200,
                                max_features = 3, 
                                 min_samples_leaf = 2, 
                                 min_samples_split = 10, 
                                 n_jobs = -1,
                                random_state = 42)

    rf_cfl.fit(trainX, trainY)
    predY_rf = rf_cfl.predict(testX)
    pred_prob = rf_cfl.predict_proba(testX)
    modelName = 'RandomForest'
    model_perf = createOutParam(modelName, testX, testY, predY_rf, pred_prob)
    
    RFClassifier_pkl_filename = obj.model_path + '/RandomForest_20200202.pkl'
    # Open the file to save as pkl file
    RFClassifier_model_pkl = open(RFClassifier_pkl_filename, 'wb')
    pickle.dump(rf_cfl, RFClassifier_model_pkl)
    # Close the pickle instances
    RFClassifier_model_pkl.close()
    
    return model_perf
