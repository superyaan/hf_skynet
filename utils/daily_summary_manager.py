# utils/daily_summary_manager.py
import json
import os
from datetime import datetime, date
from collections import defaultdict
from utils.logger import get_logger
from notifications.email_alert import EmailAlert

logger = get_logger(__name__)

# We'll store daily scan details per-day so they don't mix
# Example: reports/daily_2025-07-18.json
def _daily_file_path(day: date = None):
    if day is None:
        day = date.today()
    os.makedirs('reports', exist_ok=True)
    return os.path.join('reports', f"daily_{day.strftime('%Y-%m-%d')}.json")


def update_daily_stats(results, latency_threshold, ts: datetime = None):
    """
    Append a scan record containing only the devices that exceeded latency_threshold.
    Called after EACH scan cycle.
    """
    if ts is None:
        ts = datetime.now()

    # Filter high-latency devices from this scan
    high_latency_devices = [
        {
            "ip": d['ip'],
            "hostname": d.get('hostname', 'Unknown'),
            "mac": d.get('mac', 'Unknown'),
            "vendor": d.get('vendor', 'Unknown'),
            "latency": d.get('latency')
        }
        for d in results
        if d.get('latency') is not None and d['latency'] > latency_threshold
    ]

    # Nothing high latency this run? Still useful to track timestamp (optional).
    # To reduce file size, we skip storing empty scans.
    if not high_latency_devices:
        logger.info("Daily stats: no high-latency devices in this scan; skipping record append.")
        return

    # Load existing
    path = _daily_file_path()
    day_data = []
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                day_data = json.load(f)
        except json.JSONDecodeError:
            logger.warning(f"Corrupt daily summary file: {path}. Resetting.")
            day_data = []

    # Append this scan
    day_data.append({
        "timestamp": ts.strftime('%Y-%m-%d %H:%M:%S'),
        "high_latency": high_latency_devices
    })

    # Save
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(day_data, f, indent=4)
    logger.info(f"Daily stats updated with {len(high_latency_devices)} high-latency device(s).")


def send_daily_summary(config, day: date = None, reset_after_send: bool = True):
    """
    Aggregate all scans for a given day and send a single HTML email.
    """
    path = _daily_file_path(day)
    if not os.path.exists(path):
        logger.warning(f"No daily data found for {day or 'today'}: {path}")
        return

    try:
        with open(path, 'r', encoding='utf-8') as f:
            day_data = json.load(f)
    except json.JSONDecodeError:
        logger.error(f"Failed to read daily data file: {path}")
        return

    if not day_data:
        logger.info("Daily summary: no entries in file.")
        return

    # Aggregate
    # count high latency occurrences per IP
    agg = defaultdict(lambda: {
        "ip": None,
        "hostname": "Unknown",
        "mac": "Unknown",
        "vendor": "Unknown",
        "count": 0,
        "max_latency": 0,
        "first_seen": None,
        "last_seen": None,
    })

    total_scans_recorded = len(day_data)
    unique_ips_seen_today = set()

    for scan_entry in day_data:
        scan_ts = scan_entry.get("timestamp")
        for dev in scan_entry.get("high_latency", []):
            ip = dev.get('ip')
            if not ip:
                continue
            unique_ips_seen_today.add(ip)

            rec = agg[ip]
            rec["ip"] = ip
            rec["hostname"] = dev.get('hostname', rec["hostname"])
            rec["mac"] = dev.get('mac', rec["mac"])
            rec["vendor"] = dev.get('vendor', rec["vendor"])
            rec["count"] += 1

            lat = dev.get('latency') or 0
            if lat > rec["max_latency"]:
                rec["max_latency"] = lat

            # first/last seen timestamps
            if rec["first_seen"] is None or scan_ts < rec["first_seen"]:
                rec["first_seen"] = scan_ts
            if rec["last_seen"] is None or scan_ts > rec["last_seen"]:
                rec["last_seen"] = scan_ts

    devices_with_high_latency = len(agg)

    # Build HTML email
    day_str = (day or date.today()).strftime('%Y-%m-%d')
    html = f"""
    <h2>Skynet Daily Summary – {day_str}</h2>
    <p>This summary aggregates all scans for the day and shows devices that crossed the latency threshold at least once.</p>
    <div style="margin-bottom:16px;">
        <strong>Total Scans Recorded:</strong> {total_scans_recorded}<br>
        <strong>Devices Above Threshold (unique):</strong> {devices_with_high_latency}<br>
    </div>
    """

    # Detailed table
    html += """
    <table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;font-family:Arial;font-size:14px;">
        <thead style="background:#333;color:#fff;">
            <tr>
                <th>#</th>
                <th>IP</th>
                <th>Hostname</th>
                <th>MAC</th>
                <th>Vendor</th>
                <th>Times High</th>
                <th>Max Latency (ms)</th>
                <th>First Seen</th>
                <th>Last Seen</th>
            </tr>
        </thead>
        <tbody>
    """
    if agg:
        for idx, rec in enumerate(sorted(agg.values(), key=lambda r: r["count"], reverse=True), start=1):
            html += f"""
            <tr>
                <td>{idx}</td>
                <td>{rec['ip']}</td>
                <td>{rec['hostname']}</td>
                <td>{rec['mac']}</td>
                <td>{rec['vendor']}</td>
                <td>{rec['count']}</td>
                <td>{rec['max_latency']}</td>
                <td>{rec['first_seen']}</td>
                <td>{rec['last_seen']}</td>
            </tr>
            """
    else:
        html += """
            <tr><td colspan="9" style="text-align:center;">No high latency devices recorded today.</td></tr>
        """
    html += "</tbody></table>"
    html += "<p><i>Generated by Skynet © 2025 Hein+Fricke</i></p>"

    # Send email
    EmailAlert(config['email']).send_custom_email(
        subject=f"Skynet Daily Summary – {day_str}",
        html_content=html
    )

    logger.info(f"Daily summary email sent for {day_str}.")

    # Reset after send (archive instead of delete)
    if reset_after_send:
        archive_dir = os.path.join('reports', 'archive')
        os.makedirs(archive_dir, exist_ok=True)
        archive_path = os.path.join(archive_dir, f"daily_{day_str}.json")
        try:
            os.replace(path, archive_path)
            logger.info(f"Daily summary archived: {archive_path}")
        except Exception as e:
            logger.error(f"Failed to archive daily summary file: {e}")