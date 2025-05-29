# PentestNetFilter Quick Start Guide

## 🚀 Installation

```bash
# 1. Clone or download the project
cd pentest_netfilter

# 2. Install dependencies (Method 1: Auto installer)
chmod +x install.sh
./install.sh

# OR Method 2: Manual installation
pip3 install --user psutil scapy
```

## 🔥 Basic Usage

### Interactive Mode (Recommended for learning)
```bash
sudo python3 netfilter.py --interactive
```
- Prompts you for each unknown connection
- Great for understanding network behavior
- Shows process names and destinations

### Stealth Mode (For red team operations)
```bash
sudo python3 netfilter.py --stealth
```
- Minimal output, blocks silently
- Uses default rules without prompting
- Perfect for covert operations

### Config-Based Mode
```bash
sudo python3 netfilter.py --config example_rules.json
```
- Uses predefined rules
- No interactive prompts
- Automated filtering

## 📋 Quick Examples

### 1. Learning Mode - See what your tools do
```bash
# Start the filter
sudo python3 netfilter.py --interactive

# In another terminal, run tools
nmap -sS target.com
gobuster dir -u http://target.com
burpsuite
```

### 2. Privacy Mode - Block telemetry
```bash
# Use privacy-focused rules
sudo python3 netfilter.py --config privacy_rules.json
```

### 3. CTF Mode - Selective filtering
```bash
# Create custom rules for CTF challenge
sudo python3 netfilter.py --config ctf_rules.json
```

## 🛠 Customization

### Create Custom Rules
Edit `default_rules.json` or create new config:

```json
{
  "rules": [
    {
      "action": "allow",
      "process": "your_tool",
      "description": "Allow specific tool"
    },
    {
      "action": "block", 
      "destination": "bad.domain.com",
      "description": "Block specific domain"
    }
  ]
}
```

### Rule Types
- **process**: Filter by process name
- **port**: Filter by port number  
- **destination**: Filter by IP/domain
- **protocol**: Filter by TCP/UDP

### Actions
- **allow**: Always permit
- **block**: Always deny
- **prompt**: Ask user interactively

## 🎯 Use Case Examples

### Red Team Assessment
```bash
# Block outbound telemetry while allowing tools
sudo python3 netfilter.py --stealth --config redteam_rules.json
```

### Malware Analysis
```bash
# Control malware network access
sudo python3 netfilter.py --interactive --interface eth0
```

### CTF Competition
```bash
# Quick rule creation during challenges
sudo python3 netfilter.py --interactive
# Use 'R' to remember allowed connections
# Use 'S' to save blocked connections
```

## 🚨 Safety Notes

- Always test in VM first
- Keep SSH (port 22) allowed
- Don't run on production systems
- Use `make clean` to remove iptables rules

## 📊 Monitoring

Check logs and stats:
```bash
# View current stats
tail -f /tmp/netfilter.log

# Clean up rules
make clean
```

## 🔧 Troubleshooting

### Dependencies missing:
```bash
pip3 install --user psutil scapy
```

### Permission denied:
```bash
# Must run as root for packet capture
sudo python3 netfilter.py
```

### Can't reach internet:
```bash
# Clear iptables rules
sudo iptables -F OUTPUT
```

---

**Remember**: This tool is for educational and authorized testing only! 🔥
