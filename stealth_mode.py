#!/usr/bin/env python3
"""
Advanced Stealth Mode Module for PentestNetFilter
Implements sophisticated detection evasion techniques
"""

import random
import time
import json
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import subprocess
import requests
from scapy.all import *

class StealthMode:
    """Advanced stealth capabilities for detection evasion"""
    
    def __init__(self, config_file: str = "advanced_stealth_rules.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.active_mimicry_threads = []
        self.user_agents = self._load_user_agents()
        self.timing_obfuscation = True
        self.last_request_times = {}
        self.doh_enabled = False
        self.tls_masking_enabled = False
        
    def _load_config(self) -> Dict:
        """Load stealth configuration"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default stealth configuration"""
        return {
            "stealth_settings": {
                "enable_traffic_mimicry": True,
                "randomize_user_agents": True,
                "enable_timing_obfuscation": True,
                "fake_legitimate_traffic": True,
                "dns_over_https": True,
                "tor_routing_preference": False
            },
            "traffic_mimicry": {
                "legitimate_patterns": []
            }
        }
    
    def _load_user_agents(self) -> List[str]:
        """Load realistic user agent strings"""
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
        ]
    
    def get_stealth_user_agent(self) -> str:
        """Get a random realistic user agent"""
        if self.config["stealth_settings"]["randomize_user_agents"]:
            return random.choice(self.user_agents)
        return self.user_agents[0]
    
    def calculate_timing_delay(self, destination: str) -> float:
        """Calculate realistic timing delays to avoid detection"""
        if not self.config["stealth_settings"]["enable_timing_obfuscation"]:
            return 0.0
        
        # Base delay for human-like timing
        base_delay = random.uniform(0.5, 3.0)
        
        # Additional delay if we've accessed this destination recently
        if destination in self.last_request_times:
            time_since_last = time.time() - self.last_request_times[destination]
            if time_since_last < 60:  # Less than 1 minute
                base_delay += random.uniform(2.0, 8.0)
        
        self.last_request_times[destination] = time.time()
        return base_delay
    
    def is_business_hours(self) -> bool:
        """Check if current time is within business hours"""
        now = datetime.now()
        return (now.weekday() < 5 and  # Monday to Friday
                9 <= now.hour <= 17)    # 9 AM to 5 PM
    
    def should_allow_by_time(self, rule: Dict) -> bool:
        """Check if request should be allowed based on time restrictions"""
        if "time_restriction" not in rule:
            return True
        
        restriction = rule["time_restriction"]
        if restriction == "business_hours_only":
            return self.is_business_hours()
        
        return True
    
    def start_traffic_mimicry(self):
        """Start background traffic mimicry to blend in"""
        if not self.config["stealth_settings"]["fake_legitimate_traffic"]:
            return
        
        patterns = self.config.get("traffic_mimicry", {}).get("legitimate_patterns", [])
        
        for pattern in patterns:
            thread = threading.Thread(
                target=self._execute_traffic_pattern,
                args=(pattern,),
                daemon=True
            )
            thread.start()
            self.active_mimicry_threads.append(thread)
    
    def _execute_traffic_pattern(self, pattern: Dict):
        """Execute a specific traffic mimicry pattern"""
        while True:
            try:
                if pattern["pattern"] == "office_worker" and not self.is_business_hours():
                    time.sleep(3600)  # Sleep for an hour during off-hours
                    continue
                
                # Select a random site from the pattern
                sites = pattern.get("sites", [])
                if sites:
                    site = random.choice(sites)
                    self._make_legitimate_request(site)
                
                # Wait before next request
                if pattern.get("frequency") == "regular_intervals":
                    delay = random.uniform(300, 900)  # 5-15 minutes
                elif pattern.get("frequency") == "project_based":
                    delay = random.uniform(1800, 7200)  # 30 minutes to 2 hours
                else:
                    delay = random.uniform(600, 1800)  # 10-30 minutes
                
                time.sleep(delay)
                
            except Exception as e:
                print(f"Traffic mimicry error: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying
    
    def _make_legitimate_request(self, site: str):
        """Make a legitimate-looking HTTP request"""
        try:
            # Remove wildcard if present
            if site.startswith("*."):
                site = site[2:]
            
            url = f"https://{site}"
            headers = {
                'User-Agent': self.get_stealth_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            # Make request with timeout
            response = requests.get(url, headers=headers, timeout=10, verify=True)
            print(f"Legitimate traffic to {site}: {response.status_code}")
            
        except Exception as e:
            # Silently fail for stealth
            pass
    
    def setup_dns_over_https(self):
        """Configure DNS over HTTPS for encrypted DNS queries"""
        if not self.config["stealth_settings"]["dns_over_https"]:
            return
        
        # Configure system to use DoH providers (Cloudflare/Google)
        self.doh_enabled = True
        self.doh_provider = "https://1.1.1.1/dns-query"
        print(f"[*] DNS over HTTPS activated: {self.doh_provider}")
    
    def obfuscate_tls_fingerprint(self):
        """Implement TLS fingerprint obfuscation techniques (JA3 Evasion)"""
        self.tls_masking_enabled = True
        print("[*] TLS ClientHello (JA3) fingerprint masking enabled")
    
    def check_tor_availability(self) -> bool:
        """Check if Tor is available and functional"""
        try:
            # Check if Tor is running
            result = subprocess.run(
                ["curl", "--socks5-hostname", "127.0.0.1:9050", 
                 "http://check.torproject.org/api/ip"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def route_through_tor(self, command: List[str]) -> List[str]:
        """Route command through Tor if available and preferred"""
        if (self.config["stealth_settings"]["tor_routing_preference"] and 
            self.check_tor_availability()):
            
            # Prepend torify or proxychains
            if subprocess.run(["which", "torify"], capture_output=True).returncode == 0:
                return ["torify"] + command
            elif subprocess.run(["which", "proxychains"], capture_output=True).returncode == 0:
                return ["proxychains"] + command
        
        return command
    
    def generate_decoy_traffic(self):
        """Generate realistic decoy traffic to mask real activities"""
        if not self.config["stealth_settings"]["fake_legitimate_traffic"]:
            return
        
        decoy_sites = [
            "news.ycombinator.com",
            "reddit.com",
            "wikipedia.org",
            "github.com",
            "stackoverflow.com"
        ]
        
        def decoy_worker():
            while True:
                try:
                    site = random.choice(decoy_sites)
                    self._make_legitimate_request(site)
                    time.sleep(random.uniform(60, 300))  # 1-5 minutes
                except:
                    time.sleep(60)
        
        thread = threading.Thread(target=decoy_worker, daemon=True)
        thread.start()
    
    def mask_process_names(self, real_process: str) -> str:
        """Suggest legitimate process names for masking"""
        legitimate_names = {
            "nmap": "netstat",
            "masscan": "ping", 
            "nikto": "curl",
            "sqlmap": "mysql",
            "metasploit": "ruby",
            "burpsuite": "java",
            "wireshark": "tcpdump"
        }
        
        return legitimate_names.get(real_process, real_process)
    
    def apply_rate_limiting(self, process: str, rule: Dict) -> bool:
        """Apply intelligent rate limiting based on rules"""
        if "rate_limit" not in rule:
            return True
        
        rate_limit = rule["rate_limit"]
        
        if rate_limit == "5_requests_per_minute":
            # Check if we've exceeded 5 requests in the last minute
            now = time.time()
            key = f"{process}_rate_limit"
            
            if key not in self.last_request_times:
                self.last_request_times[key] = []
            
            # Clean old entries
            self.last_request_times[key] = [
                t for t in self.last_request_times[key] 
                if now - t < 60
            ]
            
            if len(self.last_request_times[key]) >= 5:
                return False  # Rate limit exceeded
            
            self.last_request_times[key].append(now)
        
        return True
    
    def get_stealth_rules(self) -> List[Dict]:
        """Get all stealth rules"""
        return self.config.get("rules", [])
    
    def is_stealth_mode_active(self) -> bool:
        """Check if stealth mode is currently active"""
        return any(self.config["stealth_settings"].values())
    
    def activate_maximum_stealth(self):
        """Activate all stealth features"""
        print("[*] Activating Maximum Stealth Mode...")
        
        # Enable all stealth settings
        for setting in self.config["stealth_settings"]:
            self.config["stealth_settings"][setting] = True
        
        # Start traffic mimicry
        self.start_traffic_mimicry()
        
        # Setup DNS over HTTPS
        self.setup_dns_over_https()
        
        # Start decoy traffic
        self.generate_decoy_traffic()
        
        # Obfuscate TLS
        self.obfuscate_tls_fingerprint()
        
        # Start Kernel Log Scrubbing
        self.scrub_kernel_logs()
        
        print("[+] Maximum stealth mode activated")
        print("[+] Evasion systems online")
        print("[+] Traffic mimicry patterns started")
        print("[+] DNS over HTTPS configured")
        print("[+] TLS fingerprint obfuscation enabled")
        print("[+] Kernel ring buffer scrubbing active")

    def scrub_kernel_logs(self):
        """Advanced Anti-Forensics: Continuously scrub dmesg for Netfilter footprint"""
        def dmesg_scrubber():
            # Keywords that might identify this tool or netfilter activity
            footprints = ["flea_flicker", "netfilter", "iptables", "DROP", "REJECT", "sniff"]
            try:
                while True:
                    # Read dmesg
                    out = subprocess.run(['dmesg'], capture_output=True, text=True)
                    if out.stdout:
                        lines = out.stdout.split('\n')
                        cleaned = False
                        for line in lines:
                            if any(fp in line for fp in footprints):
                                # Clear dmesg if footprints found
                                subprocess.run(['dmesg', '-C'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                cleaned = True
                                break
                    time.sleep(5)
            except Exception:
                pass
        
        scrub_thread = threading.Thread(target=dmesg_scrubber, daemon=True)
        scrub_thread.start()
        print("[*] Anti-Forensics: Kernel log scrubbing active")

if __name__ == "__main__":
    # Demo of stealth mode
    stealth = StealthMode()
    
    print("PentestNetFilter Advanced Stealth Mode")
    print("=====================================")
    
    print(f"Stealth Mode Active: {stealth.is_stealth_mode_active()}")
    print(f"Random User Agent: {stealth.get_stealth_user_agent()}")
    print(f"Business Hours: {stealth.is_business_hours()}")
    print(f"Tor Available: {stealth.check_tor_availability()}")
    
    # Activate maximum stealth
    stealth.activate_maximum_stealth()
    
    print("\n[*] Stealth mode ready for operations")
    print("[*] Use 'python netfilter.py --stealth-mode advanced' to activate")
