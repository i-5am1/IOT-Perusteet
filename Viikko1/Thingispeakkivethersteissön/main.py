from machine import Pin
import dht
from time import sleep, ticks_ms
import network
import urequests

# FIFI setuppi
SSID = "SupopakunWiFI"
PASSWORD = "VaihdaM1nut!"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    sleep(0.5)
print("Connected:", wlan.ifconfig())

# Thingspeakki shitti
THINGSPEAK_API_KEY = "meitsin-api-avain"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

def send_to_thingspeak(temp, hum):
    try:
        url = "{}?api_key={}&field1={:.1f}&field2={:.1f}".format(
            THINGSPEAK_URL, THINGSPEAK_API_KEY, temp, hum
        )
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak")
        return True
    except Exception as e:
        print("Failed to send to ThingSpeak:", e)
        return False

sensor = dht.DHT22(Pin(15))

# Taikanummerot jotka kertoo millo pitää laittaa settii menee
TEMP_THRESHOLD = 0.5
HUM_THRESHOLD = 2.0
THINGSPEAK_INTERVAL_MS = 15000  # D:

last_print_temp = None
last_print_hum = None
last_sent_temp = None
last_sent_hum = None
last_thingspeak_time = ticks_ms()

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        now = ticks_ms()

        # local printti chekki
        if (last_print_temp is None or abs(temp - last_print_temp) >= TEMP_THRESHOLD
            or last_print_hum is None or abs(hum - last_print_hum) >= HUM_THRESHOLD):
            print("Temperature: {:.1f}°C  Humidity: {:.1f}%".format(temp, hum))
            last_print_temp = temp
            last_print_hum = hum

        # Thingspeakki chekki
        if ((last_sent_temp is None or abs(temp - last_sent_temp) >= TEMP_THRESHOLD
            or last_sent_hum is None or abs(hum - last_sent_hum) >= HUM_THRESHOLD)
            and now - last_thingspeak_time >= THINGSPEAK_INTERVAL_MS):
            if send_to_thingspeak(temp, hum):
                last_sent_temp = temp
                last_sent_hum = hum
                last_thingspeak_time = now

    except Exception as e:
        print("Failed to read sensor:", e)

    sleep(2)
