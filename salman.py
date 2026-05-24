import os
import sys
import time
import random
import socket
import webbrowser
import datetime

# --- Colors ---
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
C = '\033[96m'
W = '\033[0m'

# --- Fake Data ---
TARGET_NAME = "Target_Alpha"
TARGET_IP = "192.168.x.x"
TARGET_MAC = "XX:XX:XX:XX:XX:XX"
TARGET_LOC = "Simulated_Zone"

FAKE_SMS = [
    "From: Mom - Call me when you get home.",
    "To: Mom - Okay, I will be there in 20 mins.",
    "From: Unknown - Your verification code is 8493.",
    "From: Friend - Are we still meeting tomorrow?",
    "To: Friend - Yes, usual place at 5 PM.",
    "From: Work - Meeting rescheduled to 10 AM.",
    "From: Carrier - Your data limit is reaching 80%.",
    "To: John - Did you send the files?",
    "From: John - Sending them now.",
    "From: PizzaPlace - Your order is out for delivery!",
    "To: +123456789 - Who is this?",
    "From: Delivery - Package dropped at front door.",
    "To: Work - I will be running 10 mins late today.",
    "From: Bank - Alert: Login from new device detected.",
    "To: Friend - Let's play that game tonight."
]

LOCATIONS = [
    "https://www.google.com/maps?q=0,0",
    "https://www.google.com/maps?q=10.0,10.0",
    "https://www.google.com/maps?q=20.0,20.0",
    "https://www.google.com/maps?q=30.0,30.0",
    "https://www.google.com/maps?q=40.0,40.0"
]

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def fake_loading(module_name):
    print(f"\n{C}[*] Initializing {module_name} framework...{W}")
    time.sleep(1)
    bar_length = 30
    for i in range(bar_length + 1):
        percent = int((i / bar_length) * 100)
        bar = '█' * i + '-' * (bar_length - i)
        sys.stdout.write(f'\r{Y}[{bar}] {percent}% {W}')
        sys.stdout.flush()
        time.sleep(random.uniform(0.01, 0.1))
    print(f"\n{G}[+] Modules loaded successfully.{W}\n")
    time.sleep(0.5)

def simulate_error(system_name):
    print(f"{Y}[*] Attempting to bypass {system_name} security...{W}")
    time.sleep(1.5)
    print(f"{R}[!] ERROR: {system_name} access denied. Privilege escalation failed.{W}")
    print(f"{R}[!] Handshake rejected by host.{W}")
    time.sleep(1)

def print_banner():
    clear_screen()
    banner = f"""{R}
        .                                                      .
        .n                   .                 .                  n.
  .   .dP                  dP                   9b                 9b.    .
 4    qXb         .       dX                     Xb       .        dXp     t
dX.    9Xb      .dXb    __                         __    dXb.     dXP     .Xb
9XXb._       _.dXXXXb dXXXXbo.                 .odXXXXb dXXXXb._       _.dXXP
 9XXXXXXXXXXXXXXXXXXXVXXXXXXXXOo.           .oOXXXXXXXXVXXXXXXXXXXXXXXXXXXXP
  `9XXXXXXXXXXXXXXXXXXXXX'~   ~`OOO8b   d8OOO'~   ~`XXXXXXXXXXXXXXXXXXXXXP'
    `9XXXXXXXXXXXP' `9XX'   DIE    `98v8P'  HACK    `XXP' `9XXXXXXXXXXXP'
        ~~~~~~~       9X.          .db|db.          .XP       ~~~~~~~
                        )b.  .dbo.dP'`v'`9b.odb.  .dX(
                      ,dXXXXXXXXXXXb     dXXXXXXXXXXXb.
                     dXXXXXXXXXXXP'   .   `9XXXXXXXXXXXb
                    dXXXXXXXXXXXXb   d|b   dXXXXXXXXXXXXb
                    9XXb'   `XXXXXb.dX|Xb.dXXXXX'   `dXXP
                     `'      9XXXXXX(   )XXXXXXP      `'
                              XXXX X.`v'.X XXXX
                              XP^X'`b   d'`X^XX
                              X. 9  `   '  P )X
                              `b  `       '  d'
                               `             '
{W}"""
    print(banner)
    print(f"{R}================================================================{W}")
    print(f"{G} SIMULATION ENVIRONMENT - EDUCATIONAL USE ONLY {W}")
    print(f"{R}================================================================{W}")
    print(f"{C} TARGET NAME  : {TARGET_NAME}")
    print(f" TARGET DEVICE: Android")
    print(f" TARGET IP    : {TARGET_IP}")
    print(f" TARGET MAC   : {TARGET_MAC}")
    print(f" LOCATION     : {TARGET_LOC}{W}")
    print(f"{R}================================================================{W}\n")

