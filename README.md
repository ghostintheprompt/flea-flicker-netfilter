# Flea Flicker NetFilter 🏈

A **experimental network filter** for Linux penetration testing with **advanced AI detection evasion** and **deception capabilities** - inspired by the football trick play for maximum misdirection.

> 🏈 **"Just like the Flea Flicker play, success comes from unexpected misdirection and perfect execution"**

## 🚀 Features

### Core Functionality
- **Lightweight**: Minimal resource usage, won't interfere with pentesting
- **Non-intrusive**: Manual start/stop, no annoying startup services
- **Hackable**: Easy to modify and extend for specific engagements
- **Pentest-friendly**: Won't block your tools or break your workflow
- **Real-time monitoring**: See network connections as they happen
- **Rule-based filtering**: Block/allow by process, port, or destination

### 🛡️ Advanced Stealth Features
- **AI Detection Evasion**: Block OpenAI, Microsoft Copilot, Google AI, security vendors
- **Traffic Mimicry**: Generate legitimate-looking background traffic
- **Timing Obfuscation**: Human-like delays to avoid automated detection
- **TLS Fingerprint Masking**: Avoid detection by network signatures  
- **DNS over HTTPS**: Encrypted DNS queries for enhanced privacy
- **Tor Integration**: Optional routing through Tor network

### 🏈 Experimental Flea Flicker Evasion (NEW!)
- **MAC Address Spoofing**: Instant identity changes with vendor-specific OUIs
- **Continuous MAC Rotation**: Automated identity switching with noise mode
- **AI Trap Honeypots**: Deploy fake services to confuse AI detection systems
- **Web3 Attack Simulation**: Simulate DeFi/NFT attacks to create false patterns
- **MitM Feints**: Generate fake man-in-the-middle traffic signatures
- **Protocol Confusion**: Mix protocols to confuse automated analysis
- **Emotional AI Manipulation**: Generate emotional content to confuse sentiment analysis

## 🎯 Operation Modes

### Standard Modes
| Mode | Command | Purpose |
|------|---------|---------|
| 👻 **Ghost** | `./launch.sh ghost` | Ultimate stealth - blocks ALL AI/telemetry |
| 🕴️ **Shadow** | `./launch.sh shadow` | Red team + AI evasion + Tor routing |
| 👤 **Phantom** | `./launch.sh phantom` | Maximum stealth + traffic mimicry |
| 🤖 **AI Evasion** | `./launch.sh ai-evasion` | Block AI services and security vendors |
| 🔧 **Basic** | `./launch.sh basic` | Standard network filtering |

### 🏈 Experimental Flea Flicker Modes
| Mode | Command | Purpose | Risk Level |
|------|---------|---------|------------|
| 🏈 **Trick Play** | `./launch.sh trick-play` | Basic MAC spoofing + AI confusion | ⚠️ Low |
| 🏈 **Misdirection** | `./launch.sh misdirection` | Advanced MAC rotation + honeypots | ⚠️ Medium |
| 🏈 **Deception** | `./launch.sh deception` | Full deception suite + Web3 attacks | ⚠️ High |
| 🏈 **Chaos** | `./launch.sh chaos` | Maximum experimental chaos mode | 🚨 **Extreme** |

## Philosophy

Unlike traditional firewalls that are designed to secure systems, PentestNetFilter is designed for:
- **AI-aware operations**: Evade modern AI-powered security tools
- Learning network behavior during pentests
- Selective traffic blocking without breaking tools
- Quick rule creation for specific scenarios
- Traffic analysis and pattern recognition
- C2 channel protection and evasion testing

## Quick Start

### 🥷 One-Command Stealth Launch
```bash
# Ultimate stealth mode (recommended for sensitive operations)
./launch.sh ghost

# AI detection evasion only
./launch.sh ai-evasion

# Safe testing (no root required)
./launch.sh demo
```

### 🏈 Experimental Flea Flicker Quick Start
```bash
# ⚠️  FOR AUTHORIZED TESTING ONLY ⚠️

# Basic experimental evasion
./launch.sh trick-play      # MAC spoofing + AI confusion

# Advanced deception protocols  
./launch.sh misdirection    # MAC rotation + honeypots

# Maximum experimental chaos (use with extreme caution)
./launch.sh chaos           # ALL experimental features
```

