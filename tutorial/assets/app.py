from flask import Flask
from multiprocessing import Pool, cpu_count
import math
import time

app = Flask(__name__)


@app.route("/")
def hello():
    return "Flask app is running!"

def work(x):
    return sum(math.sqrt(i)*i for i in range(1000000))

@app.route("/cpu-stress")
def cpu_stress():
    # Burn CPU cycles for ~5 seconds
    with Pool(cpu_count()) as p: 
        results = p.map(work, range(cpu_count()))

    total = sum(results)
    return f"Result from cpu stress: {total}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
