from flask import Flask
import math
import time

app = Flask(__name__)


@app.route("/")
def hello():
    return "Flask app is running!"


@app.route("/cpu-stress")
def cpu_stress():
    # Burn CPU cycles for ~5 seconds
    end_time = time.time() + 5
    while time.time() < end_time:
        math.sqrt(12345 * 54321)
    return "CPU stress test complete! Burned ~5s of CPU."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
