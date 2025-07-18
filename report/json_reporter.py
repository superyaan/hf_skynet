import os
import json
from datetime import datetime

class JSONReporter:
    def __init__(self):
        os.makedirs("reports", exist_ok=True)

    def generate(self, results, log_file=None):  # Accept log_file
        filename = f"reports/report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
        return filename
