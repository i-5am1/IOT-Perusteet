from machine import Pin
from time import sleep, localtime

pir = Pin(28, Pin.IN)

try:
    led = Pin("LED", Pin.OUT)
except Exception:
    led = Pin(25, Pin.OUT)

last_val = 0

def formatted_time():
    t = localtime()
    return "{:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5])

print("PIR alarm started. Waiting for motion...")

while True:
    val = pir.value()

    if val == 1 and last_val == 0:
        print("[{}] Motion detected!".format(formatted_time()))
        led.value(1)

    if val == 0:
        led.value(0)

    last_val = val
    sleep(0.05)
