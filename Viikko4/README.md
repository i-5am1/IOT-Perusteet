Tämä kansio sisältää IoT-pipelinen: MicroPython-laite lähettää DHT22-mittaukset REST API:lle, palvelin tallentaa ja lähettää reaaliaikaisesti websocketin kautta frontendille, sekä webhook endpointin.

Sisältö
- `main.py` — MicroPython-laiteohjelma (ESP32/ESP8266)
- `server.js` — Node.js + Express + Socket.IO palvelin
- `package.json` — Node riippuvuudet
- `public/index.html` — Dashboard (Chart.js)
- `data.db` — SQLite (luodaan ajaessa)

Asennus & ajo (server)
1. Asenna Node.js.
2. `npm install`
3. `node server.js`
4. Avaa selaimessa `http://localhost:3000`.

Laitteen konfigurointi (main.py)
1. Aseta `SSID`, `PASSWORD` ja `SERVER_URL` (esim. `http://192.168.1.50:3000/data`) tiedostoon `main.py`.
2. Fläshää tiedosto ESP32:een tai käytä Wokwi-simulaattoria.
