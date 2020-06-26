from machine import Pin
from utime import ticks_ms

class Led():
    def __init__(self, pin, active_high=True):
        self.active_high = active_high
        self.led = Pin(pin, Pin.OUT)
        self.state(False)
        self.last = 0

    def logic(self, value):
        return value if self.active_high else not value

    def state(self, value=None):
        if value is not None:
            self.led.value(self.logic(value))
        return self.logic(self.led.value())

    def blink(self, period):
        if ticks_ms() - self.last >= period:
            self.state(not self.state())
            self.last = ticks_ms()


        

