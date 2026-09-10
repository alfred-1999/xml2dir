import threading
import time


def me(name):
    print(f"Hello", {name})

def worker_task(worker_name):
    print(f"Worker {worker_name} starting its shift...")
    # Simulate a heavy background task by sleeping for 5 seconds
    time.sleep(5)
    print(f"Worker {worker_name} finished!")

# Create 3 independent threads
thread1 = threading.Thread(target=worker_task, args=("A",))
thread2 = threading.Thread(target=worker_task, args=("B",))
thread3 = threading.Thread(target=worker_task, args=("C",))

# Start them all at the exact same time
thread1.start()
thread2.start()
thread3.start()

# Wait for all workers to finish before closing the program
thread1.join()
thread2.join()
thread3.join()

print("All threads finished. Factory closing down.")
