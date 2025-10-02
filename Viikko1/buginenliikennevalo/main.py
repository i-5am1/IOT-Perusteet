from machine import Pin
from time import sleep

red = Pin(15, Pin.OUT)
yellow = Pin(14, Pin.OUT)
green = Pin(13, Pin.OUT)

button = Pin(16, Pin.IN)

buzzer = Pin(12, Pin.OUT)

def all_off():
    red.value(0)
    yellow.value(0)
    green.value(0)

lights = [(red, 2), (green, 2), (yellow, 1)]
current_index = 0

while True:
    led, duration = lights[current_index]
    
    all_off()
    led.value(1)
    
    elapsed = 0
    slice_time = 0.1
    
    while elapsed < duration:
        if button.value() == 1:
            all_off()
            red.value(1)
            buzzer.value(1)
            
            while button.value() == 1:
                sleep(0.1)
            
            sleep(1)
            buzzer.value(0)
            
            break
        
        sleep(slice_time)
        elapsed += slice_time
    
    current_index = (current_index + 1) % len(lights)
