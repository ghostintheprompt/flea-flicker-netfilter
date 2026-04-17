# PentestNetFilter Quick Start Guide

## Installation

### Method 1: Automated Installation (Recommended)
```bash
cd pentest_netfilter
chmod +x install.sh
./install.sh
```

### Method 2: Manual Installation
```bash
pip3 install --user psutil scapy
```

## Basic Usage

### Interactive Mode
Recommended for initial tool analysis and learning.
```bash
sudo python3 netfilter.py --interactive
```
- Real-time prompts for unknown connections.
- Identifies process names and destinations.
- Useful for mapping tool behavior.

### Stealth Mode
Designed for red team operations and covert assessments.
```bash
sudo python3 netfilter.py --stealth
```
- Minimal terminal output.
- Silent blocking based on predefined rules.
- Reduces operational footprint.

### Configuration-Based Mode
```bash
sudo python3 netfilter.py --config example_rules.json
```
- Uses predefined JSON rule sets.
- No interactive prompts.
- Ideal for automated environments.

## Common Scenarios

### 1. Tool Behavior Analysis
Monitor exactly what network connections your tools are initiating.
```bash
# Start the filter
sudo python3 netfilter.py --interactive

# Execute tools in another terminal
nmap -sS target.com
gobuster dir -u http://target.com
```

### 2. Telemetry Blocking
Block outbound telemetry and background noise during sensitive engagements.
```bash
sudo python3 netfilter.py --config privacy_rules.json
```

### 3. CTF & Specialized Filtering
Apply focused rule sets for specific competition environments.
```bash
sudo python3 netfilter.py --config ctf_rules.json
```

## Configuration

### Rule Definition
Custom rules can be defined in JSON format:

```json
{
  "rules": [
    {
      "action": "allow",
      "process": "custom_tool",
      "description": "Permit specific binary"
    },
    {
      "action": "block", 
      "destination": "telemetry.service.com",
      "description": "Block specific domain"
    }
  ]
}
```

### Supported Selectors
- **process**: Filter by binary name.
- **port**: Filter by destination port.
- **destination**: Filter by IP address or domain.
- **protocol**: Filter by TCP or UDP.

### Actions
- **allow**: Permit the connection.
- **block**: Deny the connection via iptables.
- **prompt**: Request manual intervention.

## Operational Security (OPSEC)

- **Verification**: Always validate rule sets in a laboratory environment before deployment.
- **Persistence**: Ensure SSH (port 22) remains permitted to prevent lockout on remote systems.
- **Cleanup**: Use `make clean` to flush active iptables rules after operations.

## Troubleshooting

### Permission Issues
Packet capture and firewall manipulation require elevated privileges.
```bash
sudo python3 netfilter.py
```

### Connectivity Loss
If the system loses connectivity due to misconfiguration, flush the rules:
```bash
sudo iptables -F OUTPUT
```

---
**Disclaimer**: This tool is intended for authorized security assessments and educational purposes only.
