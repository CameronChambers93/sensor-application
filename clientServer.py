from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Numeric, DateTime, and_, select, between, desc
import psycopg2
from config import config, settings, saveSettings
import datetime
import pdb
import time
import requests
import json

app = Flask(__name__)

#Remove all CORS on deployment
from flask_cors import CORS, cross_origin
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def connect():
    # read connection parameters
    params = config()

    POSTGRES_URL = params.get("url")
    POSTGRES_USER = params.get("user")
    POSTGRES_PW = params.get("password")
    POSTGRES_DB = params.get("database")

    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(DB_URL, client_encoding='utf8')
    
    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con, reflect=True)
    
    return con, meta

con, meta = connect()

sensor_data = Table('sensor_data', meta, autoload=True)

def getDateSearchClause(room, fromDate, toDate):
        return select([sensor_data]).where(
            and_(
                sensor_data.c.room_name == room,
                between(sensor_data.c.date_time, fromDate, toDate)
            ))

def getCurrentReadingClauses(room):
    return select([sensor_data]).where(sensor_data.c.room_name == room).order_by(desc("date_time")).limit(1)

# Returns the recordings of each Pi between two given DateTimes
@app.route('/get_readings')
@cross_origin()		#Remove on deployment
def getReadings():
    room = request.args.get('room_name', None)
    fromDate = request.args.get('from_date', None)
    toDate = request.args.get('to_date', None)
    clause = getDateSearchClause(room, fromDate, toDate)
    records = []
    for row in con.execute(clause):
        records.append({"room_name": row[0], "data": row[1], "date_time": row[2]})
    return jsonify(records)  # TODO: Convert date_time in DB to UTC timezone

# Returns a dictionary detailing the current sensor readings of each Pi
# {"date_time": DateTime,
#  "readings": ["Reading Type", "Value"],
#  "sensor": Number}
@app.route('/get_current_readings')
@cross_origin()		#Remove on deployment
def getCurrentReadings():
    _settings = settings()
    records = []
    for room in _settings:
        sensorLookups = {}
        for sensor in room['sensors']:
            sensorLookups[str(sensor['sensor_id'])] = sensor['sensor_name']
        currentClause = getCurrentReadingClauses(room['device_name'])
        for row in con.execute(currentClause):
            room, data, date_time = row
            currData = {}
            for dm in data:
                if currData.get(str(dm['sensor_id'])) is None:      # TODO: str() is required due to data inconsistencty
                    currData[str(dm['sensor_id'])] = {'name': sensorLookups[str(dm['sensor_id'])]}
                currData[str(dm['sensor_id'])][dm['type']] = dm['value']
            records.append({"room_name": room, "readings": currData, "date_time": date_time})
    returnData = {'data': records}
    return jsonify(returnData)  # TODO: Convert date_time in DB to UTC timezone

# Returns a dictionary detailing the settings of each Pi
# { "device_name": String",
#   "sensors": [{ "gpio_pin": Number,
#                 "sensor_id" Number,
#                 "sensor_name": String,
#                 "sensor_type": String}]
# }
@app.route('/get_settings')
@cross_origin()		#remove on deployment
def getSettings():
    _settings = settings()
    return jsonify(_settings)

# Sets the settings of the system
@app.route('/set_settings', methods=['POST'])
@cross_origin()		#remove on deployment
def setSettings():
    pdb.set_trace()
    newSettings = request.json['data']
    if newSettings['ip'] != 'localhost':
        url = 'http://' + newSettings['ip'] + ':5000/save_settings'
        r = requests.post(url, json=newSettings)
    _settings = settings()
    for i in range(len(_settings)):
        if _settings[i]['device_name'] == newSettings['device_name']:
            _settings[i] = newSettings
    saveSettings(_settings)
    return jsonify(_settings)
