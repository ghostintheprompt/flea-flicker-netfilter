# Advanced Stealth & Evasion Reference

## Overview
Flea Flicker NetFilter incorporates advanced detection evasion capabilities designed for security assessments where minimizing the operational footprint is critical. These features target behavioral analysis, heuristic detection, and automated telemetry collection.

## Command Reference

### Standard Execution
```bash
# Diagnostic execution (no root required)
./launch.sh demo

# Standard network filtering
./launch.sh basic

# Basic stealth mode
./launch.sh stealth
```

### Detection Evasion
```bash
# Target analysis services and security vendors
./launch.sh ai-evasion

# Full feature stealth mode
./launch.sh maximum-stealth

# Ultimate evasion (blocks all identified analysis/telemetry endpoints)
./launch.sh ghost
```

### Specialized Operations
```bash
# Red Team ruleset with Tor routing
./launch.sh shadow

# Maximum stealth with background traffic mimicry
./launch.sh phantom

# Kali Linux optimized configuration
./launch.sh kali

# General Red Team operations ruleset
./launch.sh redteam
```

## Evasion Capabilities

### 1. Analysis Endpoint Blocking
- **Identified Services**: OpenAI, Microsoft Copilot, Google AI, Anthropic Claude.
- **Security Infrastructure**: CrowdStrike, SentinelOne, Symantec, McAfee.
- **Telemetry & Analytics**: Google Analytics, Microsoft telemetry, Facebook tracking.
- **Threat Intelligence**: VirusTotal, Hybrid Analysis, abuse.ch.

### 2. Traffic Mimicry
- **Business Profile**: Simulates activity consistent with standard business hours.
- **Development Profile**: Mimics interactions with GitHub, Stack Overflow, and package repositories.
- **Research Profile**: Simulates interaction with academic and technical research databases.

### 3. Timing & Heuristics
- **Jitter & Delays**: Implements non-deterministic intervals between requests to defeat time-series analysis.
- **Rate Limiting**: Constrains connection frequency to avoid threshold-based alerting.
- **Temporal Windows**: Restricts specific activities to predefined time windows (e.g., business hours).

### 4. Protocol & Fingerprint Obfuscation
- **Encrypted DNS**: Implementation of DNS over HTTPS.
- **TLS Fingerprinting**: Obfuscation of TLS ClientHello parameters.
- **User-Agent Management**: Dynamic rotation of realistic browser identities.
- **Proxy Routing**: Optional integration with the Tor network for origin masking.

## Rule Configurations

| Profile | Purpose | Application |
|------|---------|----------|
| `default_rules.json` | General assessment rules | Standard engagements |
| `kali_rules.json` | Kali Linux distribution optimization | Virtualized environments |
| `redteam_rules.json` | Advanced assessment rules | Covert operations |
| `ai_stealth_rules.json` | Standard evasion set | General stealth |
| `advanced_stealth_rules.json` | Comprehensive evasion set | High-assurance operations |

## Operation Mode Details

### Ghost Mode
- **Objective**: Maximum isolation from analysis environments.
- **Primary Feature**: Comprehensive blocking of identified analysis and telemetry endpoints.
- **Scenario**: Sensitive data handling or extreme stealth requirements.

### Shadow Mode
- **Objective**: Advanced assessment with origin masking.
- **Primary Feature**: Red Team ruleset combined with Tor routing.
- **Scenario**: External perimeter testing or APT simulation.

### Phantom Mode
- **Objective**: Behavioral blending.
- **Primary Feature**: Evasion set combined with active traffic mimicry.
- **Scenario**: Long-term internal presence and lateral movement.

## Advanced Configuration

### Custom Evasion Rules
```json
{
  "action": "block",
  "destination": "*.target-service.com",
  "description": "Block specific telemetry endpoint",
  "category": "evasion"
}
```

### Temporal Logic
```json
{
  "action": "allow",
  "port": 22,
  "time_restriction": "business_hours_only",
  "description": "Restrict SSH to business hours"
}
```

## Operational Considerations

1. **Service Disruption**: Blocking analysis services may impact the functionality of specific local applications.
2. **Resource Consumption**: Active traffic mimicry utilizes additional CPU and network bandwidth.
3. **Pattern Detection**: While individual packets are obfuscated, overall network volume may be noted by advanced NDR (Network Detection and Response) systems.

## Emergency Flush
To immediately terminate all filtering and restore original network state:
```bash
# Terminate the process
sudo pkill -f netfilter.py

# Flush active rules
sudo iptables -F
sudo iptables -X
```

---
**Security Notice**: These capabilities are intended for authorized security research and professional assessments only.
