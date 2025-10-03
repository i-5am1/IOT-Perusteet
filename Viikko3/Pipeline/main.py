from machine import Pin
import dht
from time import sleep, ticks_ms
import network
import urequests

# FiFi settinks
SSID = "SupopakunWiFI"
PASSWORD = "VaihdaM1nut!"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    sleep(0.5)
print("Connected:", wlan.ifconfig())

# Palvelimen osoite. teknisesti ei toimi jos sääasema pyörii wokwissa picolla mutta se on nyt vaan ns.placeholderi
SERVER_URL = "http://localhost:3000/data"

sensor = dht.DHT22(Pin(15))

# update rajat tai jtn
TEMP_THRESHOLD = 0.5
HUM_THRESHOLD = 2.0
SEND_INTERVAL_MS = 15000

last_sent_temp = None
last_sent_hum = None
last_send_time = ticks_ms()

def send_to_server(temp, hum):
    try:
        payload = {"temperature": temp, "humidity": hum}
        headers = {"Content-Type": "application/json"}
        response = urequests.post(SERVER_URL, json=payload, headers=headers)
        response.close()
        print("Data sent to server:", payload)
        return True
    except Exception as e:
        print("Failed to send to server:", e)
        return False

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        now = ticks_ms()

        #sendaa shittii jos tapahtuu huomattava muutos tai aikaa on kulunut tietty määrä
        if ((last_sent_temp is None or abs(temp - last_sent_temp) >= TEMP_THRESHOLD
            or last_sent_hum is None or abs(hum - last_sent_hum) >= HUM_THRESHOLD)
            and now - last_send_time >= SEND_INTERVAL_MS):

            if send_to_server(temp, hum):
                last_sent_temp = temp
                last_sent_hum = hum
                last_send_time = now

    except Exception as e:
        print("Sensor read failed:", e)

    sleep(2)
