import Adafruit_DHT
from Sensors.Readings import Humidity, Temperature
import board
import busio
import adafruit_bme280

class Sensor:
    def __init__(self, INIT_PIN, INIT_QUEUE_SIZE, INIT_SENSOR_ID):
        self.GPIO_PIN = INIT_PIN
        self.DATA_QUEUE_SIZE = INIT_QUEUE_SIZE
        self.sensor_id = INIT_SENSOR_ID
        self.values = []

    def readFromDevice(self):
        return []

    def read(self):
        values = self.readFromDevice()
        for i in range(len(values)):
            self.values[i].update(values[i])

    def initialRead(self):
        values = self.readFromDevice()
        for i in range(len(values)):
            self.values[i].initialUpdate(values[i])

    def outputReadings(self):
        return self.values

# Adafruit Temperature/Humidity Sensor
class BME280(Sensor):
    i2c = busio.I2C(board.SCL, board.SDA)
    def __init__(self, INIT_PIN, INIT_QUEUE_SIZE, INIT_SENSOR_ID):
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        super().__init__(INIT_PIN, INIT_QUEUE_SIZE, INIT_SENSOR_ID)
        self.humidityObj = Humidity()
        self.temperatureObj = Temperature()
        self.values = [self.humidityObj, self.temperatureObj]

    def readFromDevice(self):
        return self.bme280.humidity, self.bme280.temperature

# Adafruit Temperature/Humidity Sensor
class AM2302(Sensor):
    DHT_SENSOR = Adafruit_DHT.DHT22

    def __init__(self, INIT_PIN, INIT_QUEUE_SIZE, INIT_SENSOR_ID):
        super().__init__(INIT_PIN, INIT_QUEUE_SIZE, INIT_SENSOR_ID)
        self.humidityObj = Humidity()
        self.temperatureObj = Temperature()
        self.values = [self.humidityObj, self.temperatureObj]

    def readFromDevice(self):
        humidity, temperature = None, None
        while (humidity is None) or (temperature is None):
            humidity,temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.GPIO_PIN)
        return humidity, temperature

# Demo class for the purpose of getting varried AM2302 readings
class AM2303(Sensor):
    DHT_SENSOR = Adafruit_DHT.DHT22
    
    def __init__(self, INIT_PIN, INIT_QUEUE_SIZE, INIT_SENSOR_ID):
        super().__init__(INIT_PIN, INIT_QUEUE_SIZE, INIT_SENSOR_ID)
        self.humidityObj = Humidity()
        self.temperatureObj = Temperature()
        self.values = [self.humidityObj, self.temperatureObj]

    def readFromDevice(self):
        humidity, temperature = None, None
        while (humidity is None) or (temperature is None):
            humidity,temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.GPIO_PIN)
        return humidity + 1, temperature + 1

# Demo class meant to simulate temperature-only sensor
class AM2304(Sensor):
    DHT_SENSOR = Adafruit_DHT.DHT22

    def __init__(self, INIT_PIN, INIT_QUEUE_SIZE, INIT_SENSOR_ID):
        super().__init__(INIT_PIN, INIT_QUEUE_SIZE, INIT_SENSOR_ID)
        self.humidityObj = Humidity()
        self.values = [self.humidityObj]

    def readFromDevice(self):
        humidity, temperature = None, None
        while (humidity is None) or (temperature is None):
            humidity,temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.GPIO_PIN)
        return humidity


# Demo class meant to simulate humidity-only sensor
class AM2305(Sensor):
    DHT_SENSOR = Adafruit_DHT.DHT22

    def __init__(self, INIT_PIN, INIT_QUEUE_SIZE, INIT_SENSOR_ID):
        super().__init__(INIT_PIN, INIT_QUEUE_SIZE, INIT_SENSOR_ID)
        self.temperatureObj = Temperature()
        self.values = [self.temperatureObj]
    
    def readFromDevice(self):
        humidity, temperature = None, None
        while (humidity is None) or (temperature is None):
            humidity,temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.GPIO_PIN)
        return temperature