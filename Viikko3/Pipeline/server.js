const express = require("express");
const bodyParser = require("body-parser");
const app = express();
const port = 3000;

app.use(bodyParser.json());

let dataLog = [];

// POST endpointti
app.post("/data", (req, res) => {
  const { temperature, humidity } = req.body;
  if (temperature !== undefined && humidity !== undefined) {
    const entry = {
      temperature,
      humidity,
      time: new Date().toLocaleString(),
    };
    dataLog.push(entry);

    if (dataLog.length > 100) {
      dataLog.shift();
    }

    console.log("Received:", entry);
    res.sendStatus(200);
  } else {
    res.sendStatus(400);
  }
});

// lista selaimes
app.get("/", (req, res) => {
  let html = "<h1>Sensor Data</h1><ul>";
  dataLog.forEach((d) => {
    html += `<li>${d.time} - Temp: ${d.temperature}°C, Hum: ${d.humidity}%</li>`;
  });
  html += "</ul>";
  res.send(html);
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
