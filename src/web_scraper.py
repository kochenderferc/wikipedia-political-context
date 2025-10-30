import subprocess
import time
import os

testing_languages=[
    'ko',  # Korean
    'id',  # Indonesian
    'vi',  # Vietnamese
    'cs',  # Czech
    'fi',  # Finnish
    'no',  # Norwegian (Bokmål)
    'hu',  # Hungarian
    'ro',  # Romanian
    'tr',  # Turkish
    'he',  # Hebrew
    'th',  # Thai
    'da',  # Danish
    'el',  # Greek
    'hi',  # Hindi
    'bn',  # Bengali
]


languages_that_work = [
    'en', # English
    'es', # Spanish
    'ru', # Russian
    'hu'  # Hungarian
]

languages_that_dont = [
    'ko',  # Korean
    'id',  # Indonesian
    'vi',  # Vietnamese
    'cs',  # Czech
    'fi',  # Finnish
    'no',  # Norwegian (Bokmål)
    'hu',  # Hungarian
    'ro',  # Romanian
    'tr',  # Turkish
    'he',  # Hebrew
    'th',  # Thai
    'da',  # Danish
    'el',  # Greek
    'hi',  # Hindi
    'bn',  # Bengali
    'fr',  # French
    'de',  # German
    'ja',  # Japanese
    'pt',  # Portuguese
]

# Define paths
base_path = os.path.dirname(__file__)
streaming_script = os.path.join(base_path, "data_streaming.py")
batching_script = os.path.join(base_path, "data_batching.py")
process_list = []

try:
    # Start data_streaming.py/data_batching.py process for each language
    for language in testing_languages:
        # Starting a process for each language being streamed
        print(f"Streaming {language} Data")
        process = subprocess.Popen(["python3", streaming_script, language])
        process_list.append(process)

        # Run batching concurrently using subprocess.Popen instead of os.system
        print(f"Batching {language} Data")
        batch_process = subprocess.Popen(["python3", batching_script, language])
        process_list.append(batch_process)

    print("All processes started. Press Ctrl+C to stop.")
    # Keep the script running until user stops it with Ctrl+c
    while True:
        time.sleep(1)

except KeyboardInterrupt:

    process_num = 1
    for process in process_list:
        print(f"\t{process_num}.) Terminating Process PID={process.pid}")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print(f"Process PID={process.pid} did not exit, forcing kill.")
            process.kill()
        process_num += 1
    print("All processes terminated.")

except Exception as e:
    print("Something Broke", e)
