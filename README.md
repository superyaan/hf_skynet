# Skynet©: Advanced Network Monitoring & Reporting System

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

Skynet is a modular, Python-based tool developed for **Hein+Fricke** to monitor network health and generate actionable reports. It supports real-time alerts, beautiful HTML dashboards, and weekly summaries – all following **SOLID principles** and **OOP design**.

---

## 🚀 Features

### Core Functionality
- **Auto-detect or scan custom IP ranges**
- **Multi-threaded scanning** for optimal performance
- **Comprehensive device discovery** including:
  - IP Address
  - Hostname
  - MAC Address + Vendor lookup
  - Latency measurement (ms)
  - Open Ports (configurable)
- **Automated Scheduling**:
  - Use `run_scheduler.py` to auto-run the scan every 15 minutes (or custom interval)
  - Leverages Python's `schedule` library

### Reporting & Alerts
- **Professional reports** in multiple formats (HTML, CSV, JSON)
- **Email alerts** for unreachable/high-latency devices (single consolidated mail)
- **Weekly summary email** with historical statistics
- **Centralized logging** per run with timestamped files
- **CLI overrides** for flexible usage
- **Secure configuration** via `config.json`

---

## 📂 Project Structure

```
hf_skynet/
├── README.md
├── main.py                     # Entry point
├── run_scheduler.py            # Scheduler script to run main app periodically
├── config.json                 # Configuration (IP range, email settings)
├── requirements.txt
│
├── app/
│   └── app.py                  # Orchestrates scan → report → alerts → summary
│
├── utils/
│   ├── cli.py                  # CLI argument parser
│   ├── config_loader.py        # Config file loader
│   ├── daily_summary_manager.py# Daily Summary Logic
│   ├── logger.py               # Logging setup
│   └── summary_manager.py      # Weekly summary logic
│
├── scanner/
│   └── network_scanner.py      # Scanning logic
│
├── report/
│   ├── html_reporter.py        # HTML report generation
│   ├── csv_reporter.py         # CSV report
│   ├── json_reporter.py        # JSON report
│   └── report_factory.py       # Factory to select report type
│
├── notifications/
│   ├── email_alert.py          # Email sending logic
│   └── alert_manager.py        # Consolidated alert handling
│
├── reports/                    # Generated reports
│   ├── report_YYYY-MM-DD_HH-MM.html
│   └── weekly_summary.json
│
├── logs/                       # Timestamped log files
│   └── scan_YYYY-MM-DD_HH-MM-SS.log
│
└── mac-vendors.txt             # MAC vendor reference
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone & Navigate
```bash
git clone https://github.com/superyaan/hf_skynet.git
cd hf_skynet
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3️⃣ Install Requirements
```bash
pip install -r requirements.txt
```

---

## 🔐 Configuration

Edit `config.json` to customize your network monitoring setup:

```json
{
  "ip_range": "",
  "latency_threshold": 200,
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender": "your-email@gmail.com",
    "receiver": "receiver-email@gmail.com",
    "username": "your-email@gmail.com",
    "password": "your-app-password"
  },
  "report_format": "html",
  "ports_to_check": [22, 80, 443, 3389]
}
```

### Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ip_range` | Network range to scan | `192.168.1.0/24` |
| `latency_threshold` | Alert threshold in ms | `200` |
| `email.smtp_server` | SMTP server address | `smtp.gmail.com` |
| `email.smtp_port` | SMTP port | `587` |
| `report_format` | Output format | `html` |
| `ports_to_check` | Ports to scan | `[22, 80, 443, 3389]` |

---

## ⚡ Usage

### Basic Network Scan
```bash
python main.py
```

### CLI Options

| Command | Description |
|---------|-------------|
| `python main.py --ip 192.168.1.10` | Scan single IP |
| `python main.py --range 10.3.1.0/24` | Scan custom range |
| `python main.py --self` | Self scan |
| `python main.py --format csv` | Generate CSV report |
| `python main.py --weekly-summary` | Send weekly summary email |

### Advanced Usage Examples

```bash
# Scan specific subnet with CSV output
python main.py --range 10.0.0.0/24 --format csv

# Quick self-scan for troubleshooting
python main.py --self

# Generate weekly summary
python main.py --weekly-summary
```

---

## 📧 Email Features

### Alert System
- **Single consolidated alert email** containing:
  - Device table (IP, Hostname, MAC, Vendor, Status, Latency, Open Ports)
  - Attached latest HTML report
  - Summary of issues found

