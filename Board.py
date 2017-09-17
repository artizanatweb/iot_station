import time
import network
import sys
from Relay import Relay
from SettingsSingleton import SettingsSingleton
# load all sensor classes
from LightSensor import LightSensor
from TemperatureSensor import TemperatureSensor


class Board:
    def __init__(self):
        self.settings = SettingsSingleton.getInstance()
        self.staIf = network.WLAN(network.STA_IF)
        self.bRelays = {}
        self.b_sensors = []
        self.has_relays = None
        self.has_sensors = None
        self.sensors_values = {}

    def setup(self):
        self.settings.load()
        self.staIf.active(True)
        self.wifi()
        self.relays()
        self.sensors()
        # connect to server
        # and report relays status and sensors values

    def wifi(self):
        cfg = self.settings.get('cfg')
        if not cfg:
            print("No WiFi cfg!")
            return False

        if not cfg['ssid']:
            print("Missing SSID!")
            return False

        if not cfg['pass']:
            print("Missing PWD!")
            return False

        self.staIf.connect(cfg['ssid'], cfg['pass'])
        # if self.staIf.isconnected():
        #     print(self.staIf.ifconfig())

    def relays(self):
        relays = self.settings.get('relays')
        if not (len(relays) > 0):
            self.has_relays = False
            return False

        for relayName, relaySettings in relays.items():
            relay = Relay(relayName)
            relay.setup()
            self.bRelays[relayName] = relay

        if len(self.bRelays) > 0:
            self.has_relays = True
        else:
            self.has_relays = False

    def sensors(self):
        c_sensors = self.settings.get('sensors')
        if not c_sensors:
            self.has_sensors = False
            return False

        if not (len(c_sensors) > 0):
            self.has_sensors = False
            return False

        for sensorName, sensorSettings in c_sensors.items():
            try:
                pin_number = int(sensorSettings['pin'])
                sensor_type = sensorSettings['type']
                fl = sensor_type[0].upper()
                class_name = fl + sensor_type[1:] + "Sensor"
                sensor = eval(class_name)(sensorName, pin_number)
                sensor.setup()
                self.b_sensors.append(sensor)
            except:
                print("Error on sensor: " + sensorName)
                continue

        if len(self.b_sensors) > 0:
            self.has_sensors = True
        else:
            self.has_sensors = False

    def loop(self):
        while True:
            if self.has_relays is True:
                for relay_name in self.bRelays:
                    relay_object = self.bRelays[relay_name]
                    # check if there is a server message for this relay
                    # -- to do --
                    # check if relay has a button
                    if relay_object.button is None:
                        continue
                    # check if relay button has been pressed
                    relay_object.check_button()

            if self.has_sensors is True:
                for sensor in self.b_sensors:
                    self.sensors_values[sensor.get_name()] = sensor.get_value()

            # nani
            time.sleep(0.5)
