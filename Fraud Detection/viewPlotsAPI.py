# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 15:43:34 2020

@author: 561527
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:43:19 2020

@author: 561527
"""

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/Users/561527.MFDMAI/fraud_build'
ALLOWED_EXTENSIONS = {'jpg', 'pdf', 'txt', 'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from flask import send_from_directory

@app.route('/mfdm/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
    app.run(debug=True)
    