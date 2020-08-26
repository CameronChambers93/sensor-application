from sqlalchemy import Table
import datetime
import os
import time

def clearWindow():
    os.system( 'clear' )

class SensorController:
    def __init__(self, _dbConnection, _dbMetaInfo, _sensors, _device_name, _timeBetweenInserts, _data_queue_size):
        self.dbConnection = _dbConnection
        self.dbMetaInfo = _dbMetaInfo
        self.sensors = _sensors
        self.device_name = _device_name
        self.timeBetweenInserts = _timeBetweenInserts
        self.DATA_QUEUE_SIZE = _data_queue_size
        self.dbTable = Table('sensor_data', _dbMetaInfo, autoload=True)
        self.timeOfLastInsert = None

    # Initializes the sensors, creating the initial recording sample queue
    def initializeSensors(self):
        print("Getting initial readings...")
        count = 1
        while count - 1 < self.DATA_QUEUE_SIZE:
            for sensor in self.sensors:
                sensor.initialRead()
            self.outputToConsole(initialized=False)
            time.sleep(1)
            count += 1
        currentTime = datetime.datetime.now()
        self.timeOfLastInsert = currentTime
        return currentTime

    # Reads each sensor, popping then inserting a new recording into the sample queue 
    def readSensors(self):
        for sensor in self.sensors:
                sensor.read()

    # Returns whether update is available or not
    def isUpdateAvailable(self):
        if datetime.datetime.now() - self.timeOfLastInsert + datetime.timedelta(seconds=2, milliseconds=30) > self.timeBetweenInserts:
            return True
        else:
            return False

    # Updates the database using credentials found in database.ini
    def updateDB(self):
        currentTime = datetime.datetime.now()
        readings = self.readingsToJSON()
        self.dbConnection.execute(self.dbTable.insert(), ({"room_name": self.device_name, "data": readings, "date_time": currentTime}))
        self.timeOfLastInsert = currentTime

    # Outputs controller status as JSON for database updates
    def readingsToJSON(self):
        readings = []
        for sensor in self.sensors:
            for reading in sensor.outputReadings():
                currentReading = reading.output()
                readings.append({'sensor_id': sensor.sensor_id, 'type': currentReading['type'], 'value': currentReading['value']})
        return readings

    # Outputs the current status of the controller to the console
    def outputToConsole(self, initialized = True):
        currentTime = datetime.datetime.now()
        clearWindow()
        if initialized == False:
            print("Initializing....")
        else:
            print(f'sensorController.py\nLast update: {self.timeOfLastInsert}\nCurrent time: {currentTime}\n')
        for sensor in self.sensors:
            for reading in sensor.outputReadings():
                currentReading = reading.output()
                print(f'Sensor:\t{sensor.sensor_id}\tType:\t{currentReading["type"]}\tValue:\t{currentReading["value"]}')