def menu():
    while True:
        print_banner()
        print(f"{Y}CHOOSE SIMULATION MODULE:{W}")
        print(f"{G}[1] {W}ANDROID RAT DEMO")
        print(f"{G}[2] {W}PC EXPLOIT DEMO")
        print(f"{G}[3] {W}WIFI BRUTEFORCE DEMO")
        print(f"{G}[4] {W}BLUETOOTH HACK DEMO")
        print(f"{G}[5] {W}GPS TRACKING DEMO")
        print(f"{G}[6] {W}DDoS FLOOD DEMO")
        print(f"{G}[7] {W}WHATSAPP CLONE DEMO (Will Error)")
        print(f"{G}[8] {W}CAMERA HIJACK DEMO (Will Error)")
        print(f"{G}[9] {W}SMS TAP DEMO (Tracker)")
        print(f"{G}[10]{W} NETWORK SCAN + SOCIAL DEMO")
        print(f"{R}[0] {W}EXIT\n")
        
        choice = input(f"{C}root@simulation:~# {W}")
        
        if choice == '1':
            fake_loading("RAT Payloads")
            print(f"{G}[+] Connection established to {TARGET_IP}{W}")
            for i in range(5):
                print(f"{C}[*] Fetching system logs... chunk_{i}.bin{W}")
                time.sleep(0.3)
            print(f"{G}[+] Syslog extraction complete.{W}")
            input(f"\n{Y}Press Enter to return...{W}")
            
        elif choice == '2':
            fake_loading("EternalBlue MS17-010")
            print(f"{Y}[*] Sending smb buffers...{W}")
            time.sleep(1)
            print(f"{G}[+] Ring0 payload triggered.{W}")
            print(f"{G}[+] WINREG overwritten. Access granted.{W}")
            input(f"\n{Y}Press Enter to return...{W}")
            
        elif choice == '3':
            fake_loading("WPA2 Handshake Cracker")
            print(f"{C}[*] BSSID: {TARGET_MAC} captured.{W}")
            for i in range(1, 32):
                pwd = f"pass{random.randint(1000,9999)}"
                if i == 31:
                    pwd = "targetpassword123"
                    print(f"{G}[+] Attempt {i}: {pwd} ---> SUCCESS! KEY FOUND.{W}")
                else:
                    print(f"{R}[-] Attempt {i}: {pwd} ---> Failed.{W}")
                time.sleep(0.1)
            input(f"\n{Y}Press Enter to return...{W}")
            
        elif choice == '4':
            fake_loading("BlueBorne Exploit")
            print(f"{Y}[*] Scanning for discoverable BT devices...{W}")
            time.sleep(1)
            print(f"{G}[+] Found: {TARGET_NAME}_Phone (RSSI: -45dBm){W}")
            print(f"{C}[*] Sending L2CAP packets...{W}")
            time.sleep(1)
            print(f"{G}[+] Bluetooth stack overflow successful.{W}")
            input(f"\n{Y}Press Enter to return...{W}")
            
        elif choice == '5':
            fake_loading("GPS Satellite Triangulation")
            for i in range(5):
                print(f"{C}[*] Resolving satellite {i+1} coordinates...{W}")
                time.sleep(0.4)
            loc = random.choice(LOCATIONS)
            print(f"{G}[+] Location pinned! Opening Maps: {loc}{W}")
            time.sleep(1)
            try:
                webbrowser.open(loc)
            except:
                print(f"{Y}[*] Could not launch browser. URL: {loc}{W}")
            input(f"\n{Y}Press Enter to return...{W}")
            
        elif choice == '6':
            fake_loading("SYN Flood Generator")
            print(f"{R}[!] INITIATING PACKET FLOOD ON {TARGET_IP}{W}")
            for i in range(30):
                print(f"{C}[*] Sent {random.randint(1000, 5000)} packets to port 80...{W}")
                time.sleep(0.05)
            print(f"{G}[+] Target bandwidth saturated.{W}")
            input(f"\n{Y}Press Enter to return...{W}")
            
        elif choice == '7':
            fake_loading("WhatsApp Extractor")
            simulate_error("WhatsApp Encrypted Database")
            input(f"\n{Y}Press Enter to return...{W}")
            
        elif choice == '8':
            fake_loading("Camera Subsystem Bridge")
            simulate_error("Hardware Camera Driver")
            input(f"\n{Y}Press Enter to return...{W}")
            
        elif choice == '9':
            fake_loading("SMS Interceptor Module")
            print(f"{G}[+] Access to com.android.providers.telephony SUCCESS.{W}")
            print(f"{Y}[*] Dumping SMS messages...{W}\n")
            time.sleep(1)
            for msg in FAKE_SMS:
                timestamp = datetime.datetime.now() - datetime.timedelta(minutes=random.randint(1, 1000))
                print(f"{C}[{timestamp.strftime('%Y-%m-%d %H:%M')}] {W}{msg}")
                time.sleep(0.3)
            print(f"\n{G}[+] SMS Dump complete.{W}")
            input(f"\n{Y}Press Enter to return...{W}")
            
        elif choice == '10':
            fake_loading("Network Recon & OSINT")
            print(f"{C}[*] Mapping subnet 192.168.1.0/24...{W}")
            time.sleep(1)
            for i in range(1, 5):
                print(f"{G}[+] Host up: 192.168.1.{100+i} - Vendor: Generic{W}")
                time.sleep(0.2)
            print(f"\n{Y}[*] Querying social platforms for target fingerprint...{W}")
            time.sleep(1.5)
            print(f"{G}[+] Found public data cache. Analyzing metadata...{W}")
            input(f"\n{Y}Press Enter to return...{W}")
            
        elif choice == '0':
            print(f"\n{R}[*] Terminating simulation environment...{W}")
            time.sleep(1)
            print(f"{G}MADE BY SIMULATION GENERATOR // EDUCATIONAL PURPOSES{W}\n")
            sys.exit(0)
            
        else:
            print(f"{R}[!] Invalid command.{W}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(f"\n{R}[*] Simulation aborted by user.{W}")
        sys.exit(0)
    
