# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 09:46:13 2020

@author: 561527
"""

# Import libraries
import numpy as np
from flask import Flask, request, jsonify
import pickle
import pandas as pd
import preprocessing as prep

MODEL_FOLDER = 'C:/Users/561527.MFDMAI/Fraud'
UPLOAD_FOLDER = 'C:/Users/561527.MFDMAI/fraud_build/Test_files'

app = Flask(__name__)

# Load the model
model_pkl = MODEL_FOLDER + '/RandomForest_20200202.pkl'
model = pickle.load(open(model_pkl,'rb'))
testfile = pd.read_csv(UPLOAD_FOLDER + '/TestFile.csv')
testX, testY = prep.preprocess_testdata(testfile)

@app.route('/predict',methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)
    # Make prediction using model loaded from disk as per the data.
    prediction = model.predict(testX)
    testfile['predicted_fraud'] = prediction
    print(testfile.head())
    return jsonify(testfile)

if __name__ == '__main__':
    app.run(port=5000, debug=True)