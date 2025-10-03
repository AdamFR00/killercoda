from flask import Flask
import math
import time
import os

app = Flask(__name__)

stress_cycles = 0


@app.route("/")
def hello():
    container_name = os.getenv("HOSTNAME", "Unknown Container")
    return f"Flask app running in container: {container_name}! Navigate to /cpu-stress (heavy) or /mem-stress (memory) to generate load."


@app.route("/cpu-stress")
def cpu_stress():
    global stress_cycles
    stress_cycles += 1

    start_time = time.time()
    duration = 20
    end_time = start_time + duration

    iterations_per_second = 100000

    while time.time() < end_time:
        x = 1.23456789
        y = 9.87654321

        for _ in range(iterations_per_second):
            x = math.sin(x * y) * math.cos(y / x)
            y = math.tan(x + y) + math.sqrt(abs(x * y))
            z = math.pow(x, y) * math.log(abs(y + 0.0001))

            if time.time() >= end_time:
                break

        if time.time() >= end_time:
            break

    return f"CPU stress test complete! Burned ~{duration}s of CPU. Total stress cycles: {stress_cycles}."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
