#!/usr/bin/env python3
# RED TEAM PENTESTING SIMULATOR
# DISCLAIMER: This is a VISUAL SIMULATION only. No real network connections are made.
# Authorized for educational demonstration purposes.

import os
import sys
import time
import random
import socket
import webbrowser
import datetime
import base64
import json
import threading

# --- ANSI COLORS ---
R = '\033[91m'  # Red
G = '\033[92m'  # Green
Y = '\033[93m'  # Yellow
B = '\033[94m'  # Blue
C = '\033[96m'  # Cyan
W = '\033[97m'  # White                                                                  RESET = '\033[0m'

# --- MOCK DATA ---
FAKE_TARGET_NAME = "Shayan Ali"
FAKE_TARGET_DEVICE = "Android"
FAKE_TARGET_IP = "192.168.1.105"
FAKE_TARGET_MAC = "A4:5E:60:7B:2C:18"
FAKE_TARGET_LOC = "Nasirabad, Pakistan"

NASIRABAD_LOCATIONS = [
    "https://www.google.com/maps?q=24.9322,67.0854",
    "https://www.google.com/maps?q=24.9325,67.0858",                                         "https://www.google.com/maps?q=24.9319,67.0851",
    "https://www.google.com/maps?q=24.9330,67.0862",
    "https://www.google.com/maps?q=24.9315,67.0848",
    "https://www.google.com/maps?q=24.9328,67.0855",
    "https://www.google.com/maps?q=24.9321,67.0859",
    "https://www.google.com/maps?q=24.9318,67.0853",
    "https://www.google.com/maps?q=24.9332,67.0865",
    "https://www.google.com/maps?q=24.9312,67.0845",
    "https://www.google.com/maps?q=24.9326,67.0850",
    "https://www.google.com/maps?q=24.9329,67.0857",
    "https://www.google.com/maps?q=24.9317,67.0860",
    "https://www.google.com/maps?q=24.9324,67.0849",                                         "https://www.google.com/maps?q=24.9331,67.0861",
    "https://www.google.com/maps?q=24.9316,67.0852",
    "https://www.google.com/maps?q=24.9327,67.0856",
    "https://www.google.com/maps?q=24.9320,67.0863",
    "https://www.google.com/maps?q=24.9314,67.0847",
    "https://www.google.com/maps?q=24.9333,67.0868"
]

SMS_DATABASE = [
    "[Mom]: Ghar kab aoge? Khana ban gaya hai.",
    "[Ali]: Bhai kal class hai ya chutti?",
    "[Easypaisa]: You have received Rs. 500 from 0300XXXXXXX.",
    "[Unknown]: Apka parcel deliver hone wala hai, address confirm karein.",
    "[Hamza]: Free Fire aaja bhai, rank push karna hai.",
    "[Jazz]: Apke number par naya package active ho gaya hai.",
    "[Dad]: Market se aate waqt dahi le ana.",
    "[Ahmed]: Bhai assignment bhej de yar please.",
    "[Salman]: Kal milte hain Nasirabad me.",
    "[Ufone]: Dear customer, enjoy 5000 MBs...",
    "[Zain]: PUBG update aya hai, kar liya?",
    "[Mom]: Phone kyu nahi utha rahe?",
    "[Uber]: Your ride is arriving in 5 minutes.",
    "[Bank]: OTP for your recent transaction is 482910. Do not share.",
    "[Ali]: Notes send kar WhatsApp par.",
    "[Unknown]: Congratulations! Apka inam nikla hai...",
    "[Hamza]: Bhai net nahi chal raha sahi se.",
    "[Dad]: Kahan ho?",
    "[Easypaisa]: Your account balance is low.",
    "[Zain]: Raat ko 10 baje game me aana.",
    "[Ahmed]: Bhai terminal me error aa raha hai."
]

