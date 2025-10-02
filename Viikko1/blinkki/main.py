import time
from machine import Pin
from time import sleep
time.sleep(0.1) # Wait for USB to become ready

led = Pin("LED", Pin.OUT)

while True:
    led.toggle()
    sleep(1)
