import sys
import machine
import time
from SettingsSingleton import SettingsSingleton
from Button import Button
from Led import Led


class Relay:
    """Relay object"""

    def __init__(self, name):
        self.name = name
        self.settings = None
        self.rSettings = None
        self.button = None
        self.led = None
        self.pin = None
        self.pinNr = None
        self.on = 1
        self.off = 0
        self.last_change = 0
        self.min_time_change = 500

    def setup(self):
        self.settings = SettingsSingleton.getInstance()
        self.rSettings = self.settings.getRelaySettings(self.name)

        if not self.rSettings:
            print('Relay settings are incorrect!')
            sys.exit(1)

        try:
            self.pinNr = self.rSettings["relay_pin"]
        except:
            print('Relay pin number is missing!')
            sys.exit(1)

        if not (self.pinNr >= 0):
            print('Relay pin number is incorrect!')
            sys.exit(1)

        invertState = "false"
        try:
            invertState = self.rSettings["invert"]
            if not (invertState == "false"):
                self.off = 1
                self.on = 0
        except:
            pass

        try:
            self.min_time_change = self.settings.get('button_pressed_time')
        except:
            pass

        self.pin = machine.Pin(self.pinNr, machine.Pin.OUT)
        self.pin.value(self.off)

        try:
            button_pin = self.rSettings["button_pin"]
            self.button = Button(button_pin)
            self.button.setup()
        except:
            # no button for this relay
            pass

        led_default_state = 0
        try:
            led_default_state = self.rSettings["default_led_state"]
        except:
            pass

        try:
            led_pin = self.rSettings["led_pin"]
            self.led = Led(led_pin, led_default_state)
            self.led.setup()
        except:
            # no led for this relay
            pass

    def set_state(self, new_state):
        if not self.allow_change():
            return None

        self.last_change = time.ticks_ms()

        if new_state is 1:
            self.pin.value(self.on)
            if self.led is not None:
                self.led.start_blink()
            return 1

        if new_state is 0:
            self.pin.value(self.off)
            if self.led is not None:
                self.led.stop_blink()
            return 0

    def get_state(self):
        return self.pin.value()

    def toggle_state(self):
        actual_state = self.pin.value()
        if actual_state is self.on:
            return self.set_state(0)

        if actual_state is self.off:
            return self.set_state(1)

    def check_button(self):
        if self.button.get_state() is True:
            if not self.allow_change():
                self.button.state_read()
                return None

            self.button.state_read()
            return self.toggle_state()

    def allow_change(self):
        if not ((time.ticks_ms() - self.last_change) > self.min_time_change):
            return False

        return True

    def get_name(self):
        return self.name
