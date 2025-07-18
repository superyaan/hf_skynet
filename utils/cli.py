# utils/cli.py
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Skynet | Hein+Fricke © 2025")
    parser.add_argument('--ip', help='Scan a single IP address')
    parser.add_argument('--range', help='Override IP range/subnet (e.g. 192.168.1.0/24)')
    parser.add_argument('--format', choices=['html', 'csv', 'json'], help='Output report format')
    parser.add_argument('--self', dest='self_scan', action='store_true', help='Scan only this machine')
    parser.add_argument('--weekly-summary', action='store_true', help='Send weekly summary email')
    return parser.parse_args()

def apply_overrides(config, args):
    if args.range:
        config['ip_range'] = args.range
    elif args.ip:
        config['ip_range'] = f"{args.ip}/32"
    elif args.self_scan:
        config['ip_range'] = ""  # auto-detect in scanner
    if args.format:
        config['report_format'] = args.format
    return config