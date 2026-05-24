#!/bin/bash

# Y-VOIDSYNDICATE Auto-Installer
# Updated to include PyPhisher

echo "-----------------------------------"
echo "Setting up Y-VOIDSYNDICATE..."
echo "-----------------------------------"

# 1. Update System
echo "[+] Updating Repositories..."
pkg update && pkg upgrade -y

# 2. Install Dependencies
echo "[+] Installing PHP, Python, and Git..."
pkg install php git wget curl python -y

# 3. Setup Cloudflared
if ! command -v cloudflared &> /dev/null
then
    echo "[+] Installing Cloudflared..."
    wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64
    mv cloudflared-linux-arm64 cloudflared
    chmod +x cloudflared
else
    echo "[+] Cloudflared is already installed."
fi

# 4. Setup PyPhisher
echo "[+] Setting up PyPhisher..."
if [ -d "PyPhisher" ]; then
    echo "[!] PyPhisher already exists, skipping..."
else
    git clone https://github.com/KasRoudra/PyPhisher
    cd PyPhisher
    pip install -r requirements.txt
    cd ..
    echo "[+] PyPhisher installed successfully."
fi

echo "-----------------------------------"
echo "Setup Complete!"
echo "Y-VOIDSYNDICATE is ready."
echo "-----------------------------------"

