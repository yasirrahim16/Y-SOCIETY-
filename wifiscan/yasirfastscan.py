#!/usr/bin/env python3
# Yasir Rahim - Fast Multi-Threaded Network Scanner

import subprocess
import sys
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_banner():
    print(f"""
{CYAN}{BOLD}
╔══════════════════════════════════════════════════════════════════════╗
║                    YASIR RAHIM NETWORK SCANNER                       ║
║                  Ultra-Fast Threaded Discovery                       ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")

def get_network():
    try:
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'default' in line:
                parts = line.split()
                iface = parts[parts.index('dev') + 1]
                
                ip_result = subprocess.run(['ip', 'addr', 'show', iface], 
                                       capture_output=True, text=True)
                for ip_line in ip_result.stdout.split('\n'):
                    if 'inet ' in ip_line:
                        ip = ip_line.strip().split()[1].split('/')[0]
                        network = ip.rsplit('.', 1)[0]
                        return network, iface, ip
    except:
        pass
    return "192.168.100", "wlan0", "192.168.100.5"

def scan_host(ip, timeout=1):
    try:
        # Ping with 1 second timeout
        result = subprocess.run(['ping', '-c', '1', '-W', str(timeout), ip], 
                              capture_output=True, timeout=timeout+1)
        
        if result.returncode == 0:
            arp_result = subprocess.run(['ip', 'neigh', 'show', ip], 
                                      capture_output=True, text=True)
            mac = "Unknown"
            state = "FAILED"
            
            if arp_result.stdout:
                parts = arp_result.stdout.strip().split()
                if 'lladdr' in parts:
                    mac_idx = parts.index('lladdr') + 1
                    mac = parts[mac_idx]
                    state = parts[-1] if parts[-1] in ['REACHABLE', 'STALE', 'DELAY', 'PROBE', 'FAILED'] else 'UNKNOWN'
            
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except:
                hostname = "Unknown"
            
            return {
                'ip': ip,
                'mac': mac,
                'status': 'ONLINE',
                'state': state,
                'hostname': hostname
            }
        else:
            return {
                'ip': ip,
                'mac': '-',
                'status': 'OFFLINE',
                'state': '-',
                'hostname': '-'
            }
    except:
        return {
            'ip': ip,
            'mac': '-',
            'status': 'BLOCKED/TIMEOUT',
            'state': '-',
            'hostname': '-'
        }

def main():
    print_banner()
    
    network, iface, my_ip = get_network()
    print(f"{BLUE}[*] Interface: {iface}")
    print(f"[*] Your IP: {my_ip}")
    print(f"[*] Scanning: {network}.1 - {network}.254{RESET}\n")
    
    print(f"{BOLD}{WHITE}{'IP Address':<18} {'MAC Address':<20} {'Status':<12} {'State':<12} {'Hostname'}{RESET}")
    print(f"{WHITE}{'-'*90}{RESET}")
    
    ip_list = [f"{network}.{i}" for i in range(1, 255) if f"{network}.{i}" != my_ip]
    results = []
    
    # 50 Threads parallel mein saare IPs ek sath scan karenge
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_host, ip): ip for ip in ip_list}
        for future in as_completed(futures):
            results.append(future.result())
    
    # IPs ko order mein sort karna
    results.sort(key=lambda x: int(x['ip'].split('.')[-1]))
    
    online_count = 0
    offline_count = 0
    blocked_count = 0
    
    for result in results:
        if result['status'] == 'ONLINE':
            online_count += 1
            print(f"{GREEN}{result['ip']:<18} {result['mac']:<20} {result['status']:<12} {result['state']:<12} {result['hostname'][:25]}{RESET}")
        elif result['status'] == 'OFFLINE':
            offline_count += 1
        else:
            blocked_count += 1

    print(f"\n{CYAN}{BOLD}Scan Complete!{RESET}")
    print(f"{GREEN}🟢 Online: {online_count}{RESET}")
    print(f"{RED}🔴 Offline: {offline_count}{RESET}")
    print(f"{YELLOW}⚠️  Blocked/Timeout: {blocked_count}{RESET}")
    print(f"\n{MAGENTA}Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Scan interrupted by user{RESET}")
        sys.exit(0)
