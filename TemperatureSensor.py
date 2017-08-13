import machine
from Sensor import Sensor


class TemperatureSensor(Sensor):
    def setup(self):
        self.type = 'temperature'
        self.pin = machine.ADC(self.pin_number)

    def get_value(self):
        return self.pin.read()
