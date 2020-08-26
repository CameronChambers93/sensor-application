class Reading:
    def __init__(self):
        self.readings = []
        self.total = 0

    def update(self, reading):
        self.total -= self.readings.pop()
        self.total += reading
        self.readings.append(reading)

    def initialUpdate(self, reading):
        self.total += reading
        self.readings.append(reading)

    def getCurrentValue(self):
        tmpArr = list(self.readings)
        tmpArr.sort()
        if len(self.readings) % 2 == 0:
            c = len(self.readings) // 2
            return round((tmpArr[c-1] + tmpArr[c])/2,1)
        else:
            c = len(self.readings) // 2
            return round(tmpArr[c],1)


class Temperature(Reading):
    def output(self):
        return {'type': 'temperature', 'value': self.getCurrentValue()}


class Humidity(Reading):
    def output(self):
        return {'type': 'humidity', 'value': self.getCurrentValue()}