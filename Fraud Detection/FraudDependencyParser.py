# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:41:20 2020

@author: Suvralipi
"""

import configparser

class FraudDependencyParser(object):
    
    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.read('fraud_config.ini')

        # Reading file path cofigurations
        self.model_path = self.config['Path']['model_path']
        self.inpath = self.config['Path']['inpath']
        self.outpath = self.config['Path']['outpath'] 
            
        self.all_cols_name = self.config['Data']['all_cols_name'].split(',')
        self.col_names_data = self.config['Data']['col_names_data'].split(',')
        self.col_encoded_data = self.config['Data']['col_encoded_data'].split(',')
        self.col_name_target = self.config['Data']['col_name_target']
        self.amount = self.config['Data']['amount']
        self.category = self.config['Data']['category']
        self.age = self.config['Data']['age']
        self.gender = self.config['Data']['gender']
        
    