#!/usr/bin/env python3
"""
PentestNetFilter - Lightweight Network Filter for Penetration Testing
A hackable alternative to Little Snitch for Linux

Author: PentestNetFilter Contributors
License: MIT
"""

import os
import sys
import json
import time
import signal
import argparse
import threading
import subprocess
import random
import syslog
from datetime import datetime
from collections import defaultdict

try:
    import psutil
    import scapy.all as scapy
    from scapy.layers.inet import IP, TCP, UDP
except ImportError:
    print("Missing dependencies. Install with:")
    print("pip3 install psutil scapy")
    sys.exit(1)

# Import stealth mode if available
try:
    from stealth_mode import StealthMode
    STEALTH_AVAILABLE = True
except ImportError:
    STEALTH_AVAILABLE = False
    print("Note: Advanced stealth mode not available (stealth_mode.py not found)")

# Import Flea Flicker evasion if available
try:
    from flea_flicker_evasion import FleaFlickerEvasion
    FLEA_FLICKER_AVAILABLE = True
except ImportError:
    FLEA_FLICKER_AVAILABLE = False
    print("Note: Experimental Flea Flicker evasion not available (flea_flicker_evasion.py not found)")

class PentestNetFilter:
    def __init__(self, config_file=None, interface="any", stealth=False, stealth_level="basic", flea_flicker_mode=None):
        self.config_file = config_file
        self.interface = interface
        self.stealth = stealth
        self.stealth_level = stealth_level
        self.flea_flicker_mode = flea_flicker_mode
        self.running = False
        self.rules = []
        self.connections = defaultdict(list)
        self.blocked_count = 0
        self.allowed_count = 0
        
        # Initialize stealth mode if available and requested
        self.stealth_mode = None
        if STEALTH_AVAILABLE and (stealth or stealth_level != "basic"):
            self.stealth_mode = StealthMode(stealth_level)
            print(f"[*] Stealth mode initialized: {stealth_level}")
            
        # Initialize Flea Flicker evasion if available and requested
        self.flea_flicker = None
        if FLEA_FLICKER_AVAILABLE and flea_flicker_mode:
            self.flea_flicker = FleaFlickerEvasion()
            self._setup_flea_flicker_mode(flea_flicker_mode)
        
        # Load configuration
        if config_file and os.path.exists(config_file):
            self.load_config()
        else:
            self.load_default_rules()
            
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def load_config(self):
        """Load rules from JSON config file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.rules = config.get('rules', [])
                print(f"[+] Loaded {len(self.rules)} rules from {self.config_file}")
        except Exception as e:
            print(f"[!] Error loading config: {e}")
            self.load_default_rules()
            
    def load_default_rules(self):
        """Load default pentest-friendly rules"""
        self.rules = [
            # Allow common pentest tools
            {"action": "allow", "process": "nmap", "description": "Nmap scanning"},
            {"action": "allow", "process": "masscan", "description": "Masscan scanning"},
            {"action": "allow", "process": "gobuster", "description": "Directory busting"},
            {"action": "allow", "process": "hydra", "description": "Password cracking"},
            {"action": "allow", "process": "sqlmap", "description": "SQL injection"},
            {"action": "allow", "process": "burpsuite", "description": "Burp Suite proxy"},
            {"action": "allow", "process": "msfconsole", "description": "Metasploit"},
            {"action": "allow", "process": "python3", "description": "Python scripts"},
            {"action": "allow", "process": "python", "description": "Python scripts"},
            
            # Allow essential system services
            {"action": "allow", "port": 22, "description": "SSH access"},
            {"action": "allow", "port": 53, "description": "DNS resolution"},
            {"action": "allow", "port": 80, "description": "HTTP traffic"},
            {"action": "allow", "port": 443, "description": "HTTPS traffic"},
            
            # Block suspicious outbound by default (can be overridden)
            {"action": "prompt", "default": "block", "description": "Unknown outbound connections"}
        ]
        
    def _get_stealth_config_file(self):
        """Get appropriate stealth configuration file based on level"""
        stealth_configs = {
            "basic": "ai_stealth_rules.json",
            "advanced": "advanced_stealth_rules.json",
            "maximum": "advanced_stealth_rules.json"
        }
        
        config_file = stealth_configs.get(self.stealth_level, "ai_stealth_rules.json")
        
        # Check if file exists, fallback to basic if not
        if not os.path.exists(config_file):
            config_file = "ai_stealth_rules.json"
            if not os.path.exists(config_file):
                print(f"[!] Warning: Stealth config {config_file} not found")
                return None
        
        return config_file
            
    def get_process_info(self, pid):
        """Get process information from PID"""
        try:
            proc = psutil.Process(pid)
            return {
                'name': proc.name(),
                'exe': proc.exe(),
                'cmdline': ' '.join(proc.cmdline()),
                'cwd': proc.cwd()
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None
            
    def find_process_by_connection(self, src_ip, src_port, dst_ip, dst_port):
        """Find process that owns a network connection"""
        try:
            connections = psutil.net_connections(kind='inet')
            for conn in connections:
                if (conn.laddr.ip == src_ip and conn.laddr.port == src_port and
                    hasattr(conn, 'raddr') and conn.raddr and 
                    conn.raddr.ip == dst_ip and conn.raddr.port == dst_port):
                    return conn.pid
        except Exception as e:
            if not self.stealth:
                print(f"[!] Error finding process: {e}")
        return None
        
    def check_rules_with_stealth(self, packet_info):
        """Enhanced rule checking with stealth mode integration"""
        # First check stealth rules if stealth mode is enabled
        if self.stealth_mode:
            stealth_rules = self.stealth_mode.get_stealth_rules()
            for rule in stealth_rules:
                if self.match_rule(rule, packet_info):
                    return rule
        
        # Then check regular rules
        return self.check_rules(packet_info)
    
    def get_process_name(self, src_port):
        """Get process name from source port"""
        try:
            connections = psutil.net_connections(kind='inet')
            for conn in connections:
                if conn.laddr.port == src_port and conn.pid:
                    proc = psutil.Process(conn.pid)
                    return proc.name()
        except:
            pass
        return "unknown"
    
    def match_rule(self, rule, packet_info):
        """Check if packet matches a specific rule"""
        # Check destination matching
        if 'destination' in rule:
            dest = rule['destination']
            if dest.startswith('*.'):
                domain_suffix = dest[2:]
                if not packet_info['dst_ip'].endswith(domain_suffix):
                    return False
            elif dest != packet_info['dst_ip']:
                return False
        
        # Check port matching
        if 'port' in rule and rule['port'] != packet_info['dst_port']:
            return False
        
        # Check protocol matching
        if 'protocol' in rule and rule['protocol'].upper() != packet_info['protocol']:
            return False
        
        # Check process matching (requires additional lookup)
        if 'process' in rule:
            process_name = self.get_process_name(packet_info['src_port'])
            if rule['process'] != process_name:
                return False
        
        return True
        
    def check_rules(self, packet_info):
        """Check if packet matches any rules"""
        process_info = None
        
        # Get process information if available
        pid = self.find_process_by_connection(
            packet_info['src_ip'], packet_info['src_port'],
            packet_info['dst_ip'], packet_info['dst_port']
        )
        
        if pid:
            process_info = self.get_process_info(pid)
            
        # Check rules in order
        for rule in self.rules:
            if self.rule_matches(rule, packet_info, process_info):
                return rule
                
        return None
        
    def rule_matches(self, rule, packet_info, process_info):
        """Check if a rule matches the current packet/process"""
        # Check process name
        if 'process' in rule:
            if not process_info or rule['process'] not in process_info['name']:
                return False
                
        # Check port
        if 'port' in rule:
            if packet_info['dst_port'] != rule['port']:
                return False
                
        # Check destination IP/domain
        if 'destination' in rule:
            if rule['destination'] not in packet_info['dst_ip']:
                return False
                
        # Check protocol
        if 'protocol' in rule:
            if packet_info['protocol'].lower() != rule['protocol'].lower():
                return False
                
        return True
        
    def log_event(self, action, packet_info, rule=None):
        """SIEM Integration: Log events in CEF format to Syslog"""
        rule_desc = rule.get('description', 'No description') if rule else 'No description'
        cef_log = (f"CEF:0|PentestNetFilter|NetFilter|3.0|{action.upper()}|Network Connection {action.title()}|5|"
                   f"src={packet_info.get('src_ip', '')} spt={packet_info.get('src_port', '')} "
                   f"dst={packet_info.get('dst_ip', '')} dpt={packet_info.get('dst_port', '')} "
                   f"proto={packet_info.get('protocol', '')} msg={rule_desc}")
        try:
            syslog.openlog(ident="flea_flicker", logoption=syslog.LOG_PID, facility=syslog.LOG_AUTH)
            syslog.syslog(syslog.LOG_INFO, cef_log)
        except Exception:
            pass
        return cef_log

    def modify_packet_for_evasion(self, packet):
        """Layer 7 Protocol Awareness: DPI Obfuscation & JA3 Fingerprint Evasion"""
        modified = False
        
        # JA3 Fingerprint Evasion (TCP SYN)
        if packet.haslayer(TCP) and packet[TCP].flags == 'S':
            packet[TCP].window = random.choice([8192, 16384, 29200, 32768, 65535])
            packet[TCP].seq = (packet[TCP].seq + random.randint(1, 100)) & 0xffffffff
            modified = True
            
        # DPI Obfuscation (HTTP/DNS)
        if packet.haslayer(scapy.Raw):
            raw_data = packet[scapy.Raw].load
            try:
                if b"HTTP/" in raw_data and b"User-Agent:" in raw_data:
                    import re
                    stealth_ua = b"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36\r\n"
                    obfuscated_data = re.sub(b"User-Agent:.*?\r\n", stealth_ua, raw_data, flags=re.IGNORECASE)
                    packet[scapy.Raw].load = obfuscated_data
                    modified = True
            except Exception:
                pass

        if modified:
            if packet.haslayer(IP):
                del packet[IP].len
                del packet[IP].chksum
            if packet.haslayer(TCP):
                del packet[TCP].chksum
            elif packet.haslayer(UDP):
                del packet[UDP].chksum
        return packet

    def handle_packet(self, packet):
        """Process intercepted packet with stealth enhancements"""
        if not packet.haslayer(IP):
            return
            
        # Extract packet information
        ip_layer = packet[IP]
        packet_info = {
            'src_ip': ip_layer.src,
            'dst_ip': ip_layer.dst,
            'protocol': 'TCP' if packet.haslayer(TCP) else 'UDP' if packet.haslayer(UDP) else 'OTHER',
            'src_port': packet[TCP].sport if packet.haslayer(TCP) else packet[UDP].sport if packet.haslayer(UDP) else 0,
            'dst_port': packet[TCP].dport if packet.haslayer(TCP) else packet[UDP].dport if packet.haslayer(UDP) else 0,
            'timestamp': datetime.now().isoformat()
        }
        
        # Skip local traffic
        if packet_info['dst_ip'].startswith('127.') or packet_info['dst_ip'].startswith('192.168.'):
            return
            
        # Optional: modify packet dynamically before logic applies
        if self.flea_flicker_mode:
            packet = self.modify_packet_for_evasion(packet)
        
        # Apply stealth mode timing obfuscation
        if self.stealth_mode:
            delay = self.stealth_mode.calculate_timing_delay(packet_info['dst_ip'])
            if delay > 0:
                time.sleep(delay)
            
        # Check rules (including stealth rules if enabled)
        rule = self.check_rules_with_stealth(packet_info)
        
        if rule:
            action = rule['action']
            
            if action == 'allow':
                self.allowed_count += 1
                self.log_event('allow', packet_info, rule)
                
                # Apply stealth modifications for allowed traffic
                if self.stealth_mode:
                    # Check time restrictions
                    if not self.stealth_mode.should_allow_by_time(rule):
                        if not self.stealth:
                            print(f"[TIME_BLOCK] {packet_info['dst_ip']}:{packet_info['dst_port']} - Outside allowed time window")
                        self.block_connection(packet_info)
                        self.log_event('block', packet_info, rule)
                        return
                    
                    # Apply rate limiting
                    process_name = self.get_process_name(packet_info['src_port'])
                    if not self.stealth_mode.apply_rate_limiting(process_name, rule):
                        if not self.stealth:
                            print(f"[RATE_LIMIT] {packet_info['dst_ip']}:{packet_info['dst_port']} - Rate limit exceeded")
                        self.block_connection(packet_info)
                        self.log_event('block', packet_info, rule)
                        return
                
                if not self.stealth:
                    print(f"[ALLOW] {packet_info['dst_ip']}:{packet_info['dst_port']} - {rule.get('description', 'No description')}")
                return
                
            elif action == 'block':
                self.blocked_count += 1
                self.log_event('block', packet_info, rule)
                if not self.stealth:
                    stealth_reason = " (EVASION)" if rule.get('category', '').startswith('ai_') else ""
                    print(f"[BLOCK] {packet_info['dst_ip']}:{packet_info['dst_port']} - {rule.get('description', 'No description')}{stealth_reason}")
                # Implement blocking logic here (iptables rules, etc.)
                self.block_connection(packet_info)
                return
                
            elif action == 'prompt':
                # Interactive mode - ask user
                decision = self.prompt_user(packet_info, rule)
                if decision == 'block':
                    self.block_connection(packet_info)
                    self.log_event('block', packet_info, rule)
                    self.blocked_count += 1
                else:
                    self.log_event('allow', packet_info, rule)
                    self.allowed_count += 1
                return
                
        # Default action - log and allow
        self.allowed_count += 1
        self.log_event('allow', packet_info)
        if not self.stealth:
            print(f"[?] DEFAULT ALLOW: {packet_info['dst_ip']}:{packet_info['dst_port']}")
            
    def block_connection(self, packet_info):
        """Block a network connection using iptables"""
        try:
            # Create iptables rule to drop packets
            cmd = [
                'iptables', '-A', 'OUTPUT',
                '-d', packet_info['dst_ip'],
                '-p', packet_info['protocol'].lower(),
                '--dport', str(packet_info['dst_port']),
                '-j', 'DROP'
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            if not self.stealth:
                print(f"[+] Blocked {packet_info['dst_ip']}:{packet_info['dst_port']} via iptables")
                
        except subprocess.CalledProcessError as e:
            if not self.stealth:
                print(f"[!] Failed to block connection: {e}")
                
    def prompt_user(self, packet_info, rule):
        """Prompt user for decision on connection"""
        print(f"\n[!] NEW CONNECTION DETECTED:")
        print(f"    Destination: {packet_info['dst_ip']}:{packet_info['dst_port']}")
        print(f"    Protocol: {packet_info['protocol']}")
        print(f"    Rule: {rule.get('description', 'No description')}")
        
        while True:
            choice = input("    [A]llow, [B]lock, [R]emember choice: ").lower()
            
            if choice in ['a', 'allow']:
                return 'allow'
            elif choice in ['b', 'block']:
                return 'block'
            elif choice in ['r', 'remember']:
                # Add permanent rule
                new_rule = {
                    'action': input("    Remember as [allow/block]: ").lower(),
                    'destination': packet_info['dst_ip'],
                    'port': packet_info['dst_port'],
                    'description': f"User rule for {packet_info['dst_ip']}:{packet_info['dst_port']}"
                }
                self.rules.insert(0, new_rule)  # Insert at beginning for priority
                return new_rule['action']
            else:
                print("    Invalid choice. Use A, B, or R.")
                
    def start_monitoring(self):
        """Start packet capture and monitoring"""
        print(f"[+] Starting PentestNetFilter on interface {self.interface}")
        print(f"[+] Stealth mode: {'ON' if self.stealth else 'OFF'}")
        print(f"[+] Loaded {len(self.rules)} rules")
        print("[+] Press Ctrl+C to stop\n")
        
        self.running = True
        
        try:
            # Start packet capture
            scapy.sniff(
                iface=self.interface if self.interface != "any" else None,
                prn=self.handle_packet,
                stop_filter=lambda x: not self.running,
                store=0  # Don't store packets in memory
            )
        except PermissionError:
            print("[!] Permission denied. Run as root/sudo for packet capture.")
            sys.exit(1)
        except Exception as e:
            print(f"[!] Error during monitoring: {e}")
            
    def stop_monitoring(self):
        """Stop monitoring and cleanup"""
        self.running = False
        print(f"\n[+] Stopping PentestNetFilter")
        print(f"[+] Statistics: {self.allowed_count} allowed, {self.blocked_count} blocked")
        
        # Cleanup iptables rules if needed
        self.cleanup_iptables()
        
    def cleanup_iptables(self):
        """Remove any iptables rules we created"""
        try:
            # This is a simplified cleanup - in production you'd track specific rules
            subprocess.run(['iptables', '-F', 'OUTPUT'], check=False, capture_output=True)
            if not self.stealth:
                print("[+] Cleaned up iptables rules")
        except Exception as e:
            if not self.stealth:
                print(f"[!] Error cleaning up iptables: {e}")
                
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.stop_monitoring()
        sys.exit(0)
        
    def save_config(self, filename):
        """Save current rules to config file"""
        config = {
            'rules': self.rules,
            'created': datetime.now().isoformat(),
            'description': 'PentestNetFilter configuration'
        }
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
            
        print(f"[+] Configuration saved to {filename}")
    
    def _setup_flea_flicker_mode(self, mode):
        """Setup Flea Flicker evasion based on mode"""
        if not self.flea_flicker:
            return
            
        print(f"🏈 Initializing Flea Flicker {mode.upper()} mode...")
        
        if mode == "basic":
            # Basic MAC spoofing + AI confusion
            self.flea_flicker.change_mac_address()
            self.flea_flicker.start_ai_confusion()
            print("   [+] MAC spoofing activated")
            print("   [+] Evasion tactics enabled")
            
        elif mode == "advanced":
            # Advanced MAC rotation + honeypots
            self.flea_flicker.start_mac_rotation(interval=300)  # 5 minutes
            self.flea_flicker.deploy_ai_traps()
            self.flea_flicker.start_ai_confusion()
            print("   [+] MAC rotation every 5 minutes")
            print("   [+] Trap honeypots deployed")
            print("   [+] Advanced evasion tactics enabled")
            
        elif mode == "maximum":
            # Full deception suite
            self.flea_flicker.start_mac_rotation(interval=120)  # 2 minutes
            self.flea_flicker.deploy_ai_traps()
            self.flea_flicker.start_web3_attacks()
            self.flea_flicker.start_mitm_feints()
            self.flea_flicker.start_ai_confusion()
            print("   [+] Rapid MAC rotation every 2 minutes")
            print("   [+] Trap honeypots with Web3 attacks active")
            print("   [+] MitM feint operations active")
            print("   [+] Maximum evasion protocols active")
            
        elif mode == "chaos":
            # Maximum experimental chaos
            self.flea_flicker.start_mac_rotation(interval=60, noise_mode=True)  # 1 minute + noise
            self.flea_flicker.deploy_ai_traps()
            self.flea_flicker.start_web3_attacks()
            self.flea_flicker.start_mitm_feints()
            self.flea_flicker.start_protocol_confusion()
            self.flea_flicker.start_emotional_ai_confusion()
            self.flea_flicker.start_ai_confusion()
            print("   [!] CHAOS MODE: All experimental features active")
            print("   [+] Continuous MAC noise + rapid rotation")
            print("   [+] Full deception suite active")
            print("   [+] Web3 attack simulation active")
            print("   [+] Protocol confusion active")
            print("   [+] Heuristic manipulation active")

def main():
    parser = argparse.ArgumentParser(description='Flea Flicker NetFilter - Experimental Network Filter for Pentesting')
    parser.add_argument('-c', '--config', help='Configuration file path')
    parser.add_argument('-i', '--interface', default='any', help='Network interface to monitor')
    parser.add_argument('-s', '--stealth', action='store_true', help='Enable stealth mode (minimal output)')
    parser.add_argument('--stealth-mode', choices=['basic', 'advanced', 'maximum'], 
                       default='basic', help='Stealth mode level (default: basic)')
    parser.add_argument('--ai-evasion', action='store_true', 
                       help='Enable detection evasion (implies stealth)')
    parser.add_argument('--flea-flicker', choices=['basic', 'advanced', 'maximum', 'chaos'],
                       help='🏈 Enable experimental Flea Flicker evasion mode')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode (prompt for unknown connections)')
    parser.add_argument('--save-config', help='Save current rules to config file and exit')
    parser.add_argument('--demo', action='store_true', help='Run in demo mode (safe for testing)')
    
    args = parser.parse_args()
    
    # Auto-enable stealth if AI evasion or Flea Flicker is requested
    if args.ai_evasion or args.flea_flicker:
        args.stealth = True
        if args.stealth_mode == 'basic':
            args.stealth_mode = 'advanced'
    
    # Flea Flicker mode warnings
    if args.flea_flicker:
        print("🏈 [!] EXPERIMENTAL FLEA FLICKER MODE ACTIVATED")
        print("   Using advanced evasion techniques for authorized testing only")
    
    # Check if running as root (skip for demo mode)
    if not args.demo and os.geteuid() != 0:
        print("[!] This tool requires root privileges for packet capture and iptables manipulation.")
        print("    Run with: sudo python3 netfilter.py")
        print("    Or use: python3 netfilter.py --demo (for testing)")
        sys.exit(1)
        
    # Create filter instance
    netfilter = PentestNetFilter(
        config_file=args.config,
        interface=args.interface,
        stealth=args.stealth,
        stealth_level=args.stealth_mode,
        flea_flicker_mode=args.flea_flicker
    )
    
    # Activate maximum stealth if requested
    if args.stealth_mode == 'maximum' and netfilter.stealth_mode:
        netfilter.stealth_mode.activate_maximum_stealth()
    
    # Add interactive rule if requested
    if args.interactive:
        netfilter.rules.append({
            'action': 'prompt',
            'description': 'Interactive mode - prompt for all unknown connections'
        })
        
    # Save config and exit if requested
    if args.save_config:
        netfilter.save_config(args.save_config)
        return
    
    # Demo mode
    if args.demo:
        print("[*] Demo Mode - Running safe simulation")
        from demo import run_demo
        run_demo()
        return
        
    # Start monitoring
    try:
        if args.ai_evasion:
            print("[*] Detection Evasion Mode Activated")
            print("[*] Blocking analysis services and security vendors")
            
        if args.flea_flicker:
            print(f"🏈 Flea Flicker {args.flea_flicker.upper()} Mode Active")
            print("[*] Experimental deception and misdirection protocols engaged")
        
        netfilter.start_monitoring()
    except KeyboardInterrupt:
        netfilter.stop_monitoring()

if __name__ == "__main__":
    main()
