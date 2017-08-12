import sys
import machine


class Button:
    """Button object"""

    def __init__(self, pin_number):
        self.pin = None
        if not pin_number:
            print("No pin number for button!")
            sys.exit(1)
        self.pinNr = pin_number
        self.pressed = False

    def setup(self):
        self.pin = machine.Pin(self.pinNr, machine.Pin.IN, machine.Pin.PULL_UP)
        self.pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.pressed_action)

    def pressed_action(self, pin):
        self.pressed = True

    def state_read(self):
        self.pressed = False

    def get_state(self):
        return self.pressed
