

class Sensor:
    def __init__(self, name, pin_number):
        self.pin_number = pin_number
        self.pin = None
        self.type = None
        self.name = name

    def setup(self):
        pass

    def get_value(self):
        pass

    def get_type(self):
        return self.type

    def get_name(self):
        return self.name
