import sys
import machine
from AlarmsSingleton import AlarmsSingleton


class Led:

    def __init__(self, pin_number, default_state):
        self.pin_number = pin_number
        self.default_state = default_state
        self.pin = None
        self.on = 0
        self.off = 1
        self.timer = None
        self.alarmId = None
        self.alarms = None
        self.blinking = False
        self.first_run = True

    def setup(self):
        if not (self.pin_number > -1):
            print("LED pin number is not numeric!")
            sys.exit(1)

        self.pin = machine.Pin(self.pin_number, machine.Pin.OUT)

        if self.default_state is 1:
            self.off = 0
            self.on = 1

        self.pin.value(self.off)

        self.alarms = AlarmsSingleton.getInstance()
        self.alarmId = self.alarms.get_index("led", self.pin_number)

    def start_blink(self):
        if self.blinking is True:
            print("Big error: LED is in blink mode")
            sys.exit(1)

        self.blinking = True
        self.timer = machine.Timer(self.alarmId)
        self.timer.init(period=800, mode=machine.Timer.PERIODIC, callback=lambda t:self.toggle())

    def stop_blink(self):
        # Stop the timer
        self.timer.deinit()
        # self.timer = None

        self.blinking = False

        # Set led to default value
        self.pin.value(self.off)

    def toggle(self):
        if self.pin.value() is self.on:
            self.pin.value(self.off)
            # print("LED off")
            return self.off

        if self.pin.value() is self.off:
            self.pin.value(self.on)
            # print("LED on")
            return self.on

    def after_first_run(self):
        if self.first_run is not True:
            return False

        self.first_run = False

        if self.default_state is 1:
            self.off = 0
            self.on = 1

        if self.default_state is 0:
            self.off = 1
            self.on = 0
