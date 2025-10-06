import network
import urequests
import time
import machine
import dht

# FiFi asetukset
SSID = "YOUR_WIFI_SSID"
PASSWORD = "YOUR_WIFI_PASSWORD"

# Vaihda omaksi serverin ip:ksi
SERVER_URL = "http://192.168.1.50:3000/data"

# Laite ID
DEVICE_ID = "esp32-01"

# Anturi
sensor = dht.DHT22(machine.Pin(4))

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to wifi...")
    while not wlan.isconnected():
        time.sleep(1)
    print("Connected:", wlan.ifconfig())
    return wlan

def send_data(temp, hum):
    try:
        payload = {
            "device_id": DEVICE_ID,
            "ts": int(time.time() * 1000),
            "temperature": temp,
            "humidity": hum
        }
        headers = {"Content-Type": "application/json"}
        res = urequests.post(SERVER_URL, json=payload, headers=headers)
        print("Sent:", res.text)
        res.close()
    except Exception as e:
        print("Error while sending:", e)

def main():
    connect_wifi()
    while True:
        try:
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            print("Temperature:", temp, "°C   Humidity:", hum, "%")
            send_data(temp, hum)
        except Exception as e:
            print("Error while measuring:", e)
        time.sleep(15)

if __name__ == "__main__":
    main()
