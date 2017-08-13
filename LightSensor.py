import machine

from Sensor import Sensor


class LightSensor(Sensor):
    def setup(self):
        # light sensor on ESP-12F Witty
        # adc = machine.ADC(0)
        # adc.read() -- 29->384
        self.type = 'light'
        self.pin = machine.ADC(self.pin_number)

    def get_value(self):
        return self.pin.read()
