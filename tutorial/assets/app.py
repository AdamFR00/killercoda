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
