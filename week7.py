import subprocess
import time
import os
import signal

# Define paths
base_path = os.path.join(os.path.dirname(__file__), "src")
streaming_script = os.path.join(base_path, "data_streaming.py")
visualizer_script = os.path.join(base_path, "data_visualizer.py")

# Step 1: Start data_streaming.py
print("Starting data_streaming.py...")
process = subprocess.Popen(["python", streaming_script])

# Step 2: Wait for 10 seconds
time.sleep(10)

# Step 3: Send KeyboardInterrupt (SIGINT)
print("Stopping data_streaming.py with KeyboardInterrupt...")
process.send_signal(signal.SIGINT)
process.wait()

os.system('cls' if os.name == 'nt' else 'clear')

# Step 4: Run data_visualizer.py
print("Running data_visualizer.py...")
subprocess.run(["python", visualizer_script])
