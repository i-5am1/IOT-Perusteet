from machine import Pin
from time import sleep

led = Pin(18, Pin.OUT)

button = Pin(13, Pin.IN, Pin.PULL_UP)

while True:
    if button.value() == 0:
        led.value(1)
    else:
        led.value(0)
    sleep(0.01)