import sys
import time
import network
from SettingsSingleton import SettingsSingleton
from Relay import Relay


class Board:
    def __init__(self):
        self.settings = SettingsSingleton.getInstance()
        self.staIf = network.WLAN(network.STA_IF)
        self.bRelays = {}

    def setup(self):
        self.settings.load()
        self.staIf.active(True)
        self.wifi()
        self.relays()
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
            return False

        for relayName, relaySettings in relays.items():
            relay = Relay(relayName)
            relay.setup()
            self.bRelays[relayName] = relay

    def sensors(self):
        # light sensor on ESP-12F Witty
        # adc = machine.ADC(0)
        # adc.read() -- 29->384
        pass

    def loop(self):
        while True:
            for relay_name in self.bRelays:
                relay_object = self.bRelays[relay_name]
                # check if there is a server message for this relay

                # check if relay has a button and if button has been pressed
                if relay_object.button is None:
                    continue

                relay_object.check_button()

            # nani
            time.sleep(0.5)
