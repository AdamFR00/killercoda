from flask import Flask
import math
import time
import os

app = Flask(__name__)

stress_cycles = 0
memory_chunks = []  # List to hold allocated memory


@app.route("/")
def hello():
    container_name = os.getenv("HOSTNAME", "Unknown Container")
    return f"Flask app running in container: {container_name}! Navigate to /cpu-stress to generate load."


@app.route("/cpu-stress")
def cpu_stress():
    global stress_cycles
    stress_cycles += 1

    start_time = time.time()
    duration = 20
    end_time = start_time + duration

    # Number of calculations to perform per second
    # Adjust this value for more or less CPU load
    calculations_per_second = 200000  # High number of operations

    # Initialize variables outside the inner loop
    a = 1.0
    b = 2.0

    while time.time() < end_time:
        for _ in range(calculations_per_second):
            # Perform a series of intensive mathematical operations
            # Focus on operations that are CPU bound and avoid edge cases for log/pow if possible

            # Sine and cosine of sums/differences, square roots, multiplications
            a = math.sin(a * b + 0.1) * math.cos(
                b / (a + 0.0001)
            )  # Added small epsilon to avoid division by zero
            b = math.tan(a + b) + math.sqrt(
                abs(a * b) + 1e-6
            )  # Added epsilon to sqrt input and abs

            # Removed log/pow for simplicity and error avoidance, replaced with more trig/math
            # If you want a log-like behavior, you could consider something like:
            # a = math.log10(abs(a) + 1.0) # log10 of a positive number always > 0

            if time.time() >= end_time:
                break

        if time.time() >= end_time:
            break

    return f"CPU stress test complete! Burned ~{duration}s of CPU. Total stress cycles: {stress_cycles}."


@app.route("/mem-stress")
def mem_stress():
    global stress_cycles  # Reuse cycle counter or create a new one if you prefer
    stress_cycles += 1

    start_time = time.time()
    duration = 25  # seconds
    end_time = start_time + duration

    # Allocate memory in chunks
    chunk_size_mb = 50  # Allocate 50MB per chunk
    num_chunks_to_allocate = 20  # Try to allocate ~1GB total

    try:
        for i in range(num_chunks_to_allocate):
            if time.time() >= end_time:
                break

            # Allocate a chunk of memory. Fill it with some data to ensure it's used.
            # This consumes significant RAM.
            new_chunk = [0.0] * (
                chunk_size_mb * 1024 * 1024 // 8
            )  # Approx bytes for float64
            for j in range(len(new_chunk)):
                new_chunk[j] = math.sin(j * i) * math.cos(i / (j + 1e-6))

            memory_chunks.append(new_chunk)

            # Small delay to not completely freeze the web server,
            # but still consume memory rapidly.
            time.sleep(0.5)

        return f"Memory stress test complete! Allocated ~{len(memory_chunks) * chunk_size_mb}MB of memory. Total stress cycles: {stress_cycles}."

    except MemoryError:
        return "Memory stress test failed: Ran out of memory!", 500
    finally:
        # Clean up some memory if the process is ending, but keep most of it
        # to observe the high usage. For a true test, you might want to leave
        # it allocated until the container is stopped/restarted.
        # In a real scenario, you'd have to consider how to stop this gracefully.
        pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
