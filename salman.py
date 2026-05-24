import os
import time
import random
import sys

# Termux Colors
GREEN = '\033[0;32m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
YELLOW = '\033[1;33m'
WHITE = '\033[1;37m'
NC = '\033[0m' # No Color

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def fake_loading():
    clear_screen()
    print(f"{RED}[*] INITIATING SALMAN CONTROL OWNER FRAMEWORK...{NC}\n")
    
    modules = [
        "exploit/multi/handler",
        "payload/android/meterpreter/reverse_tcp",
        "post/windows/gather/hashdump",
        "auxiliary/scanner/portscan/tcp",
        "exploit/router/dns_hijack",
        "nasirabad_gps_tracker_v3"
    ]
    
    # 5-second realistic loading simulation
    for i in range(1, 101):
        time.sleep(0.05) # Total ~5 seconds
        sys.stdout.write(f"\r{BLUE}[*] Booting Core System: {GREEN}[{'#' * (i // 5)}{'.' * (20 - (i // 5))}] {i}%{NC}")
        sys.stdout.flush()
        
        # Randomly show module loading
        if i % 20 == 0:
            sys.stdout.write(f"\n{CYAN}[+] Module Loaded: {random.choice(modules)}{NC}\n")
            
    print(f"\n\n{YELLOW}[!] Bypassing Mainframe Security...{NC}")
    time.sleep(1)
    print(f"{GREEN}[++] ROOT ACCESS GRANTED TO SYSTEM.{NC}")
    time.sleep(1.5)

def header():
    print(f"{RED}")
    print(r"""
  ██████  █████  ██      ███    ███  █████  ███    ██ 
 ██      ██   ██ ██      ████  ████ ██   ██ ████   ██ 
 ███████ ███████ ██      ██ ████ ██ ███████ ██ ██  ██ 
      ██ ██   ██ ██      ██  ██  ██ ██   ██ ██  ██ ██ 
 ██████  ██   ██ ███████ ██      ██ ██   ██ ██   ████ 
                                                      
    [ OWNER: SALMAN ] --- [ FRAMEWORK v2.0-PRO ]
    """)
    print(f"{NC}")
    print(f"{CYAN}=============================================================={NC}")
    print(f"{YELLOW} [*] WARNING: Unauthorized use is strictly prohibited.{NC}")
    print(f"{CYAN}=============================================================={NC}")

def device_info():
    fake_ips = ["192.168.10.45", "103.255.4.12", "172.16.254.1", "39.40.124.89"]
    devices = ["Samsung Galaxy S24 Ultra", "OnePlus 12", "Xiaomi 14 Pro", "iPhone 15 Pro Max"]
    
    print(f"\n{BLUE}[ TARGET SYSTEM INFO ]{NC}")
    print(f" [+] Target Name   : {GREEN}Aana Shiyan Ali{NC}")
    print(f" [+] Assigned IP   : {GREEN}{random.choice(fake_ips)}{NC}")
    print(f" [+] Device Model  : {GREEN}{random.choice(devices)}{NC}")
    print(f" [+] Network ISP   : {GREEN}PTCL / Zong 4G{NC}")
    print(f"{CYAN}--------------------------------------------------------------{NC}")

def nasirabad_location():
    locations = [
        "Nasirabad Main Bazar, Sector B",
        "Near Grid Station, Nasirabad, Balochistan",
        "Ward No. 4, Jamali Mohalla, Nasirabad",
        "National Highway (N-65) Bypass, Nasirabad",
        "DPO Office Road, Nasirabad",
        "District Headquarters Hospital Area, Nasirabad"
    ]
    print(f"\n{BLUE}[*] Triangulating GPS Signals from cellular towers...{NC}")
    time.sleep(1.5)
    print(f"{RED}[!] Bypassing Location Spoofers...{NC}")
    time.sleep(1)
    loc = random.choice(locations)
    lat = round(random.uniform(28.5000, 28.6000), 4)
    lon = round(random.uniform(67.4000, 67.5000), 4)
    
    print(f"{GREEN}[+] Live Target Location Found!{NC}")
    print(f"{YELLOW} -> Address: {loc}{NC}")
    print(f"{YELLOW} -> Coordinates: {lat}° N, {lon}° E{NC}")
    print(f"{YELLOW} -> Accuracy: Within 3.5 meters{NC}")
    input(f"\n{WHITE}Press Enter to return to Main Menu...{NC}")

