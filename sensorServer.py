from flask import Flask
from flask import request
from flask import jsonify
from config import saveSettings
import datetime
import pdb
import os
import re


import threading

#Remove all CORS on deployment
#from flask_cors import CORS, cross_origin


app = Flask(__name__)


#Remove the following on deployment
#cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/save_settings', methods=['POST'])
#@cross_origin()
def save_settings():
    newSettings = request.json
    saveSettings(newSettings)
    os.system('sudo systemctl restart sensor.controller.service')
    return "Success"
