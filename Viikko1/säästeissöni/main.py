from machine import Pin
import dht
from time import sleep, ticks_ms

sensor = dht.DHT22(Pin(15))

PRINT_INTERVAL_MS = 30000
TEMP_THRESHOLD = 0.5
HUM_THRESHOLD = 2.0

last_temp = None
last_hum = None
last_print_time = 0

print("Weather station started.")

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        now = ticks_ms()

        print_due = False

        if last_temp is None or last_hum is None:
            print_due = True
        elif abs(temp - last_temp) >= TEMP_THRESHOLD or abs(hum - last_hum) >= HUM_THRESHOLD:
            print_due = True
        elif now - last_print_time >= PRINT_INTERVAL_MS:
            print_due = True

        if print_due:
            print("Temperature: {:.1f}°C  Humidity: {:.1f}%".format(temp, hum))
            last_temp = temp
            last_hum = hum
            last_print_time = now

    except Exception as e:
        print("Failed to read sensor:", e)

    sleep(0.1)