WHATSAPP_DATABASE = [
    {"sender": "Ali", "msg": "Kal university aana hai?"},
    {"sender": "Hamza", "msg": "Bhai headshot check kar mera status pe!"},
    {"sender": "Salman", "msg": "Code bhej de Y-SOCIETY wala."},
    {"sender": "Mom", "msg": "Jaldi wapas aao."},
    {"sender": "Group [CS Boys]", "msg": "Sir ne test cancel kar diya hai."},
    {"sender": "Zain", "msg": "Custom room banaya hai aaja."},
    {"sender": "Ahmed", "msg": "Script run nahi ho rahi yar."},
    {"sender": "Group [Family]", "msg": "Image attached (Photo)"},
    {"sender": "Ali", "msg": "Notes print karwa liye?"},
    {"sender": "Unknown", "msg": "Hello, is this Shayan?"},
    {"sender": "Hamza", "msg": "Bhai ping high aa rahi hai meri."},
    {"sender": "Salman", "msg": "Nasirabad location send kar di hai maine."},
    {"sender": "Group [CS Boys]", "msg": "Project deadline extend ho gayi!"},
    {"sender": "Zain", "msg": "Voice note (0:15s)"},
    {"sender": "Mom", "msg": "Raste me ho?"},
    {"sender": "Ahmed", "msg": "Linux me permission denied aa raha hai."},
    {"sender": "Ali", "msg": "Kal presentation teri hai yaad rakhna."},
    {"sender": "Group [Gaming]", "msg": "Tournament entry fee 500 hai."},
    {"sender": "Hamza", "msg": "Bhai link open kar ek dafa."},
    {"sender": "Salman", "msg": "Hacker boy :D"},
    {"sender": "Zain", "msg": "Bhai wo file corrupt thi."}
]

