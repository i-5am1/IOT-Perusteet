from machine import Pin; from time import sleep
led = Pin("LED", Pin.OUT)
while 1: led.toggle() or sleep(0.5)

