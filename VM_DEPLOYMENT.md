# PentestNetFilter VMware Shared Folder Deployment Guide

## 🔧 Setup for macOS Host + Kali Linux VM

### Step 1: Configure VMware Shared Folder

1. **In VMware Fusion (macOS host):**
   ```bash
   # Navigate to your project directory
   cd /path/to/pentest_netfilter
   ```

2. **VMware Settings:**
   - VM Settings → Sharing → Enable shared folders
   - Add folder: `/path/to/pentest_netfilter`
   - Name it: `pentest_netfilter`
   - Enable: "Read/Write" access

### Step 2: Access from Kali Linux VM

```bash
# In your Kali Linux VM, the shared folder will be at:
ls /mnt/hgfs/pentest_netfilter/

# Or sometimes at:
ls /mnt/shared/pentest_netfilter/

# Create a symlink for easier access
sudo ln -s /mnt/hgfs/pentest_netfilter /opt/netfilter
cd /opt/netfilter
```

### Step 3: One-Time Setup in Kali

```bash
# Navigate to the shared folder
cd /mnt/hgfs/pentest_netfilter

# Make scripts executable (needed after copying to Linux)
chmod +x install.sh netfilter.py demo.py

# Install dependencies
./install.sh

# Or manual install
sudo apt update
sudo apt install python3-pip
pip3 install psutil scapy
```

### Step 4: Daily Usage Workflow

```bash
# Quick access alias (add to ~/.bashrc)
echo "alias netfilter='cd /mnt/hgfs/pentest_netfilter'" >> ~/.bashrc
echo "alias nf='sudo python3 /mnt/hgfs/pentest_netfilter/netfilter.py'" >> ~/.bashrc
source ~/.bashrc

# Now you can use:
netfilter                    # Jump to directory
nf --interactive            # Start interactive mode
nf --stealth               # Start stealth mode
nf --config example_rules.json  # Use custom rules
```

## 🎯 Typical Pentest Workflow

### Before Starting an Engagement:
```bash
# 1. Navigate to shared folder
netfilter

# 2. Create engagement-specific rules
cp example_rules.json client_rules.json
nano client_rules.json  # Customize for engagement

# 3. Start monitoring
sudo python3 netfilter.py --config client_rules.json --stealth
```

### During Active Testing:
```bash
# Run your tools normally, netfilter handles the filtering
nmap -sS target.com
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt
sqlmap -u "http://target.com/page?id=1" --dbs

# Check what's being blocked/allowed
tail -f /tmp/netfilter.log
```

### For Red Team Operations:
```bash
# Stealth mode - minimal output, blocks telemetry
sudo python3 netfilter.py --stealth --config redteam_rules.json

# Your C2 traffic and tools work, but blocks attribution
msfconsole
# Your payloads work but OS telemetry is blocked
```

## 📂 Recommended Folder Structure in VM

```bash
# Create a dedicated workspace
mkdir -p ~/pentest_tools/
ln -s /mnt/hgfs/pentest_netfilter ~/pentest_tools/netfilter

# Your workflow becomes:
cd ~/pentest_tools/netfilter
sudo python3 netfilter.py --interactive
```

## ⚡ Quick Start Scripts

Create these in your Kali VM for rapid deployment:

### ~/bin/start-netfilter.sh
```bash
#!/bin/bash
echo "🔥 Starting PentestNetFilter..."
cd /mnt/hgfs/pentest_netfilter
sudo python3 netfilter.py --interactive
```

### ~/bin/stealth-netfilter.sh  
```bash
#!/bin/bash
echo "👻 Starting stealth mode..."
cd /mnt/hgfs/pentest_netfilter
sudo python3 netfilter.py --stealth &
echo "Netfilter running in background (PID: $!)"
echo "Use 'sudo pkill -f netfilter.py' to stop"
```

Make them executable:
```bash
chmod +x ~/bin/start-netfilter.sh ~/bin/stealth-netfilter.sh
```

## 🛡️ Security Benefits for VM Usage

1. **Isolation**: Runs in VM, won't affect macOS host
2. **Persistence**: Rules and configs saved to shared folder
3. **Backup**: Automatically synced to macOS host
4. **Version Control**: Can git track from macOS host
5. **Multiple VMs**: Same tool across different Kali instances

## 🔄 Sync Workflow

### Edit on macOS (VS Code/preferred editor):
```bash
# On macOS host
cd /path/to/pentest_netfilter
code example_rules.json  # Edit with VS Code
```

### Use immediately in Kali:
```bash
# In Kali VM - changes are instant
cd /mnt/hgfs/pentest_netfilter
sudo python3 netfilter.py --config example_rules.json
```

## 📊 Monitoring from macOS

You can even monitor logs from your macOS host:
```bash
# On macOS, watch Kali VM logs in real-time  
tail -f /path/to/pentest_netfilter/vm_logs.txt
```

This setup gives you the best of both worlds - comfortable development environment on macOS with full Linux networking capabilities in your Kali VM! 🔥