### Weekly Summary
- **Automated weekly summary email** with:
  - Historical statistics
  - Trend analysis
  - Performance metrics
  - Device availability reports

---

## 🗂 Logs & Reports

### Logging
Each run creates a timestamped log file:
```
logs/scan_YYYY-MM-DD_HH-MM-SS.log
```

The HTML report includes a clickable link to the corresponding log file for easy troubleshooting.

### Report Formats
- **HTML**: Beautiful, interactive dashboard
- **CSV**: Spreadsheet-compatible format
- **JSON**: Machine-readable format for integration

---

## 🔧 System Requirements

- **Python 3.8+**
- **Internet access** for email sending and vendor lookup
- **Admin privileges** for ARP operations (on some operating systems)

### Dependencies
All dependencies are listed in `requirements.txt`:
```txt
requests>=2.25.1
psutil>=5.8.0
netifaces>=0.11.0
```

---

## 🚨 Troubleshooting

### Common Issues

**Permission Denied (ARP)**
- Run with administrator/sudo privileges
- Check firewall settings

**Email Not Sending**
- Verify SMTP credentials
- Enable "Less secure app access" for Gmail
- Use app-specific passwords

**Slow Scanning**
- Reduce IP range size
- Adjust thread count in scanner
- Check network connectivity

---

## 🛠 Development

### Architecture
Skynet follows **SOLID principles** and uses **Object-Oriented Programming** for maintainability:

- **Single Responsibility**: Each module has one clear purpose
- **Open/Closed**: Extensible without modifying existing code
- **Liskov Substitution**: Interchangeable components
- **Interface Segregation**: Focused interfaces
- **Dependency Inversion**: Abstract dependencies

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## (NEW UPDATE)
## 📊 Daily Summary Feature

Skynet now includes a **Daily High Latency Summary** feature for comprehensive 24-hour monitoring and reporting.

### 🎯 What It Does

- **Continuous Monitoring**: Tracks all devices across **96 scans per day** (every 15 minutes)
- **Intelligent Analysis**: Identifies devices that crossed the **latency threshold** at least once
- **Comprehensive Aggregation**:
  - Total scans performed during the day
  - Unique devices detected
  - Devices with high latency incidents
  - Frequency count of high latency events per device
  - Maximum latency observed per device
  - First seen / Last seen timestamps for each device

### 📧 Daily Summary Email

Automated daily reporting delivered once per day (typically at 23:59 or on custom schedule):

- **Summary Dashboard**: Professional HTML table of all high-latency devices
- **Event Analytics**: Count of high-latency incidents per device
- **Performance Metrics**: Maximum latency recorded per device
- **Historical Context**: Timeline of device availability

### 🚀 How To Use

#### 1️⃣ Continuous Monitoring
Run automated scans every 15 minutes using the scheduler:
```bash
python run_scheduler.py
```

#### 2️⃣ Generate Daily Summary
At the end of each day, send the comprehensive summary:
```bash
python main.py --daily-summary
```
*This can be automated via cron (Linux/macOS) or Task Scheduler (Windows)*

### 🔧 Automation Setup

#### Linux/macOS (Crontab)
```bash
# Add to crontab for daily summary at 23:59
59 23 * * * /path/to/venv/bin/python /path/to/skynet/main.py --daily-summary
```

#### Windows (Task Scheduler)
Create a daily task running at 23:59:
```cmd
Program: python
Arguments: main.py --daily-summary
Start in: C:\path\to\skynet\
```

### 📁 Data Storage

Daily summaries are stored in structured JSON format:
```
reports/daily_YYYY-MM-DD.json
```

**What the Daily Summary Does:**
1. Aggregates data from all 96 daily scan reports
2. Generates HTML email with detailed high-latency device analysis  
3. Archives daily summary JSON for historical reference
4. Provides actionable insights for network performance optimization

---

## 👨‍💻 Author

**Sufiyaan Rahi**  
*Intern @ Hein+Fricke GmbH*  
*rahis@duck.com*

For questions or support, please contact: [rahis@duck.com](mailto:rahis@duck.com)

---

## 🔗 Quick Links

- [Installation Guide](#️-setup-instructions)
- [Configuration](#-configuration)
- [Usage Examples](#-usage)
- [Troubleshooting](#-troubleshooting)
- [Contributing Guidelines](#-development)