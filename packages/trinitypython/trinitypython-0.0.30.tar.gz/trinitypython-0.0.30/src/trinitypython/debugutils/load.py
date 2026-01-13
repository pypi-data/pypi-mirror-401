import time
import multiprocessing
import os
import sys

def cpu_worker(target_percent, duration):
    end = time.time() + duration
    interval = 0.1

    busy = interval * (target_percent / 100)
    idle = interval - busy

    while time.time() < end:
        start = time.time()
        while (time.time() - start) < busy:
            pass
        time.sleep(idle)

def allocate_memory(mb):
    size = mb * 1024 * 1024
    print(f"Allocating {mb} MB RAM (visible in Task Manager)...")

    # Allocate and touch memory to force commit
    block = bytearray(size)
    for i in range(0, size, 4096):  # touch each page
        block[i] = 1

    return block

def main(cpu_target, ram_mb, duration_secs):
    try:
        # Allocate memory in main process (will be visible in Task Manager)
        mem = allocate_memory(ram_mb)

        cores = os.cpu_count()
        print(f"Detected {cores} logical cores")
        print(f"Spawning {cores} worker processes for accurate CPU load")

        processes = []
        for _ in range(cores):
            p = multiprocessing.Process(
                target=cpu_worker,
                args=(cpu_target, duration_secs)
            )
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        print("Done. Resources released.")

    except KeyboardInterrupt:
        print("\nStopped by user.")
        sys.exit(0)

def simulate_load(cpu_target, ram_mb, duration_secs):
    multiprocessing.freeze_support()  # important for Windows
    main(cpu_target, ram_mb, duration_secs)
