import subprocess
import platform
import socket
import ipaddress
import netifaces
import threading
import re
from utils.logger import get_logger

logger = get_logger(__name__)

class NetworkScanner:
    def __init__(self, config):
        self.ports = config.get("ports_to_check", [])
        self.results = []
        self.lock = threading.Lock()

        try:
            self.subnet = config.get("ip_range") or self.get_local_subnet()
        except Exception as e:
            raise RuntimeError(f"Could not determine IP range: {e}")

        self.ip_range = [str(ip) for ip in ipaddress.IPv4Network(self.subnet, strict=False)]

    def get_local_subnet(self):
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                ip_info = addrs[netifaces.AF_INET][0]
                ip_addr = ip_info.get('addr')
                netmask = ip_info.get('netmask')

                if not ip_addr or ip_addr.startswith(("127.", "169.254")):
                    continue

                network = ipaddress.IPv4Network(f"{ip_addr}/{netmask}", strict=False)
                return str(network)

        raise RuntimeError("Unable to auto-detect subnet.")

    def ping_device(self, ip):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', str(ip)]

        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            if "ttl=" in output.lower() or "time=" in output.lower():
                latency = None
                if "time=" in output:
                    try:
                        latency = float(output.split("time=")[-1].split("ms")[0].strip())
                    except:
                        latency = None
                return "Reachable", latency
            else:
                return "Unreachable", None
        except subprocess.CalledProcessError:
            return "Unreachable", None

    def get_hostname(self, ip):
        try:
            # Method 1: Reverse DNS
            hostname = socket.gethostbyaddr(ip)[0]
            if hostname and hostname != ip:
                return hostname
        except Exception:
            pass

        # Method 2: NetBIOS via nmblookup
        try:
            output = subprocess.check_output(['nmblookup', '-A', ip], stderr=subprocess.DEVNULL).decode()
            for line in output.splitlines():
                if '<00>' in line and 'UNIQUE' in line:
                    return line.strip().split()[0]
        except Exception:
            pass

        # Method 3: Try extracting from ping output (some devices show hostnames in parentheses)
        try:
            output = subprocess.check_output(['ping', '-c', '1', ip], stderr=subprocess.DEVNULL).decode()
            if '(' in output and ')' in output:
                # Example: PING my-device (192.168.1.10) → extract my-device
                ping_line = output.splitlines()[0]
                candidate = ping_line.split('(')[0].replace('PING', '').strip()
                if candidate and candidate != ip and not candidate.isnumeric():
                    return candidate
        except Exception:
            pass

        return "Unknown"

    def get_mac_address(self, ip):
        try:
            # Ensure ARP table is populated
            subprocess.call(['ping', '-c', '1', ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Linux/macOS: ip neigh
            if platform.system().lower() in ['linux', 'darwin']:
                output = subprocess.check_output(['ip', 'neigh', 'show', ip], universal_newlines=True)
                match = re.search(r'lladdr\s+([0-9a-fA-F:]{17})', output)
                if match:
                    return match.group(1)

                # Fallback to arp -n
                output = subprocess.check_output(['arp', '-n', ip], universal_newlines=True)
                match = re.search(r'(([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2})', output)
                if match:
                    return match.group(1)

            # Windows: arp -a
            elif platform.system().lower() == 'windows':
                output = subprocess.check_output(['arp', '-a'], universal_newlines=True)
                pattern = rf"{ip}\s+([-\w]+)"
                match = re.search(pattern, output)
                if match:
                    return match.group(1)

        except Exception as e:
            logger.warning(f"MAC fetch failed for {ip}: {e}")

        return "Unknown"
    
    def lookup_mac_vendor(self, mac, oui_file="mac-vendors.txt"):
        if not mac or mac == "Unknown":
            return "Unknown"

        mac_prefix = mac.upper().replace(":", "-")[0:8]

        try:
            with open(oui_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if mac_prefix in line:
                        return line.split('        ')[-1].strip()
        except Exception as e:
            logger.warning(f"Vendor lookup failed for MAC {mac}: {e}")

        return "Unknown"

    def check_ports(self, ip):
        open_ports = []
        for port in self.ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.5)
                    result = s.connect_ex((str(ip), port))
                    if result == 0:
                        open_ports.append(port)
            except Exception:
                continue
        return open_ports

    def scan_ip(self, ip):
        status, latency = self.ping_device(ip)
        hostname = self.get_hostname(ip)
        mac = self.get_mac_address(ip)
        open_ports = self.check_ports(ip)
        vendor = self.lookup_mac_vendor(mac)

        # Skip if it's not a real device (no MAC, no hostname, and unreachable)
        if (
            mac == "Unknown"
            and hostname == "Unknown"
            and status == "Unreachable"
        ):
            logger.info(f"Skipping {ip} — likely no device present.")
            return

        device_data = {
            "ip": ip,
            "status": status,
            "latency": latency,
            "hostname": hostname,
            "mac": mac,
            "vendor": vendor,
            "open_ports": open_ports
        }

        with self.lock:
            self.results.append(device_data)
            logger.info(f"Scanned {device_data}")

    def scan(self):
        logger.info(f"Threaded Scan Starting on Subnet: {self.subnet}")
        threads = []

        for ip in self.ip_range:
            t = threading.Thread(target=self.scan_ip, args=(ip,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        logger.info("Threaded Scan Complete.")
        return self.results