### 🖥️ VMware Shared Folder (Recommended for macOS users)
```bash
# 1. Set up shared folder in VMware Fusion pointing to this directory
# 2. In your Kali Linux VM:
cd /mnt/hgfs/pentest_netfilter
chmod +x vmware_setup.sh
./vmware_setup.sh

# 3. Start filtering with new launcher:
./launch.sh ghost           # Ultimate stealth mode
./launch.sh shadow          # Red team + AI evasion + Tor
./launch.sh phantom         # Maximum stealth + traffic mimicry
./launch.sh trick-play      # 🏈 Basic Flea Flicker mode
./launch.sh chaos           # 🏈 Maximum experimental chaos
./launch.sh kali            # Kali-optimized rules
```

### 🐧 Native Linux Installation
```bash
# Clone and setup
git clone https://github.com/username/pentest-netfilter
cd pentest-netfilter
chmod +x install.sh
sudo ./install.sh

# Start the filter with AI evasion
./launch.sh ai-evasion
```

## 🛡️ Advanced Stealth Capabilities

### AI Detection Evasion
Blocks connections to:
- **AI Services**: OpenAI, Microsoft Copilot, Google AI, Anthropic Claude
- **Security Vendors**: CrowdStrike, SentinelOne, Symantec, McAfee, etc.
- **Analytics**: Google Analytics, Facebook tracking, Microsoft telemetry
- **Threat Intel**: VirusTotal, Hybrid Analysis, abuse.ch

### Traffic Camouflage
- **Legitimate Traffic**: Mimics office worker, developer, or researcher patterns
- **Timing Obfuscation**: Human-like delays between requests
- **User Agent Rotation**: Realistic browser identification
- **DNS over HTTPS**: Encrypted DNS queries

### Special Operation Modes
- **👻 Ghost Mode**: Ultimate stealth - blocks ALL AI/telemetry services
- **🕴️ Shadow Mode**: Red team operations with AI evasion and Tor routing
- **👤 Phantom Mode**: Maximum stealth with background traffic mimicry

## Use Cases

1. **AI-Aware Red Team Operations**: Evade modern AI-powered security tools
2. **Advanced Persistent Threat Simulation**: Long-term covert operations
3. **Malware Analysis**: Control network access during dynamic analysis
4. **CTF Challenges**: Selective filtering for complex scenarios
5. **Research**: Study application network behavior with stealth
6. **Evasion Testing**: Test C2 channel resilience against AI detection

## Why Not Traditional Firewalls?

- **ufw/iptables**: Too complex for quick pentest scenarios, no AI evasion
- **Little Snitch**: macOS only, too heavy for Linux VMs
- **OpenSnitch**: Good but not pentest-optimized, lacks stealth features
- **Commercial solutions**: Expensive, overkill, intrusive

PentestNetFilter fills the gap for security researchers who need something simple, powerful, and hackable.

## 📚 Documentation

- **[STEALTH_GUIDE.md](STEALTH_GUIDE.md)** - Comprehensive guide to advanced stealth features
- **[QUICKSTART.md](QUICKSTART.md)** - Detailed installation and setup instructions  
- **[VM_DEPLOYMENT.md](VM_DEPLOYMENT.md)** - VMware shared folder workflow
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Code organization and files
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development and contribution guidelines

## 🚨 Important Disclaimers

### ⚠️ Experimental Flea Flicker Features Warning
The experimental Flea Flicker evasion capabilities are **CUTTING-EDGE RESEARCH TOOLS** intended for:
- ✅ **Authorized penetration testing**
- ✅ **Security research in controlled environments**  
- ✅ **Red team exercises with proper approval**
- ✅ **Academic cybersecurity research**

**❌ DO NOT USE FOR:**
- Illegal activities or unauthorized access
- Circumventing legitimate security measures without permission
- Any activity that violates local, national, or international law

### 🔬 Experimental Nature
Flea Flicker evasion techniques are **experimental** and may:
- Cause network instability in production environments
- Trigger security alerts and monitoring systems
- Require extensive cleanup after testing
- Have unpredictable interactions with enterprise security tools

**Only use in isolated test environments with proper authorization.**

### 🏈 "The Perfect Flea Flicker"
> *"In football, a Flea Flicker works because the defense expects one thing but gets another. In cybersecurity, the same principle applies - successful evasion comes from unexpected misdirection and perfect execution."*

**Use responsibly. Use ethically. Use effectively.**

---

**🥷 Ready for ghost mode?** Start with `./launch.sh ghost` for ultimate stealth operations.
