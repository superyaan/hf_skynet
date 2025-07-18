import csv
import os
from datetime import datetime

class CSVReporter:
    def __init__(self):
        os.makedirs("reports", exist_ok=True)

    def generate(self, results, log_file=None):  # Added log_file arg
        filename = f"reports/report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        fields = ["ip", "mac", "vendor", "hostname", "status", "latency", "open_ports"]

        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()

            for device in results:
                writer.writerow({
                    "ip": device["ip"],
                    "mac": device["mac"],
                    "vendor": device["vendor"],
                    "hostname": device["hostname"],
                    "status": device["status"],
                    "latency": device["latency"],
                    "open_ports": ", ".join(map(str, device["open_ports"])) if device["open_ports"] else "None"
                })

        return filename  # Return file path