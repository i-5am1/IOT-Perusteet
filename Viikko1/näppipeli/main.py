from machine import Pin
from time import sleep, ticks_ms
import urandom

led = Pin(15, Pin.OUT)

button = Pin(14, Pin.IN, Pin.PULL_DOWN)

def wait_for_press():
    while button.value() == 0:
        sleep(0.01)

def wait_for_release():
    while button.value() == 1:
        sleep(0.01)

while True:
    led.value(1)

    wait_for_release()

    min_on_time = 1.0
    random_additional = urandom.randint(0, 20) / 10.0
    delay = min_on_time + random_additional
    sleep(delay)

    led.value(0)

    start_time = ticks_ms()
    wait_for_press()
    reaction_time = ticks_ms() - start_time

    print("Your reaction time: {} ms".format(reaction_time))

    wait_for_release()
    sleep(0.2)