def mobile_control():
    print(f"\n{BLUE}[*] Establishing Reverse TCP Connection to Mobile Device...{NC}")
    time.sleep(2)
    
    status = random.choice(["GRANTED", "DENIED", "GRANTED"]) # Higher chance of success for fun
    
    if status == "DENIED":
        print(f"{RED}[!!] ACCESS DENIED: Target device firewall (Knox/Secure Enclave) blocked the payload!{NC}")
        input(f"\n{WHITE}Press Enter to return to Main Menu...{NC}")
    else:
        print(f"{GREEN}[++] ACCESS GRANTED! Session 1 Opened.{NC}")
        time.sleep(1)
        
        while True:
            clear_screen()
            header()
            print(f"{RED}--- [ MOBILE CONTROL SUB-MENU ] ---{NC}")
            print(f"{GREEN}1.{NC} Jam WiFi Network (Deauth Attack)")
            print(f"{GREEN}2.{NC} Crash Bluetooth Services")
            print(f"{GREEN}3.{NC} Force Volume to 0% (Silent Mode)")
            print(f"{GREEN}4.{NC} Force Device Reboot (Kernel Panic)")
            print(f"{GREEN}5.{NC} Dump SMS & Call Logs")
            print(f"{GREEN}6.{NC} Bypass Screen Lock (Brute-force PIN)")
            print(f"{GREEN}7.{NC} Back to Main Menu")
            
            sub_choice = input(f"\n{CYAN}meterpreter > {NC}")
            
            if sub_choice == "1":
                print(f"{BLUE}[*] Sending Deauth packets to router...{NC}")
                time.sleep(2)
                print(f"{GREEN}[+] Target completely disconnected from WiFi.{NC}")
                time.sleep(1.5)
            elif sub_choice == "2":
                print(f"{BLUE}[*] Overloading Bluetooth stack...{NC}")
                time.sleep(1.5)
                print(f"{GREEN}[+] Bluetooth module crashed successfully.{NC}")
                time.sleep(1.5)
            elif sub_choice == "3":
                print(f"{BLUE}[*] Injecting audio control payload...{NC}")
                time.sleep(1)
                print(f"{GREEN}[+] Device muted. Volume locked at 0%.{NC}")
                time.sleep(1.5)
            elif sub_choice == "4":
                print(f"{RED}[!] Sending critical sysrq trigger...{NC}")
                time.sleep(2)
                print(f"{GREEN}[+] Device rebooting... Connection lost.{NC}")
                time.sleep(1.5)
                break
            elif sub_choice == "5":
                print(f"{BLUE}[*] Extracting databases (sms.db, calllog.db)...{NC}")
                time.sleep(2)
                print(f"{GREEN}[+] 452 SMS and 128 Call Logs extracted to /root/loot/ {NC}")
                time.sleep(1.5)
            elif sub_choice == "6":
                print(f"{BLUE}[*] Running PIN Brute-force...{NC}")
                for i in range(1111, 1150):
                    sys.stdout.write(f"\r{RED}Trying PIN: {i}{NC}")
                    sys.stdout.flush()
                    time.sleep(0.05)
                print(f"\n{GREEN}[+] Screen Lock Bypassed! PIN is 1149{NC}")
                time.sleep(2)
            elif sub_choice == "7":
                break
            else:
                print(f"{RED}[-] Unknown command.{NC}")
                time.sleep(1)

