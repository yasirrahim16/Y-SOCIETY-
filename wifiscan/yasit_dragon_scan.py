#!/usr/bin/env python3
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Colors
RED, GREEN, YELLOW, CYAN, WHITE, BOLD, RESET = '\033[91m', '\033[92m', '\033[93m', '\033[96m', '\033[97m', '\033[1m', '\033[0m'

DRAGON = f"""
{CYAN}{BOLD}
      /\\       /\\
     /  \\     /  \\
    /    \\   /    \\
   /      \\_/      \\
  /   /\\  / \\  /\\   \\
 /   /  \\/   \\/  \\   \\
/___/    /   \\    \\___\\
    {WHITE}YASIT{CYAN}  DRAGON {WHITE}SCANNER{CYAN}
{RESET}
"""

def get_network():
    try:
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'default' in line:
                iface = line.split('dev')[1].split()[0]
                ip_result = subprocess.run(['ip', 'addr', 'show', iface], capture_output=True, text=True)
                for ip_line in ip_result.stdout.split('\n'):
                    if 'inet ' in ip_line:
                        ip = ip_line.strip().split()[1].split('/')[0]
                        return ip.rsplit('.', 1)[0], iface, ip
    except:
        pass
    return "192.168.100", "wlan0", "192.168.100.199"

def scan_ip(ip):
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True, timeout=2)
        
        # Get MAC from ARP
        arp_result = subprocess.run(['ip', 'neigh', 'show', ip], capture_output=True, text=True)
        mac = "Unknown"
        state = "FAILED"
        
        if arp_result.stdout:
            parts = arp_result.stdout.strip().split()
            if 'lladdr' in parts:
                mac = parts[parts.index('lladdr') + 1]
                state = parts[-1] if parts[-1] in ['REACHABLE', 'STALE', 'DELAY', 'PROBE', 'FAILED', 'INCOMPLETE'] else 'UNKNOWN'
        
        # Try hostname
        try:
            import socket
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            hostname = "Unknown"
        
        if result.returncode == 0:
            return {'ip': ip, 'mac': mac, 'status': 'ONLINE', 'state': state, 'hostname': hostname}
        else:
            return {'ip': ip, 'mac': mac, 'status': 'OFFLINE', 'state': state, 'hostname': hostname}
            
    except subprocess.TimeoutExpired:
        return {'ip': ip, 'mac': '-', 'status': 'BLOCKED/TIMEOUT', 'state': '-', 'hostname': '-'}
    except:
        return {'ip': ip, 'mac': '-', 'status': 'ERROR', 'state': '-', 'hostname': '-'}

def main():
    print(DRAGON)
    
    network, iface, my_ip = get_network()
    print(f"{CYAN}[*] Interface: {iface}")
    print(f"[*] Your IP: {my_ip}")
    print(f"[*] Scanning: {network}.1 - {network}.254{RESET}\n")
    
    print(f"{BOLD}{WHITE}{'IP Address':<18} {'MAC Address':<20} {'Status':<15} {'State':<12} {'Hostname'}{RESET}")
    print(f"{WHITE}{'-'*90}{RESET}")
    
    devices = []
    
    # Multithreaded scan - FAST!
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_ip, f"{network}.{i}"): i for i in range(1, 255) if f"{network}.{i}" != my_ip}
        
        for future in futures:
            result = future.result()
            devices.append(result)
            
            # Print in real-time
            if result['status'] == 'ONLINE':
                print(f"{GREEN}{result['ip']:<18} {result['mac']:<20} {result['status']:<15} {result['state']:<12} {result['hostname'][:20]}{RESET}")
            elif result['status'] == 'OFFLINE' and result['mac'] != 'Unknown' and result['mac'] != '-':
                # Show offline devices that were previously seen
                print(f"{RED}{result['ip']:<18} {result['mac']:<20} {result['status']:<15} {result['state']:<12} {result['hostname'][:20]}{RESET}")
            elif result['status'] == 'BLOCKED/TIMEOUT':
                print(f"{YELLOW}{result['ip']:<18} {result['mac']:<20} {result['status']:<15} {result['state']:<12} {result['hostname'][:20]}{RESET}")
    
    # Summary
    online = len([d for d in devices if d['status'] == 'ONLINE'])
    offline = len([d for d in devices if d['status'] == 'OFFLINE'])
    blocked = len([d for d in devices if d['status'] == 'BLOCKED/TIMEOUT'])
    
    print(f"\n{CYAN}{BOLD}╔{'═'*68}╗")
    print(f"║{f' SCAN COMPLETE - {datetime.now().strftime("%H:%M:%S")}':^68}║")
    print(f"╠{'═'*68}╣")
    print(f"║  {GREEN}🟢 ONLINE: {online:>3}{' '*54}║")
    print(f"║  {RED}🔴 OFFLINE: {offline:>3}{' '*53}║")
    print(f"║  {YELLOW}⚠️  BLOCKED: {blocked:>3}{' '*52}║")
    print(f"╚{'═'*68}╝{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Stopped by user{RESET}")
        sys.exit(0)
