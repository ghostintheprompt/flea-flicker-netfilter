# Advanced Stealth Features - Quick Reference

## 🥷 Stealth Mode Overview

PentestNetFilter now includes sophisticated AI detection evasion capabilities designed for high-stakes operations where remaining undetected is critical.

## 🚀 Quick Start Commands

### Basic Usage
```bash
# Safe testing (no root required)
./launch.sh demo

# Basic network filtering
./launch.sh basic

# Enable stealth mode
./launch.sh stealth
```

### AI Detection Evasion
```bash
# Block AI services and security vendors
./launch.sh ai-evasion

# Maximum stealth with all features
./launch.sh maximum-stealth

# Ultimate stealth mode (blocks ALL AI/telemetry)
./launch.sh ghost
```

### Advanced Operations
```bash
# Red team + AI evasion + Tor routing
./launch.sh shadow

# Maximum stealth + traffic mimicry
./launch.sh phantom

# Kali Linux optimized rules
./launch.sh kali

# Red team operations
./launch.sh redteam
```

## 🛡️ Stealth Features

### 1. AI Detection Evasion
- **Blocks**: OpenAI, Microsoft Copilot, Google AI, Anthropic Claude
- **Security Vendors**: CrowdStrike, SentinelOne, Symantec, McAfee, etc.
- **Analytics**: Google Analytics, Facebook tracking, Microsoft telemetry
- **Threat Intelligence**: VirusTotal, Hybrid Analysis, abuse.ch

### 2. Traffic Mimicry
- **Office Worker Pattern**: Regular business hours activity
- **Developer Pattern**: GitHub, Stack Overflow, package repositories
- **Researcher Pattern**: Academic sites, arXiv, research databases

### 3. Timing Obfuscation
- **Human-like delays**: Random intervals between requests
- **Rate limiting**: Prevents automated detection patterns
- **Time restrictions**: Business hours only for certain activities

### 4. Protocol Enhancements
- **DNS over HTTPS**: Encrypted DNS queries
- **TLS fingerprint masking**: Avoid detection by TLS signatures
- **User agent rotation**: Realistic browser identification
- **Tor routing**: Optional routing through Tor network

## 📋 Configuration Files

| File | Purpose | Use Case |
|------|---------|----------|
| `default_rules.json` | General pentest-friendly rules | Basic operations |
| `kali_rules.json` | Kali Linux optimized | Kali VM operations |
| `redteam_rules.json` | Red team operations | Advanced pentesting |
| `ai_stealth_rules.json` | Basic AI evasion | Standard stealth mode |
| `advanced_stealth_rules.json` | Maximum AI evasion | High-stakes operations |

## 🎯 Operation Modes

### Ghost Mode (`./launch.sh ghost`)
- **Purpose**: Ultimate stealth for sensitive operations
- **Features**: Blocks ALL AI services, maximum evasion
- **Use Case**: High-stakes red team engagements

### Shadow Mode (`./launch.sh shadow`)
- **Purpose**: Red team operations with AI evasion
- **Features**: Red team rules + AI blocking + Tor routing
- **Use Case**: Advanced persistent threat simulation

### Phantom Mode (`./launch.sh phantom`)
- **Purpose**: Stealth with traffic camouflage
- **Features**: Maximum stealth + background traffic mimicry
- **Use Case**: Long-term covert operations

## 🔧 Advanced Configuration

### Custom Stealth Rules
Create custom rules in JSON format:
```json
{
  "action": "block",
  "destination": "*.example-ai-service.com",
  "description": "Block custom AI service",
  "category": "ai_evasion"
}
```

### Time-based Restrictions
```json
{
  "action": "allow",
  "port": 22,
  "time_restriction": "business_hours_only",
  "description": "SSH during business hours only"
}
```

### Rate Limiting
```json
{
  "action": "allow",
  "process": "python",
  "rate_limit": "5_requests_per_minute",
  "description": "Rate-limited Python execution"
}
```

## ⚠️ Important Warnings

1. **AI Evasion Impact**: Blocking AI services may affect legitimate applications
2. **Performance**: Traffic mimicry uses additional bandwidth
3. **Detection Risk**: Unusual network patterns may trigger investigation
4. **Legal**: Ensure compliance with applicable laws and regulations

## 🛠️ Troubleshooting

### Stealth Mode Not Working
```bash
# Check if stealth_mode.py exists
ls -la stealth_mode.py

# Verify Python dependencies
python3 -c "import psutil, scapy, requests"

# Run in demo mode for testing
./launch.sh demo
```

### High Resource Usage
```bash
# Disable traffic mimicry
# Edit advanced_stealth_rules.json:
# "fake_legitimate_traffic": false

# Reduce timing obfuscation
# "enable_timing_obfuscation": false
```

### Tor Integration Issues
```bash
# Install Tor
sudo apt install tor

# Start Tor service
sudo systemctl start tor

# Verify Tor is running
curl --socks5-hostname 127.0.0.1:9050 http://check.torproject.org/api/ip
```

## 📚 Further Reading

- `README.md` - Project overview and basic setup
- `QUICKSTART.md` - Detailed installation guide
- `VM_DEPLOYMENT.md` - VMware deployment instructions
- `PROJECT_STRUCTURE.md` - Code organization
- `CONTRIBUTING.md` - Development guidelines

## 🚨 Emergency Stop

To immediately disable all filtering:
```bash
# Kill the process
sudo pkill -f netfilter.py

# Reset iptables (if needed)
sudo iptables -F
sudo iptables -X
```

---

**Remember**: Use these features responsibly and in compliance with all applicable laws and regulations. The advanced stealth capabilities are designed for legitimate security testing and research purposes only.
