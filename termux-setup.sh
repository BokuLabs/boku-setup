#!/data/data/com.termux/files/usr/bin/bash
# ─── Termux Quick Setup for BokuLabs ───
# Run: curl -sL https://raw.githubusercontent.com/BokuLabs/infra/master/termux-setup.sh | bash

echo "╔╗ ┌─┐┌─┐┬ ┬  Termux Setup"
echo "╠╩╗│ ││ ┬│││  ─────────────"
echo "╚═╝└─┘└─┘└┴┘"

# Update packages
echo "[1/5] Updating packages..."
pkg update -y && pkg upgrade -y

# Install essentials
echo "[2/5] Installing essentials..."
pkg install -y python git curl

# Install pip packages
echo "[3/5] Installing Python packages..."
pip install --upgrade pip
pip install colorama beautifulsoup4 lxml httpx requests

# Clone setup repo
echo "[4/5] Cloning setup scripts..."
cd $HOME
if [ -d "boku-setup" ]; then
    cd boku-setup && git pull
else
    # Need token first
    echo ""
    echo "Enter your GitHub PAT (Personal Access Token):"
    echo "Create one at: https://github.com/settings/tokens"
    echo "Required scope: repo"
    echo ""
    read -p "Token: " TOKEN
    
    if [ -z "$TOKEN" ]; then
        echo "[!] No token provided. Exiting."
        exit 1
    fi
    
    git clone https://BokuLabs:${TOKEN}@github.com/BokuLabs/boku-setup.git $HOME/boku-setup
    cd $HOME/boku-setup
fi

# Run setup
echo "[5/5] Running setup..."
python3 setup.py

echo ""
echo "Done! Quick commands:"
echo "  cd ~/DorkParse && python3 main.py"
echo "  cd ~/Tempmail-CloudFlare && python3 bot.py"
