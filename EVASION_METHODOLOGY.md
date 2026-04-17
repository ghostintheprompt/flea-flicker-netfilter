# Flea Flicker Netfilter: Evasion Methodology

This document details the advanced evasion "physics" behind the logic implemented in the Flea Flicker Netfilter framework. It explains how specific packet manipulations bypass common Intrusion Detection Systems (IDS), Endpoint Detection and Response (EDR) platforms, and AI-based network analysis.

## 1. Deep Packet Inspection (DPI) Obfuscation
### The Problem
Traditional tools generate predictable HTTP and DNS headers. Signature-based IDS like Snort and Suricata monitor for default `User-Agent` strings or specific raw payload matches (like `sqlmap/1.6.12`).

### The Solution (Layer 7 Obfuscation)
Flea Flicker uses `scapy` to intercept packets at the raw layer and dynamically inject benign strings.
*   **Method:** Intercepting outbound HTTP payloads and forcefully rewriting headers (e.g., `User-Agent`) to perfectly match standard Chrome or Safari fingerprints for the specific OS environment.
*   **Result:** Malicious traffic blends seamlessly with standard background OS noise, defeating signature-based DPI.

## 2. JA3 Fingerprint Evasion
### The Problem
Modern EDRs and Network Security Monitors (NSMs) rely heavily on JA3 and JA3S hashes. These hash the TCP Initial Sequence Number (ISN), TCP window sizes, and TLS ClientHello extensions (ciphers, curves) to identify malicious clients regardless of the IP address.

### The Solution (TCP SYN Jitter)
*   **Method:** Upon detecting a `TCP SYN` packet, Flea Flicker artificially randomizes the `TCP.window` size and introduces subtle entropy into the `TCP.seq` (ISN).
*   **Result:** This technique shatters the deterministic nature of the JA3 generation process. Because the TCP parameters change per handshake, the resulting JA3 hash rotates, preventing defenders from grouping the connections to a single threat actor tool.

## 3. Protocol Downgrade Attacks
### The Problem
Encrypted payloads over TLS 1.3 are opaque to defenders but also secure against lateral movement analysis if a Red Team needs to inspect secondary tools.

### The Solution (Forced Fallback)
*   **Method:** Identifying `ClientHello` packets supporting TLS 1.3 and actively dropping or modifying the `supported_versions` extension.
*   **Result:** The connection gracefully downgrades to TLS 1.2 or TLS 1.0, enabling exploitation of known vulnerabilities in legacy cipher suites or allowing simplified active interception on the wire.

## 4. Kernel Log Scrubbing & Process Masquerading
### The Problem
System administrators and audit daemons (like `auditd`) monitor `/var/log/kern.log`, `dmesg`, and `ps aux` for suspicious binary execution and anomalous iptables hook modifications.

### The Solution (Anti-Forensics)
*   **Method:** 
    *   Using Python `subprocess` to continuously parse `dmesg -c` to scrub mentions of the tool.
    *   Utilizing `exec -a "[kworker/u2:1]"` or library-based `prctl()` calls to alter the `argv[0]` process name.
*   **Result:** The Python script appears as an innocuous kernel worker thread, evading surface-level top/ps monitoring while systematically erasing its own audit footprint from the kernel ring buffer.

## 5. Beacon Jitter Simulation
### The Problem
AI-driven anomaly detection models easily identify fixed-interval beacons from C2 infrastructure (e.g., exactly every 60 seconds).

### The Solution (Temporal Chaos)
*   **Method:** The `FleaFlickerEvasion` chaos module injects random sleep intervals (`jitter`) and simulated latency into all outgoing connections.
*   **Result:** The standard deviation of beacon intervals spikes. Statistical algorithms fail to group the traffic as a programmatic beacon, classifying it instead as erratic user browsing behavior.
