#!/bin/bash
# Yasir Rahim - Wifiscan Installer

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                YASIR RAHIM WIFISCAN SETUP                  ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}[*] Setting execute permissions for Python scripts...${NC}"
chmod +x yasirfastscan.py
chmod +x yasir_fullscan.py
chmod +x yasit_dragon_scan.py 2>/dev/null

echo -e "${YELLOW}[*] Checking required system tools...${NC}"
# Kali Linux mein iproute2 aur ping pehle se hote hain, 
# lekin doosre OS ke liye check karna best practice hai
sudo apt-get update -y > /dev/null 2>&1
sudo apt-get install iproute2 iputils-ping -y > /dev/null 2>&1

echo -e "${GREEN}[+] Installation Complete! All scripts are ready to use.${NC}\n"

echo -e "To run the Fast Scanner, type:"
echo -e "${CYAN}sudo ./yasirfastscan.py${NC}\n"

echo -e "To run the Full Scanner, type:"
echo -e "${CYAN}sudo ./yasir_fullscan.py${NC}\n"
