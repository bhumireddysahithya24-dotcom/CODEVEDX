import psutil
import time

# List of suspicious keywords
suspicious_keywords = [
    "keylogger",
    "hook",
    "spy",
    "logger",
    "record"
]

print("Starting Keylogger Detection System...\n")

while True:

    suspicious_found = False

    for process in psutil.process_iter(['pid', 'name']):

        try:
            process_name = process.info['name'].lower()

            for keyword in suspicious_keywords:

                if keyword in process_name:

                    suspicious_found = True

                    print("ALERT: Suspicious Process Detected!")
                    print("Process Name:", process.info['name'])
                    print("PID:", process.info['pid'])
                    print("-" * 40)

        except:
            pass

    if not suspicious_found:
        print("System Safe: No suspicious processes detected.")

    print("\nScanning again in 10 seconds...\n")

    time.sleep(10)
