#!/bin/bash

# PentestNetFilter VMware Setup Script
# Run this once in your Kali Linux VM after setting up the shared folder

echo "🔥 PentestNetFilter VMware Shared Folder Setup"
echo "=============================================="

# Check if we're in a VMware environment
if [ ! -d "/mnt/hgfs" ]; then
    echo "[!] VMware shared folders not detected"
    echo "    Make sure VMware Tools is installed and shared folders are enabled"
    echo "    Run: sudo apt install open-vm-tools open-vm-tools-desktop"
    exit 1
fi

# Find the shared folder
SHARED_FOLDER=""
if [ -d "/mnt/hgfs/pentest_netfilter" ]; then
    SHARED_FOLDER="/mnt/hgfs/pentest_netfilter"
elif [ -d "/mnt/shared/pentest_netfilter" ]; then
    SHARED_FOLDER="/mnt/shared/pentest_netfilter"
else
    echo "[!] PentestNetFilter shared folder not found"
    echo "    Expected: /mnt/hgfs/pentest_netfilter or /mnt/shared/pentest_netfilter"
    echo "    Check your VMware shared folder configuration"
    exit 1
fi

echo "[+] Found shared folder: $SHARED_FOLDER"

# Create convenience symlink
if [ ! -L "/opt/netfilter" ]; then
    echo "[+] Creating symlink /opt/netfilter -> $SHARED_FOLDER"
    sudo ln -s "$SHARED_FOLDER" /opt/netfilter
fi

# Make scripts executable (required after copying from host)
echo "[+] Making scripts executable..."
chmod +x "$SHARED_FOLDER"/*.sh "$SHARED_FOLDER"/*.py 2>/dev/null

# Check and install dependencies
echo "[+] Checking dependencies..."

# Check Python dependencies
if ! python3 -c "import psutil" &>/dev/null; then
    echo "[+] Installing psutil..."
    pip3 install --user psutil
fi

if ! python3 -c "import scapy" &>/dev/null; then
    echo "[+] Installing scapy..."
    pip3 install --user scapy
fi

# Create convenience aliases
BASHRC="$HOME/.bashrc"
if ! grep -q "netfilter aliases" "$BASHRC"; then
    echo "" >> "$BASHRC"
    echo "# PentestNetFilter aliases" >> "$BASHRC"
    echo "alias netfilter='cd $SHARED_FOLDER'" >> "$BASHRC"
    echo "alias nf='sudo python3 $SHARED_FOLDER/netfilter.py'" >> "$BASHRC"
    echo "alias nf-demo='python3 $SHARED_FOLDER/demo.py --demo'" >> "$BASHRC"
    echo "alias nf-status='sudo python3 $SHARED_FOLDER/netfilter.py --help'" >> "$BASHRC"
    echo "[+] Added convenience aliases to ~/.bashrc"
fi

# Create quick start scripts
mkdir -p "$HOME/bin"

# Interactive mode script
cat > "$HOME/bin/start-netfilter" << 'EOF'
#!/bin/bash
echo "🔥 Starting PentestNetFilter (Interactive Mode)..."
cd /opt/netfilter
sudo python3 netfilter.py --interactive
EOF

# Stealth mode script
cat > "$HOME/bin/stealth-netfilter" << 'EOF'
#!/bin/bash
echo "👻 Starting PentestNetFilter (Stealth Mode)..."
cd /opt/netfilter
sudo python3 netfilter.py --stealth &
NETFILTER_PID=$!
echo "Netfilter running in background (PID: $NETFILTER_PID)"
echo "Log: tail -f /tmp/netfilter.log"
echo "Stop: sudo pkill -f netfilter.py"
EOF

# Kali-optimized mode script
cat > "$HOME/bin/kali-netfilter" << 'EOF'
#!/bin/bash
echo "🗡️ Starting PentestNetFilter (Kali Optimized)..."
cd /opt/netfilter
sudo python3 netfilter.py --config kali_rules.json --interactive
EOF

# Make scripts executable
chmod +x "$HOME/bin/"*netfilter

echo ""
echo "✅ Setup Complete!"
echo ""
echo "🚀 Quick Start Commands:"
echo "  start-netfilter     - Interactive mode"
echo "  stealth-netfilter   - Background stealth mode"
echo "  kali-netfilter      - Kali-optimized rules"
echo "  netfilter          - Navigate to folder"
echo "  nf --help          - Show all options"
echo ""
echo "📂 Project Location:"
echo "  Shared folder: $SHARED_FOLDER"
echo "  Symlink: /opt/netfilter"
echo ""
echo "🔄 To apply aliases in current session:"
echo "  source ~/.bashrc"
echo ""
echo "💡 Next steps:"
echo "  1. source ~/.bashrc"
echo "  2. start-netfilter"
echo "  3. Run your pentest tools in another terminal"
