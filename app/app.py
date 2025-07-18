import os
from scanner.network_scanner import NetworkScanner
from notifications.alert_manager import build_alerts, send_consolidated_alerts
from report.report_factory import get_reporter
from utils.summary_manager import update_weekly_summary
from utils.logger import get_logger

logger = get_logger(__name__)

def run_scan_cycle(config):
    logger.info("Starting Network Monitor App")

    # 1. Scan
    scanner = NetworkScanner(config)
    results = scanner.scan()

    # 2. Report
    reporter = get_reporter(config.get('report_format', 'html'))
    # You may want to dynamically pick today's log file; hardcode or extend logger to expose path
    log_file = _get_latest_log_file()
    report_file = reporter.generate(results, log_file=logger.log_file)
    logger.info(f"Report generated: {report_file}")

    # 3. Alerts (unreachable OR latency > threshold)
    alerts = build_alerts(results, config['latency_threshold'])
    if alerts:
        send_consolidated_alerts(alerts, config['email'], attachment=report_file)
        logger.info(f"Sent consolidated alert email for {len(alerts)} issues.")
    else:
        logger.info("No alert conditions detected.")

    # 4. Update weekly summary
    update_weekly_summary(results)
    logger.info("Weekly summary data updated.")
    logger.info("Scan cycle complete.")


def _get_latest_log_file():
    """Best-effort: return latest file in logs/, else None."""
    logs_dir = "logs"
    if not os.path.isdir(logs_dir):
        return None
    files = [os.path.join(logs_dir, f) for f in os.listdir(logs_dir) if f.endswith(".log")]
    return max(files, key=os.path.getmtime) if files else None