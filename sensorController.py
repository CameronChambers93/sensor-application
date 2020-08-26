from config import connect, getSensors
from Sensors.SensorController import SensorController
import datetime
import pdb
import time
import threading
import os

import threading


MINUTES_BETWEEN_INSERT = 1
DATA_QUEUE_SIZE = 10


if __name__ == '__main__':
    dbConnection, dbMetaInfo = connect()
    sensors, device_name = getSensors(DATA_QUEUE_SIZE)
    timeBetweenInserts = datetime.timedelta(minutes=MINUTES_BETWEEN_INSERT)
    controller = SensorController(dbConnection, dbMetaInfo, sensors, device_name, timeBetweenInserts, DATA_QUEUE_SIZE)
    controller.initializeSensors()
    while True:
        controller.readSensors()
        #controller.outputToConsole(initialized=True)	# Uncomment to view sensor status in terminal
        if controller.isUpdateAvailable():
            controller.updateDB()
        time.sleep(5)
