#!/usr/bin/env python3
"""
PentestNetFilter Demo & Test Script
Quick demonstration of core functionality without requiring root privileges
"""

import json
import sys
import os

def load_rules(config_file="default_rules.json"):
    """Load and display rules from config file"""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config.get('rules', [])
    except Exception as e:
        print(f"Error loading config: {e}")
        return []

def demo_rule_matching():
    """Demonstrate rule matching logic"""
    print("🔥 PentestNetFilter Demo")
    print("=" * 50)
    
    rules = load_rules()
    print(f"Loaded {len(rules)} rules from default_rules.json\n")
    
    # Sample packets to test
    test_packets = [
        {
            'process_name': 'nmap',
            'dst_ip': '192.168.1.1',
            'dst_port': 80,
            'protocol': 'TCP'
        },
        {
            'process_name': 'firefox',
            'dst_ip': 'telemetry.mozilla.org',
            'dst_port': 443,
            'protocol': 'TCP'
        },
        {
            'process_name': 'unknown_app',
            'dst_ip': '8.8.8.8',
            'dst_port': 53,
            'protocol': 'UDP'
        }
    ]
    
    print("Testing packet filtering:")
    print("-" * 30)
    
    for i, packet in enumerate(test_packets, 1):
        print(f"\nTest {i}: {packet['process_name']} -> {packet['dst_ip']}:{packet['dst_port']}")
        
        # Find matching rule
        matched_rule = None
        for rule in rules:
            if rule_matches(rule, packet):
                matched_rule = rule
                break
                
        if matched_rule:
            action = matched_rule['action']
            description = matched_rule.get('description', 'No description')
            print(f"  Result: {action.upper()} - {description}")
        else:
            print(f"  Result: PROMPT - No matching rule found")

def rule_matches(rule, packet_info):
    """Test rule matching logic (simplified version)"""
    # Check process name
    if 'process' in rule and packet_info.get('process_name'):
        if rule['process'].lower() in packet_info['process_name'].lower():
            return True
            
    # Check port
    if 'port' in rule:
        if (rule['port'] == packet_info.get('dst_port') or 
            rule['port'] == packet_info.get('src_port')):
            return True
            
    # Check destination
    if 'destination' in rule:
        if rule['destination'] in packet_info.get('dst_ip', ''):
            return True
            
    # Check protocol
    if 'protocol' in rule:
        if rule['protocol'].upper() == packet_info.get('protocol', '').upper():
            return True
            
    return False

def show_usage():
    """Show usage examples"""
    print("\n" + "=" * 50)
    print("📚 Usage Examples:")
    print("=" * 50)
    
    examples = [
        ("Basic monitoring", "sudo python3 netfilter.py --interactive"),
        ("Stealth mode", "sudo python3 netfilter.py --stealth"),
        ("Custom config", "sudo python3 netfilter.py --config custom_rules.json"),
        ("Specific interface", "sudo python3 netfilter.py --interface eth0"),
        ("View help", "python3 netfilter.py --help")
    ]
    
    for desc, cmd in examples:
        print(f"{desc:20}: {cmd}")
    
    print("\n💡 Pro Tips:")
    print("- Run without sudo first to check dependencies")
    print("- Use --stealth for red team operations")
    print("- Create custom rule files for specific engagements")
    print("- Monitor /var/log/netfilter.log for activity")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_rule_matching()
        show_usage()
    else:
        print("🔥 PentestNetFilter Demo Script")
        print("Run with --demo to see rule matching demonstration")
        print("Or use netfilter.py for the actual network filter")