# --- UTILITY FUNCTIONS ---
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def type_text(text, speed=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def fake_loading(task_name, duration=3):
    print(f"{C}[*] INITIALIZING {task_name.upper()}...{RESET}")
    time.sleep(0.5)
    print(f"{R}[!] ERROR: DEPENDENCY MISSING - ATTEMPTING BYPASS...{RESET}")
    time.sleep(1)
    print(f"{Y}[*] BYPASS SUCCESSFUL. ALLOCATING MEMORY...{RESET}")

    width = 40
    for i in range(width + 1):
        percent = (i * 100) // width
        bar = f"{G}█{RESET}" * i + "-" * (width - i)
        sys.stdout.write(f"\r{Y}[{bar}] {percent}%{RESET}")
        sys.stdout.flush()
        time.sleep(duration / width)
    print(f"\n{G}[+] {task_name.upper()} MODULE LOADED SUCCESSFULLY.{RESET}\n")
    time.sleep(0.5)

def print_banner():
    clear()
    banner = f"""{R}
    ██╗   ██╗      ███████╗ ██████╗  ██████╗ ██╗███████╗████████╗██╗   ██╗
    ╚██╗ ██╔╝      ██╔════╝██╔═══██╗██╔════╝ ██║██╔════╝╚══██╔══╝╚██╗ ██╔╝
     ╚████╔╝ █████╗███████╗██║   ██║██║      ██║█████╗     ██║    ╚████╔╝
      ╚██╔╝  ╚════╝╚════██║██║   ██║██║      ██║██╔══╝     ██║     ╚██╔╝
       ██║         ███████║╚██████╔╝╚██████╗ ██║███████╗   ██║      ██║
       ╚═╝         ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚══════╝   ╚═╝      ╚═╝

             .-""-.
            / _  _ \    {W}CREATOR:{R} YASIR RAHIM
            |(_)(_)|    {W}MADE FOR:{R} SALMAN
            (_  ~  _)   {W}TARGET:{R} SHAYAN ALI
             |'--'|     {W}LOCATION:{R} NASIRABAD
            /'----'\    {G}STATUS:{W} AUTHORIZED SIMULATION{R}
{RESET}"""
    print(banner)

def print_target_info():
    print(f"{Y}="*50)
    print(f"{W}[+] TARGET INFORMATION [SYNCHRONIZED]{RESET}")
    print(f"{C}NAME:      {W}{FAKE_TARGET_NAME}")
    print(f"{C}DEVICE:    {W}{FAKE_TARGET_DEVICE}")
    print(f"{C}IP ADDR:   {W}{FAKE_TARGET_IP}")
    print(f"{C}MAC ADDR:  {W}{FAKE_TARGET_MAC}")
    print(f"{C}LOCATION:  {W}{FAKE_TARGET_LOC}")
    print(f"{Y}="*50 + f"{RESET}\n")

# --- ATTACK SIMULATION MODULES ---
def rat_demo():
    fake_loading("Android RAT Payload")
    type_text(f"{C}[*] Establishing Reverse TCP Connection to {FAKE_TARGET_IP}:4444...{RESET}")
    time.sleep(1)
    print(f"{G}[+] Meterpreter session 1 opened ({FAKE_TARGET_IP}:4444 -> 192.168.1.10:55555){RESET}")
    time.sleep(1)
    print(f"\n{W}meterpreter > {RESET}sysinfo")
    time.sleep(0.5)
    print(f"Computer        : {FAKE_TARGET_DEVICE}_SHAYAN")
    print(f"OS              : Android 13 (Linux 5.10.101)")
    print(f"Architecture    : aarch64")
    print(f"Meterpreter     : java/android\n")

    print(f"{W}meterpreter > {RESET}webcam_list")
    time.sleep(0.5)
    print("1: Back Camera (12MP)")
    print("2: Front Camera (8MP)\n")

    print(f"{W}meterpreter > {RESET}dump_contacts")
    time.sleep(1)
    print(f"{G}[+] Extracting contacts database...{RESET}")
    time.sleep(1)
    for i in range(1, 6):
        print(f"[*] Contact {i}: +92300{random.randint(1111111, 9999999)}")
        time.sleep(0.1)
    print(f"{G}[+] Successfully saved 142 contacts to local drive.{RESET}\n")
    input(f"{Y}Press Enter to return to main menu...{RESET}")

def pc_exploit_demo():
    fake_loading("EternalBlue Exploit")
    type_text(f"{C}[*] Scanning target {FAKE_TARGET_IP} for MS17-010 vulnerability...{RESET}")
    time.sleep(2)
    print(f"{R}[!] TARGET OPERATING SYSTEM MISMATCH.{RESET}")
    print(f"{Y}[*] Note: Target is running Android. EternalBlue (SMBv1) is for Windows.{RESET}")
    print(f"{C}[*] Pivoting to Android ADB exploit framework...{RESET}")
    time.sleep(1.5)
    print(f"{G}[+] Exploitation aborted. Safe mode simulation complete.{RESET}\n")
    input(f"{Y}Press Enter to return to main menu...{RESET}")

def wifi_bruteforce():
    fake_loading("WiFi WPA2 Bruteforce")
    type_text(f"{C}[*] Capturing WPA2 Handshake for BSSID {FAKE_TARGET_MAC}...{RESET}")
    time.sleep(1)
    print(f"{G}[+] Handshake captured successfully.{RESET}")
    type_text(f"{C}[*] Initializing wordlist dictionary attack (rockyou.txt)...{RESET}")

    words = ["password", "123456", "admin", "admin123", "shayan", "shayanali", "shayan12", "ali123", "pakistan", "karachi123", "nasirabad", "hacker", "ysociety", "salman123", "yasir123", "freefire", "pubgmobile", "headshot", "gamer", "unknown", "qwerty", "asdfgh", "zxcvbn", "112233", "000000", "786786", "iloveyou", "shayan1", "shayan1234", "shayan123"]

    for i, word in enumerate(words):
        print(f"[{i+1}] Attempting password: {R}{word}{RESET}")
        time.sleep(0.05)

    print(f"[31] Attempting password: {G}shayan123{RESET}")
    print(f"\n{G}[+] KEY FOUND! [ shayan123 ]{RESET}\n")
    input(f"{Y}Press Enter to return to main menu...{RESET}")

def bluetooth_hack():
    fake_loading("BlueBorne Vulnerability")
    type_text(f"{C}[*] Scanning for Bluetooth devices in range...{RESET}")
    time.sleep(1.5)
    print(f"{G}[+] Found target: {FAKE_TARGET_NAME}'s Device (MAC: {FAKE_TARGET_MAC}){RESET}")
    type_text(f"{C}[*] Injecting BlueBorne payload (CVE-2017-0781)...{RESET}")
    time.sleep(2)
    print(f"{R}[!] ERROR: Bluetooth is currently turned off on target device.{RESET}")
    print(f"{Y}[*] Injecting silent remote BT toggle...{RESET}")
    time.sleep(1)
    print(f"{G}[+] Bluetooth activated. Connection established.{RESET}")
    print(f"{C}[*] Downloading paired device history...{RESET}")
    time.sleep(0.5)
    print(" - Galaxy Buds Pro")
    print(" - Salman's Speaker")
    print(" - Car Audio System\n")
    input(f"{Y}Press Enter to return to main menu...{RESET}")

def gps_tracking():
    fake_loading("GPS Satellite Tracking")
    type_text(f"{C}[*] Hooking into Android LocationManager Service...{RESET}")
    time.sleep(1)
    print(f"{Y}[*] Bypassing mock locations...{RESET}")
    time.sleep(1.5)

    selected_loc = random.choice(NASIRABAD_LOCATIONS)
    print(f"{G}[+] Real-time coordinates acquired!{RESET}")
    print(f"{C}Target Location URL: {W}{selected_loc}{RESET}")

    type_text(f"{Y}[*] Opening coordinates in Google Maps...{RESET}")
    time.sleep(1)
    try:
        webbrowser.open(selected_loc)
    except:
        print(f"{R}[!] Could not open browser automatically. Please copy the link.{RESET}")
    print()
    input(f"{Y}Press Enter to return to main menu...{RESET}")

def ddos_flood():
    fake_loading("UDP/TCP Packet Flood")
    type_text(f"{C}[*] Targeting {FAKE_TARGET_IP} on port 80/443...{RESET}")
    print(f"{R}[!] WARNING: Commencing simulated flood...{RESET}")
    time.sleep(1)

    try:
        for i in range(1, 101):
            sys.stdout.write(f"\r{Y}[*] Sending packet {i*5432} to {FAKE_TARGET_IP}... Size: 65500 bytes{RESET}")
            sys.stdout.flush()
            time.sleep(0.02)
    except KeyboardInterrupt:
        pass
    print(f"\n\n{G}[+] Simulated flood complete. Target system stability affected (MOCK).{RESET}\n")
    input(f"{Y}Press Enter to return to main menu...{RESET}")

def whatsapp_clone():
    fake_loading("WhatsApp Database Decryption")
    type_text(f"{C}[*] Accessing Android/media/com.whatsapp/WhatsApp/Databases/...{RESET}")
    time.sleep(1)
    print(f"{Y}[*] Downloading msgstore.db.crypt14...{RESET}")
    time.sleep(2)
    print(f"{G}[+] Decryption key extracted from Android Keystore.{RESET}")
    print(f"{C}[*] Parsing WhatsApp messages...{RESET}\n")
    time.sleep(1)

    print(f"{W}--- WHATSAPP RECENT CHATS ---{RESET}")
    for i, chat in enumerate(WHATSAPP_DATABASE):
        print(f"{G}[{chat['sender']}]{RESET}: {chat['msg']}")
        time.sleep(0.1)
    print(f"\n{C}[+] {len(WHATSAPP_DATABASE)} messages parsed successfully.{RESET}\n")
    input(f"{Y}Press Enter to return to main menu...{RESET}")

def camera_hijack():
    fake_loading("Camera API Hooking")
    type_text(f"{C}[*] Requesting background camera access (Camera2 API)...{RESET}")
    time.sleep(1)
    print(f"{R}[!] Security Warning detected on target device.{RESET}")
    print(f"{Y}[*] Injecting overlay to hide warning icon...{RESET}")
    time.sleep(1.5)
    print(f"{G}[+] Camera access granted silently.{RESET}")

    print(f"\n{W}[ SIMULATED CAMERA VIEW ]{RESET}")
    for _ in range(5):
        print(f"{C}[*] Frame captured - Saving as IMG_{int(time.time())}.jpg{RESET}")
        time.sleep(0.5)
    print(f"\n{G}[+] 5 frames saved to local loot directory.{RESET}\n")
    input(f"{Y}Press Enter to return to main menu...{RESET}")

def sms_tap():
    fake_loading("SMS Content Provider Access")
    type_text(f"{C}[*] Querying content://sms/inbox...{RESET}")
    time.sleep(1.5)
    print(f"{G}[+] SMS Database accessed.{RESET}\n")

    print(f"{W}--- LATEST SMS MESSAGES ---{RESET}")
    for i, msg in enumerate(SMS_DATABASE):
        print(f"{Y}{msg}{RESET}")
        time.sleep(0.1)
    print(f"\n{C}[+] {len(SMS_DATABASE)} SMS records displayed.{RESET}\n")
    input(f"{Y}Press Enter to return to main menu...{RESET}")

def network_scan():
    fake_loading("Deep Network & App Scan")
    type_text(f"{C}[*] Running Nmap scan on local subnet (192.168.1.0/24)...{RESET}")
    time.sleep(2)
    print(f"{G}[+] Hosts up: 4{RESET}")
    print(" - 192.168.1.1 (Router)")
    print(f" - {FAKE_TARGET_IP} ({FAKE_TARGET_NAME}'s Android)")
    print(" - 192.168.1.108 (Salman's PC)")
    print(" - 192.168.1.112 (Smart TV)\n")

    type_text(f"{C}[*] Scraping target app data (Instagram)...{RESET}")
    time.sleep(1)
    print(f"{G}[+] Session token found for Instagram.{RESET}")
    print(f"{W}Username: @shayan_ali_real{RESET}")
    print(f"{W}Followers: 452 | Following: 310{RESET}")
    print(f"{C}[*] Direct Messages extracted: 5 recent threads.{RESET}\n")

    input(f"{Y}Press Enter to return to main menu...{RESET}")

# --- MAIN MENU ---
def main():
    while True:
        print_banner()
        print_target_info()

        print(f"{R}=== EXPLOITATION MODULES (SIMULATION) ==={RESET}")
        print(f"[{G}1{RESET}] ANDROID RAT DEMO        [{G}6{RESET}] DDoS FLOOD DEMO")
        print(f"[{G}2{RESET}] PC EXPLOIT DEMO         [{G}7{RESET}] WHATSAPP CLONE DEMO")
        print(f"[{G}3{RESET}] WIFI BRUTEFORCE DEMO    [{G}8{RESET}] CAMERA HIJACK DEMO")
        print(f"[{G}4{RESET}] BLUETOOTH HACK DEMO     [{G}9{RESET}] SMS TAP DEMO")
        print(f"[{G}5{RESET}] GPS TRACKING DEMO       [{G}10{RESET}] NETWORK SCAN + INSTAGRAM")
        print(f"\n[{R}0{RESET}] EXIT FRAMEWORK\n")

        choice = input(f"{W}Y-SOCIETY@root:~# {RESET}")

        if choice == '1':
            rat_demo()
        elif choice == '2':
            pc_exploit_demo()
        elif choice == '3':
            wifi_bruteforce()
        elif choice == '4':
            bluetooth_hack()
        elif choice == '5':
            gps_tracking()
        elif choice == '6':
            ddos_flood()
        elif choice == '7':
            whatsapp_clone()
        elif choice == '8':
            camera_hijack()
        elif choice == '9':
            sms_tap()
        elif choice == '10':
            network_scan()
        elif choice == '0':
            print(f"\n{R}[!] SHUTTING DOWN Y-SOCIETY SIMULATION...{RESET}")
            time.sleep(1)
            print(f"{W}MADE BY YASIR RAHIM // Y-SOCIETY // FOR: SALMAN{RESET}\n")
            sys.exit(0)
        else:
            print(f"{R}[!] Invalid option. Please try again.{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] PROCESS INTERRUPTED...{RESET}")
        print(f"{W}MADE BY YASIR RAHIM // Y-SOCIETY // FOR: SALMAN{RESET}\n")
        sys.exit(0)
