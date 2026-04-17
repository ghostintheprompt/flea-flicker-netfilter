#!/bin/bash

# PentestNetFilter Installation Script
# Installs dependencies and sets up the network filter

set -e

echo "🔥 PentestNetFilter Installation Script"
echo "======================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "[!] Don't run this installation script as root!"
   echo "    Install normally, then run the filter with sudo"
   exit 1
fi

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "[+] Detected Linux system"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "[!] macOS detected - this tool is designed for Linux"
    echo "    Consider using Little Snitch on macOS instead"
    exit 1
else
    echo "[!] Unsupported operating system: $OSTYPE"
    exit 1
fi

# Check for required commands
commands=("python3" "pip3" "iptables" "setcap")
missing_commands=()

for cmd in "${commands[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        missing_commands+=("$cmd")
    fi
done

if [ ${#missing_commands[@]} -ne 0 ]; then
    echo "[!] Missing required commands: ${missing_commands[*]}"
    echo "    Please install them first:"
    echo "    sudo apt update && sudo apt install python3 python3-pip iptables libcap2-bin"
    exit 1
fi

echo "[+] All required commands found"

# Install Python dependencies
echo "[+] Installing Python dependencies..."
pip3 install --user psutil scapy

# Check if we can import the modules
echo "[+] Testing Python dependencies..."
python3 -c "import psutil, scapy" 2>/dev/null || {
    echo "[!] Failed to import Python dependencies"
    echo "    Try: pip3 install --user --upgrade psutil scapy"
    exit 1
}

echo "[+] Python dependencies installed successfully"

# Setup Least-Privilege Deployment using setcap
echo "[+] Setting up least-privilege deployment (granting CAP_NET_ADMIN)..."
PYTHON_BIN=$(readlink -f $(which python3))
sudo setcap cap_net_admin,cap_net_raw+eip "$PYTHON_BIN"
echo "[+] Capabilities granted to $PYTHON_BIN"

# Make the script executable
chmod +x netfilter.py

# Create example configuration
echo "[+] Creating example configuration..."
cat > example_rules.json << 'EOF'
{
  "rules": [
    {
      "action": "allow",
      "process": "nmap",
      "description": "Allow Nmap scanning"
    },
    {
      "action": "allow",
      "process": "burpsuite",
      "description": "Allow Burp Suite traffic"
    },
    {
      "action": "allow",
      "port": 22,
      "description": "Allow SSH connections"
    },
    {
      "action": "allow",
      "port": 53,
      "description": "Allow DNS resolution"
    },
    {
      "action": "allow",
      "port": 80,
      "description": "Allow HTTP traffic"
    },
    {
      "action": "allow",
      "port": 443,
      "description": "Allow HTTPS traffic"
    },
    {
      "action": "block",
      "destination": "telemetry.microsoft.com",
      "description": "Block Microsoft telemetry"
    },
    {
      "action": "prompt",
      "description": "Prompt for unknown connections"
    }
  ],
  "created": "2025-05-28T00:00:00",
  "description": "Example PentestNetFilter configuration"
}
EOF

# Create a simple start script
cat > start_filter.sh << 'EOF'
#!/bin/bash
# Quick start script for PentestNetFilter

echo "🔥 Starting PentestNetFilter..."
echo ""
echo "Choose mode:"
echo "1. Interactive mode (prompt for unknown connections)"
echo "2. Config file mode"
echo "3. Stealth mode (minimal output)"
echo ""
read -p "Choice [1-3]: " choice

case $choice in
    1)
        python3 netfilter.py --interactive
        ;;
    2)
        python3 netfilter.py --config example_rules.json
        ;;
    3)
        python3 netfilter.py --stealth
        ;;
    *)
        echo "Invalid choice. Starting in interactive mode..."
        python3 netfilter.py --interactive
        ;;
esac
EOF

chmod +x start_filter.sh

# Create CTF-specific configuration
echo "[+] Creating CTF-specific configuration..."
cat > ctf_rules.json << 'EOF'
{
  "rules": [
    {
      "action": "allow",
      "process": "nmap",
      "description": "Nmap reconnaissance"
    },
    {
      "action": "allow",
      "process": "masscan",
      "description": "Masscan port scanning"
    },
    {
      "action": "allow",
      "process": "gobuster",
      "description": "Directory/file enumeration"
    },
    {
      "action": "allow",
      "process": "hydra",
      "description": "Password attacks"
    },
    {
      "action": "allow",
      "process": "sqlmap",
      "description": "SQL injection testing"
    },
    {
      "action": "allow",
      "process": "python3",
      "port": 4444,
      "description": "Reverse shell listener"
    },
    {
      "action": "allow",
      "port": 22,
      "description": "SSH access"
    },
    {
      "action": "allow",
      "port": 53,
      "description": "DNS resolution"
    },
    {
      "action": "block",
      "destination": "google-analytics.com",
      "description": "Block analytics tracking"
    },
    {
      "action": "block",
      "destination": "facebook.com",
      "description": "Block social media"
    },
    {
      "action": "prompt",
      "default": "block",
      "description": "Block unknown connections by default"
    }
  ],
  "created": "2025-05-28T00:00:00",
  "description": "CTF-optimized PentestNetFilter configuration"
}
EOF

echo ""
echo "🎉 Installation Complete!"
echo "========================"
echo ""
echo "Quick Start:"
echo "  ./start_filter.sh                    # Interactive start menu"
echo "  python3 netfilter.py --help          # Show all options"
echo ""
echo "Example Usage:"
echo "  python3 netfilter.py --interactive           # Interactive mode"
echo "  python3 netfilter.py --config ctf_rules.json # CTF mode"
echo "  python3 netfilter.py --stealth               # Stealth mode"
echo ""
echo "Configuration Files:"
echo "  example_rules.json  # Basic configuration"
echo "  ctf_rules.json      # CTF-optimized rules"
echo ""
echo "Note: The filter no longer requires sudo thanks to least-privilege deployment (setcap)"
echo ""
echo "Happy hacking! 🔥"
