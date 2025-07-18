# report/report_factory.py
from report.html_reporter import HTMLReporter
from report.csv_reporter import CSVReporter
from report.json_reporter import JSONReporter
from utils.logger import get_logger

logger = get_logger(__name__)

def get_reporter(fmt: str):
    fmt = (fmt or 'html').lower()
    if fmt == 'html':
        return HTMLReporter()
    if fmt == 'csv':
        return CSVReporter()
    if fmt == 'json':
        return JSONReporter()
    logger.warning(f"Unsupported report format '{fmt}', defaulting to HTML.")
    return HTMLReporter()