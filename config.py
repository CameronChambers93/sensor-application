#!/usr/bin/python
from configparser import ConfigParser
import json
import pdb
from Sensors.Sensors import *
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Numeric, DateTime, and_, select, between
import psycopg2
import datetime
import os
import time

modelDict = {
        'AM2302': AM2302,
        'AM2303': AM2303,
        'AM2304': AM2304,
        'AM2305': AM2305,
        'BME280': BME280
    }


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def settings(filename='groupSettings.ini'):
    with open(filename, 'r') as file:
        data = file.read()
    obj = json.loads(data)
    return obj

def saveSettings(data, filename='settings.ini'):
    with open('groupSettings.ini', 'w') as file:
        json.dump(data, file)


def getSensors(DATA_QUEUE_SIZE):
    with open('settings.ini', 'r') as file:
        data = file.read()
    sensorList = json.loads(data)['sensors']
    sensors = []
    device_name = json.loads(data)['device_name']
    for sensor in sensorList:
        Sensor = modelDict[sensor['sensor_type']]
        newSensor = Sensor(sensor['gpio_pin'], DATA_QUEUE_SIZE, sensor['sensor_id'])
        sensors.append(newSensor)
    return sensors, device_name

def connect():
    # read connection parameters
    params = config()
    
    POSTGRES_URL = params.get("url")
    POSTGRES_USER = params.get("user")
    POSTGRES_PW = params.get("password")
    POSTGRES_DB = params.get("database")

    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

    # The return value of create_engine() is our connection object
    dbConnection = sqlalchemy.create_engine(DB_URL, client_encoding='utf8')
    
    # We then bind the connection to MetaData()
    dbMetaInfo = sqlalchemy.MetaData(bind=dbConnection, reflect=True)
    
    return dbConnection, dbMetaInfo