import subprocess
import time
import os


"""
de - German - https://de.wikipedia.org/w/api.php
fr - French - https://fr.wikipedia.org/w/api.php
es - Spanish - https://es.wikipedia.org/w/api.php
ja - Japanese - https://ja.wikipedia.org/w/api.php
ru - Russian - https://ru.wikipedia.org/w/api.php
pt - Portuguese - https://pt.wikipedia.org/w/api.php
"""
languages = ['en', 'de', 'fr', 'es', 'ja', 'ru', 'pt']

# Define paths
base_path = os.path.dirname(__file__)
streaming_script = os.path.join(base_path, "data_streaming.py")
batching_script = os.path.join(base_path, "data_batching.py")
# visualizer_script = os.path.join(base_path, "data_visualizer.py")

process_list = []

try:
    # Start data_streaming.py/data_batching.py process for each language
    for language in languages:

        print(f"Streaming {language} Data")

        # Starting a process for each language being streamed
        process = subprocess.Popen(["python", streaming_script, language])
        process_list.append(process)

        # Run batching concurrently using subprocess.Popen instead of os.system
        print(f"Batching {language} Data")
        batch_process = subprocess.Popen(["python3", batching_script, language])
        process_list.append(batch_process)

        # os.system('cls' if os.name == 'nt' else 'clear')

    ### NEW CODE START
    print("All processes started. Press Ctrl+C to stop.")
    # Keep the script running until user stops it with Ctrl+c
    while True:
        time.sleep(1)


except KeyboardInterrupt:
    for process in process_list:
        print(f"Terminating Process PID={process.pid}")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print(f"Process PID={process.pid} did not exit, forcing kill.")
            process.kill()
    print("All processes terminated.")


except Exception as e:
    print("Something Broke", e)
