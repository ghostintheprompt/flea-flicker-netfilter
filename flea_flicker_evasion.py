#!/usr/bin/env python3
"""
Flea Flicker NetFilter - Experimental Evasion Module
Advanced deception and misdirection capabilities for pentesting
Named after the football trick play - unexpected misdirection
"""

import random
import time
import subprocess
import threading
import json
import socket
import struct
import uuid
from datetime import datetime
import hashlib
import requests

class FleaFlickerEvasion:
    """Experimental evasion techniques and deception capabilities"""
    
    def __init__(self):
        self.mac_rotation_active = False
        self.ai_trap_active = False
        self.web3_mode = False
        self.mitm_active = False
        self.feint_mode = False
        self.original_mac = self.get_current_mac()
        self.mac_history = []
        self.ai_trap_requests = []
        
    def get_current_mac(self):
        """Get current MAC address"""
        try:
            # Get the primary interface MAC
            result = subprocess.run(['ip', 'link', 'show'], 
                                  capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'link/ether' in line:
                    mac = line.split()[1]
                    return mac
        except:
            pass
        return "00:00:00:00:00:00"
    
    def generate_random_mac(self, vendor_oui=None):
        """Generate a random MAC address with optional vendor OUI"""
        if vendor_oui:
            # Use specific vendor OUI (first 3 bytes)
            mac_bytes = bytes.fromhex(vendor_oui.replace(':', ''))
            mac_bytes += bytes([random.randint(0, 255) for _ in range(3)])
        else:
            # Generate completely random MAC
            mac_bytes = bytes([random.randint(0, 255) for _ in range(6)])
            
        # Set locally administered bit and unicast
        mac_bytes = bytes([mac_bytes[0] | 0x02 & 0xfe]) + mac_bytes[1:]
        
        mac_str = ':'.join([f'{b:02x}' for b in mac_bytes])
        return mac_str
    
    def get_vendor_ouis(self):
        """Common vendor OUIs for realistic MAC spoofing"""
        return {
            'apple': '00:1b:63',
            'cisco': '00:1a:a1', 
            'dell': '00:14:22',
            'hp': '00:1f:29',
            'intel': '00:15:17',
            'microsoft': '00:03:ff',
            'vmware': '00:50:56',
            'virtualbox': '08:00:27',
            'lenovo': '00:21:cc',
            'samsung': '00:16:32'
        }
    
    def instant_mac_change(self, interface='eth0', vendor=None):
        """Instantly change MAC address with one click"""
        try:
            vendors = self.get_vendor_ouis()
            vendor_oui = vendors.get(vendor, None) if vendor else None
            new_mac = self.generate_random_mac(vendor_oui)
            
            # Bring interface down
            subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', interface, 'down'], 
                          capture_output=True)
            
            # Change MAC
            subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', interface, 
                           'address', new_mac], capture_output=True)
            
            # Bring interface up
            subprocess.run(['sudo', 'ip', 'link', 'set', 'dev', interface, 'up'], 
                          capture_output=True)
            
            self.mac_history.append({
                'timestamp': datetime.now().isoformat(),
                'old_mac': self.original_mac,
                'new_mac': new_mac,
                'vendor': vendor or 'random'
            })
            
            print(f"🎭 MAC flicker: {new_mac} ({vendor or 'random'})")
            return new_mac
            
        except Exception as e:
            print(f"[!] MAC change failed: {e}")
            return None
    
    def start_mac_noise(self, interface='eth0', interval=30):
        """Start continuous MAC address rotation (noise mode)"""
        self.mac_rotation_active = True
        
        def mac_noise_worker():
            vendors = list(self.get_vendor_ouis().keys())
            
            while self.mac_rotation_active:
                try:
                    # Random vendor for realistic appearance
                    vendor = random.choice(vendors + [None, None])  # 33% random, 66% vendor
                    self.instant_mac_change(interface, vendor)
                    
                    # Random interval for unpredictability
                    noise_interval = random.uniform(interval * 0.5, interval * 1.5)
                    time.sleep(noise_interval)
                    
                except Exception as e:
                    print(f"[!] MAC noise error: {e}")
                    time.sleep(interval)
        
        thread = threading.Thread(target=mac_noise_worker, daemon=True)
        thread.start()
        print(f"🎪 MAC noise started - rotating every ~{interval}s")
    
    def stop_mac_noise(self):
        """Stop MAC address rotation"""
        self.mac_rotation_active = False
        print("🛑 MAC noise stopped")
    
    def setup_ai_traps(self):
        """Setup honeypots to confuse AI detection systems"""
        self.ai_trap_active = True
        
        # Create fake processes that look suspicious to AI
        fake_processes = [
            'chrome --disable-web-security --user-data-dir=/tmp/chrome',
            'python3 -c "import socket; s=socket.socket()"',
            'curl -H "User-Agent: sqlmap/1.6.12" http://example.com',
            'ncat -l 4444',
            'python3 -m http.server 8080'
        ]
        
        def ai_trap_worker():
            while self.ai_trap_active:
                try:
                    # Generate fake network activity logs
                    fake_log = {
                        'timestamp': datetime.now().isoformat(),
                        'process': random.choice(fake_processes),
                        'destination': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                        'port': random.choice([22, 80, 443, 4444, 8080, 3389, 1433]),
                        'protocol': random.choice(['TCP', 'UDP']),
                        'fake': True
                    }
                    
                    self.ai_trap_requests.append(fake_log)
                    
                    # Keep only last 100 fake logs
                    if len(self.ai_trap_requests) > 100:
                        self.ai_trap_requests = self.ai_trap_requests[-100:]
                    
                    time.sleep(random.uniform(5, 30))
                    
                except Exception as e:
                    print(f"[!] AI trap error: {e}")
                    time.sleep(10)
        
        thread = threading.Thread(target=ai_trap_worker, daemon=True)
        thread.start()
        print("🕳️  AI traps activated - generating fake suspicious activity")
    
    def stop_ai_traps(self):
        """Stop AI trap generation"""
        self.ai_trap_active = False
        print("🛑 AI traps deactivated")
    
    def web3_attack_simulation(self):
        """Simulate Web3/blockchain attack patterns"""
        self.web3_mode = True
        
        web3_targets = [
            'api.etherscan.io',
            'mainnet.infura.io',
            'api.opensea.io', 
            'api.coinbase.com',
            'api.binance.com',
            'api.uniswap.org'
        ]
        
        web3_patterns = [
            '/api/v1/account/',
            '/v3/ethereum/mainnet',
            '/api/v1/assets',
            '/v2/exchange-rates',
            '/api/v3/ticker/price',
            '/api/v2/pools'
        ]
        
        def web3_worker():
            while self.web3_mode:
                try:
                    target = random.choice(web3_targets)
                    pattern = random.choice(web3_patterns)
                    
                    # Generate fake Web3 requests
                    fake_request = {
                        'timestamp': datetime.now().isoformat(),
                        'target': target,
                        'endpoint': pattern,
                        'method': random.choice(['GET', 'POST']),
                        'user_agent': 'Web3Provider/1.0',
                        'fake_web3': True
                    }
                    
                    print(f"🪙 Web3 feint: {target}{pattern}")
                    time.sleep(random.uniform(10, 60))
                    
                except Exception as e:
                    print(f"[!] Web3 simulation error: {e}")
                    time.sleep(30)
        
        thread = threading.Thread(target=web3_worker, daemon=True)
        thread.start()
        print("🌐 Web3 attack simulation started")
    
    def stop_web3_simulation(self):
        """Stop Web3 attack simulation"""
        self.web3_mode = False
        print("🛑 Web3 simulation stopped")
    
    def setup_mitm_feints(self):
        """Setup fake MitM activity to confuse detection"""
        self.mitm_active = True
        
        def mitm_feint_worker():
            while self.mitm_active:
                try:
                    # Generate fake ARP/DNS activity logs
                    fake_activities = [
                        f"ARP spoofing detected: {self.generate_random_mac()} -> 192.168.1.1",
                        f"DNS request intercepted: facebook.com -> 192.168.1.100",
                        f"SSL certificate mismatch: github.com",
                        f"HTTP traffic captured: 192.168.1.{random.randint(2,254)}"
                    ]
                    
                    activity = random.choice(fake_activities)
                    print(f"🎯 MitM feint: {activity}")
                    
                    time.sleep(random.uniform(15, 45))
                    
                except Exception as e:
                    print(f"[!] MitM feint error: {e}")
                    time.sleep(30)
        
        thread = threading.Thread(target=mitm_feint_worker, daemon=True)
        thread.start()
        print("🕸️  MitM feints activated")
    
    def stop_mitm_feints(self):
        """Stop MitM feint generation"""
        self.mitm_active = False
        print("🛑 MitM feints stopped")
    
    def generate_protocol_confusion(self):
        """Generate confusing protocol patterns"""
        confusion_patterns = [
            # Fake SSH over HTTP
            {'port': 80, 'protocol': 'SSH-2.0-OpenSSH_8.2', 'description': 'SSH over HTTP'},
            # Fake HTTPS over telnet port
            {'port': 23, 'protocol': 'TLS 1.3 ClientHello', 'description': 'HTTPS over telnet'},
            # Fake DNS over unusual ports
            {'port': 8080, 'protocol': 'DNS Query', 'description': 'DNS over HTTP proxy'},
            # Fake VPN over DNS
            {'port': 53, 'protocol': 'OpenVPN', 'description': 'VPN over DNS'}
        ]
        
        for pattern in confusion_patterns:
            print(f"🌀 Protocol confusion: {pattern['description']} on port {pattern['port']}")
    
    def emotional_ai_confusion(self):
        """Generate emotional/psychological patterns to confuse AI analysis"""
        emotional_patterns = [
            "User exhibits frustrated typing patterns",
            "Rapid-fire failed login attempts suggest desperation",
            "Long pauses between commands indicate hesitation",
            "Aggressive port scanning followed by immediate retreat",
            "Erratic timing suggests human emotional state"
        ]
        
        for pattern in emotional_patterns:
            print(f"🧠 Emotional feint: {pattern}")
    
    def quantum_noise_generator(self):
        """Generate quantum-inspired random patterns"""
        # Use system entropy for quantum-like randomness
        entropy = random.SystemRandom()
        
        patterns = []
        for _ in range(10):
            pattern = {
                'quantum_bit': entropy.choice([0, 1]),
                'superposition': entropy.random(),
                'entanglement_id': entropy.randint(1000000, 9999999),
                'measurement_time': datetime.now().isoformat()
            }
            patterns.append(pattern)
        
        print("⚛️  Quantum noise patterns generated")
        return patterns
    
    def flea_flicker_combo(self, interface='eth0'):
        """Execute the ultimate flea flicker - multiple evasion techniques"""
        print("🏈 FLEA FLICKER ACTIVATED!")
        print("=" * 50)
        
        # 1. Instant MAC change
        print("1️⃣  Executing MAC address flicker...")
        self.instant_mac_change(interface, random.choice(['apple', 'cisco', 'dell']))
        
        # 2. Start AI traps
        print("2️⃣  Deploying AI confusion traps...")
        self.setup_ai_traps()
        
        # 3. Protocol confusion
        print("3️⃣  Generating protocol confusion...")
        self.generate_protocol_confusion()
        
        # 4. Emotional patterns
        print("4️⃣  Injecting emotional confusion...")
        self.emotional_ai_confusion()
        
        # 5. Quantum noise
        print("5️⃣  Adding quantum noise...")
        self.quantum_noise_generator()
        
        # 6. Start all background activities
        print("6️⃣  Launching background evasion...")
        self.start_mac_noise(interface, interval=20)
        self.web3_attack_simulation()
        self.setup_mitm_feints()
        
        print("🏈 FLEA FLICKER COMPLETE - Blue team is confused!")
        print("💫 Multiple evasion techniques now active")
    
    def stop_all_evasion(self):
        """Stop all evasion techniques"""
        print("🛑 Stopping all flea flicker activities...")
        self.stop_mac_noise()
        self.stop_ai_traps()
        self.stop_web3_simulation()
        self.stop_mitm_feints()
        print("✅ All evasion techniques stopped")
    
    def get_status(self):
        """Get current status of all evasion techniques"""
        status = {
            'mac_rotation': self.mac_rotation_active,
            'ai_traps': self.ai_trap_active,
            'web3_mode': self.web3_mode,
            'mitm_feints': self.mitm_active,
            'mac_changes': len(self.mac_history),
            'fake_requests': len(self.ai_trap_requests)
        }
        return status

# Quick test/demo
if __name__ == "__main__":
    print("🏈 Flea Flicker NetFilter - Experimental Evasion Module")
    print("=" * 60)
    
    evasion = FleaFlickerEvasion()
    
    print("Current MAC:", evasion.get_current_mac())
    print("Available vendors:", list(evasion.get_vendor_ouis().keys()))
    
    # Demo some capabilities (safe mode)
    print("\n🧪 Demo Mode - Safe Testing:")
    evasion.generate_protocol_confusion()
    evasion.emotional_ai_confusion()
    evasion.quantum_noise_generator()
    
    print(f"\n📊 Status: {evasion.get_status()}")
    print("\n💡 Use 'flea_flicker_combo()' for full evasion suite!")