def pc_control():
    print(f"\n{BLUE}[*] Targeting PC MAC Address...{NC}")
    time.sleep(1.5)
    print(f"{RED}[!!] FIREWALL ALERT: Windows Defender / CrowdStrike detected anomalous activity.{NC}")
    time.sleep(1)
    print(f"{RED}[!] Exploit failed. Connection terminated to avoid tracing.{NC}")
    input(f"\n{WHITE}Press Enter to return to Main Menu...{NC}")

def router_control():
    print(f"\n{BLUE}[*] Initiating Nmap Stealth Scan on Gateway...{NC}")
    time.sleep(2)
    print(f"{GREEN}[+] Port 80   (HTTP)   - OPEN")
    print(f"[+] Port 443  (HTTPS)  - OPEN")
    print(f"[+] Port 8080 (Proxy)  - FILTERED{NC}")
    time.sleep(1)
    print(f"{BLUE}[*] Injecting custom firmware payload...{NC}")
    time.sleep(2)
    print(f"{GREEN}[++] Admin privileges escalated. Router DNS is now under your control.{NC}")
    input(f"\n{WHITE}Press Enter to return to Main Menu...{NC}")

def camera_mic_intercept():
    print(f"\n{BLUE}[*] Bypassing Camera/Mic hardware indicators...{NC}")
    time.sleep(2)
    print(f"{GREEN}[+] Front Camera accessed. Streaming to /dev/null...")
    print(f"[+] Microphone recording started (Audio stream active).{NC}")
    time.sleep(1)
    print(f"{RED}[!] Bandwidth low: Stream paused to maintain stealth.{NC}")
    input(f"\n{WHITE}Press Enter to return to Main Menu...{NC}")

def main():
    fake_loading()
    
    while True:
        clear_screen()
        header()
        device_info()
        
        print(f"{YELLOW}--- [ MAIN EXPLOIT MENU ] ---{NC}")
        print(f"{GREEN}1.{NC} Execute Mobile Control (Target: Aana Shiyan Ali)")
        print(f"{GREEN}2.{NC} Execute PC Control (Remote Desktop)")
        print(f"{GREEN}3.{NC} Router Exploit & Network Hijack")
        print(f"{GREEN}4.{NC} Live GPS Tracking (Nasirabad Radar)")
        print(f"{GREEN}5.{NC} Intercept Camera & Microphone")
        print(f"{GREEN}6.{NC} Extract WhatsApp & Social Media Data")
        print(f"{GREEN}7.{NC} Bypass Satellite Communications (Advanced)")
        print(f"{GREEN}8.{NC} Exit Framework & Clear Logs")
        
        choice = input(f"\n{CYAN}root@salman:~# {NC}")
        
        if choice == "1":
            mobile_control()
        elif choice == "2":
            pc_control()
        elif choice == "3":
            router_control()
        elif choice == "4":
            nasirabad_location()
        elif choice == "5":
            camera_mic_intercept()
        elif choice == "6":
            print(f"\n{BLUE}[*] Decrypting msgstore.db.crypt14...{NC}")
            time.sleep(2)
            print(f"{GREEN}[+] WhatsApp Chat History downloaded successfully.{NC}")
            input(f"\n{WHITE}Press Enter to return...{NC}")
        elif choice == "7":
            print(f"\n{BLUE}[*] Connecting to Low Earth Orbit (LEO) Satellites...{NC}")
            time.sleep(2)
            print(f"{GREEN}[+] Signal Intercepted. Local comms disabled.{NC}")
            input(f"\n{WHITE}Press Enter to return...{NC}")
        elif choice == "8":
            print(f"\n{RED}[*] Wiping bash history and logs...{NC}")
            time.sleep(1)
            print(f"{RED}[*] Shutting down SALMAN CONTROL OWNER... Goodbye.{NC}")
            break
        else:
            print(f"{RED}[-] Invalid Command!{NC}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Process interrupted by user. Exiting safely...{NC}")
        sys.exit()
  
