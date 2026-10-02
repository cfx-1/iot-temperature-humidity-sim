from flask import Flask, jsonify, render_template_string
import random
from datetime import datetime

app = Flask(__name__)

history = []

def get_latest_data():
    temperature = round(random.uniform(18.0, 32.0), 1)
    humidity = round(random.uniform(40.0, 80.0), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "temperature": temperature,
        "humidity": humidity,
        "time": timestamp
    }
    history.append(data)
    if len(history) > 20:
        history.pop(0)
    return data

@app.route("/")
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>模拟物联网温湿度监控</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial; text-align: center; margin-top: 50px; background-color: #f5f5f5; }
            .card { background: white; display: inline-block; padding: 30px 50px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            .data { font-size: 22px; margin: 18px 0; }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>模拟物联网温湿度实时监控</h1>
            <div class="data">
                <p>当前温度：<span id="temp">--</span> °C</p>
                <p>当前湿度：<span id="hum">--</span> %</p>
                <p>更新时间：<span id="time">--</span></p>
            </div>
        </div>
        <script>
            function updateData() {
                fetch('/api/data')
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById('temp').innerText = data.temperature;
                        document.getElementById('hum').innerText = data.humidity;
                        document.getElementById('time').innerText = data.time;
                    });
            }
            setInterval(updateData, 2000);
            updateData();
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/api/data")
def api_data():
    return jsonify(get_latest_data())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)