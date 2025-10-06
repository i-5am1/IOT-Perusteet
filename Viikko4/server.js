const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const bodyParser = require('body-parser');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

app.use(cors());
app.use(bodyParser.json());

const db = new sqlite3.Database('./data.db');
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    ts INTEGER,
    temperature REAL,
    humidity REAL
  )`);
});

app.post('/data', (req, res) => {
  const { device_id = 'unknown', ts = Date.now(), temperature, humidity } = req.body;
  if (temperature == null || humidity == null) {
    return res.status(400).json({ error: 'temperature and humidity required' });
  }
  const stmt = db.prepare("INSERT INTO readings (device_id, ts, temperature, humidity) VALUES (?, ?, ?, ?)");
  stmt.run(device_id, ts, temperature, humidity, function(err) {
    if (err) {
      console.error(err);
      return res.status(500).json({ ok: false });
    }
    const row = { id: this.lastID, device_id, ts, temperature, humidity };
    io.emit('reading', row);
    res.json({ ok: true, row });
  });
});

app.post('/webhook', (req, res) => {
  const payload = req.body;
  io.emit('webhook', payload);
  res.json({ ok: true });
});

app.get('/readings', (req, res) => {
  const { device, limit = 200 } = req.query;
  const q = device ? "SELECT * FROM readings WHERE device_id = ? ORDER BY ts DESC LIMIT ?" :
                     "SELECT * FROM readings ORDER BY ts DESC LIMIT ?";
  const params = device ? [device, limit] : [limit];
  db.all(q, params, (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows.reverse());
  });
});

app.use(express.static('public'));

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server listening on ${PORT}`));
