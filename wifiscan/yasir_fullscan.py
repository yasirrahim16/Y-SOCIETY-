#!/usr/bin/env python3
# Yasir Rahim - Full Network Scanner with Status
# Shows ALL devices: Online, Offline, Blocked

import subprocess
import sys
from datetime import datetime
import time

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
║                    YASIR RAHIM NETWORK SCANNER                      ║
║                      Full Device Discovery                           ║
╚══════════════════════════════════════════════════════════════════════╝{RESET}
""")

def get_network():
    """Get current network range"""
    try:
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'default' in line:
                parts = line.split()
                iface = parts[parts.index('dev') + 1]
                
                # Get IP info
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

def scan_host(ip, timeout=2):
    """Scan single host"""
    try:
        # Ping check
        result = subprocess.run(['ping', '-c', '1', '-W', str(timeout), ip], 
                              capture_output=True, timeout=timeout+1)
        
        if result.returncode == 0:
            # Get MAC from ARP
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
            
            # Try hostname
            try:
                import socket
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
    
    online_count = 0
    offline_count = 0
    blocked_count = 0
    
    # Scan all 254 IPs
    for i in range(1, 255):
        ip = f"{network}.{i}"
        
        # Skip self
        if ip == my_ip:
            continue
        
        result = scan_host(ip)
        
        if result['status'] == 'ONLINE':
            online_count += 1
            print(f"{GREEN}{result['ip']:<18} {result['mac']:<20} {result['status']:<12} {result['state']:<12} {result['hostname'][:25]}{RESET}")
        elif result['status'] == 'OFFLINE':
            offline_count += 1
            # Uncomment to see offline devices
            # print(f"{RED}{result['ip']:<18} {result['mac']:<20} {result['status']:<12} {result['state']:<12} {result['hostname'][:25]}{RESET}")
        else:
            blocked_count += 1
        
        # Progress indicator
        if i % 50 == 0:
            sys.stdout.write(f"\r{YELLOW}Scanning... {i}/254{RESET}")
            sys.stdout.flush()
    
    print(f"\n\n{CYAN}{BOLD}Scan Complete!{RESET}")
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
