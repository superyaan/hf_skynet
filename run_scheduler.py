import schedule
import time
import subprocess

def run_scan():
    print("Starting scheduled network scan...")
    subprocess.run(["python3", "main.py"])  # Runs your existing script

# Schedule job every 15 minutes
schedule.every(15).minutes.do(run_scan)

print("Scheduler started. Running scan every 15 minutes...")
while True:
    schedule.run_pending()
    time.sleep(10)
