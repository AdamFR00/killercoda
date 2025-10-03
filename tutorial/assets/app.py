from flask import Flask
import math
import time
import os
import multiprocessing  # Import multiprocessing
import threading  # Import threading for the /cpu-stress endpoint if needed

app = Flask(__name__)

stress_cycles = 0
# List to hold worker processes
worker_processes = []
# Event to signal workers to stop
stop_event = threading.Event()  # Use threading.Event for graceful shutdown


# Define the CPU intensive task for worker processes
def cpu_intensive_task(iterations_per_second):
    x = 1.0
    y = 2.0
    while not stop_event.is_set():  # Loop until the stop_event is set
        # Perform a series of intensive mathematical operations
        x = math.sin(x * y + 0.1) * math.cos(y / (x + 0.0001))
        y = math.tan(x + y) + math.sqrt(abs(x * y) + 1e-6)

        # Do a lot of these calculations to burn CPU
        for _ in range(iterations_per_second // 4):  # Divide iterations by num_workers
            a = 1.23456789
            b = 9.87654321
            a = math.sin(a * b) * math.cos(b / (a + 0.0001))
            b = math.tan(a + b) + math.sqrt(abs(a * b) + 1e-6)
            # If we have more iterations to do, continue


# Function to manage worker processes
def start_cpu_burners(num_workers, iterations_per_second):
    global worker_processes
    global stop_event

    # Clear previous workers and stop event if they exist
    if worker_processes:
        stop_event.set()  # Signal existing workers to stop
        for p in worker_processes:
            p.join(timeout=2)  # Give them a moment to finish
            if p.is_alive():
                p.terminate()  # Force terminate if they don't stop
        worker_processes = []
        stop_event.clear()  # Reset the event for the new run

    # Start new worker processes
    for _ in range(num_workers):
        p = multiprocessing.Process(
            target=cpu_intensive_task, args=(iterations_per_second,)
        )
        p.start()
        worker_processes.append(p)
    print(f"Started {num_workers} CPU burner processes.")


# Function to stop worker processes
def stop_cpu_burners():
    global worker_processes
    global stop_event

    if worker_processes:
        print("Signaling CPU burners to stop...")
        stop_event.set()  # Signal all workers to stop
        for p in worker_processes:
            p.join(timeout=5)  # Wait for them to finish gracefully
            if p.is_alive():
                print(f"Worker process {p.pid} did not stop gracefully, terminating.")
                p.terminate()  # Force terminate if they don't stop
        worker_processes = []
        stop_event.clear()  # Reset the event
        print("All CPU burner processes stopped.")


@app.route("/")
def hello():
    container_name = os.getenv("HOSTNAME", "Unknown Container")
    return f"Flask app running in container: {container_name}! Navigate to /cpu-stress to generate load."


@app.route("/cpu-stress")
def cpu_stress():
    global stress_cycles
    stress_cycles += 1

    start_time = time.time()
    duration = 20  # seconds for the stress to run

    # Determine number of workers based on available cores
    num_workers = multiprocessing.cpu_count()
    if num_workers is None or num_workers == 0:  # Fallback if cpu_count fails
        num_workers = 4

    # Total calculations to aim for over the duration
    # More iterations = more load. Distribute this across workers.
    total_iterations = (
        50000000  # Aim for 50 million calculations *per worker* over the duration
    )

    print(
        f"Starting CPU stress for ~{duration}s with {num_workers} workers, ~{total_iterations} iterations per worker."
    )

    # Start the CPU burner processes
    start_cpu_burners(num_workers, total_iterations)

    # Let the workers run for the specified duration
    time.sleep(duration)

    # Stop the CPU burner processes
    stop_cpu_burners()

    return f"CPU stress test complete! Ran for ~{duration}s. Total stress cycles: {stress_cycles}. Utilized {num_workers} cores."


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
    # It's good practice to set up the multiprocessing start method, especially on macOS/Windows.
    # 'fork' is default on Unix and generally faster for this purpose.
    if os.name == "posix":
        multiprocessing.set_start_method("fork", force=True)

    app.run(host="0.0.0.0", port=5000)
