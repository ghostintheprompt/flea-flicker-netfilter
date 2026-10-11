#!/usr/bin/env python3
"""
Flea Flicker NetFilter Demo & Test Script
Quick demonstration of core functionality without requiring root privileges
"""

import json
import sys
import os

def load_rules(config_file="default_rules.json"):
    """Load and display rules from config file"""
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get('rules', [])
        return []
    except Exception as e:
        print(f"Error loading config: {e}")
        return []

def demo_rule_matching():
    """Demonstrate rule matching logic"""
    print("Flea Flicker NetFilter Demo")
    print("=" * 50)
    
    rules = load_rules()
    if not rules:
        # Fallback to some hardcoded rules if file not found
        rules = [
            {"action": "allow", "process": "nmap", "description": "Nmap scanning"},
            {"action": "block", "destination": "telemetry.mozilla.org", "description": "Block Mozilla telemetry"}
        ]
        
    print(f"Loaded {len(rules)} rules for demonstration\n")
    
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
    """Test rule matching logic.

    Fixed 2026-10-11: this previously used OR semantics (any single
    matching field triggered the rule), which does not match the real
    engine in netfilter.py's PentestNetFilter.rule_matches(), where ALL
    fields present on a rule must match (AND semantics). Under the old
    OR logic a rule like {"port": 443} would match literally any packet
    on port 443 by itself, which happened to produce the same practical
    failure as the real engine's rule-ordering bug (see
    demo_ai_evasion_feature below) but for the wrong reason, and would
    have silently diverged from netfilter.py behavior for any rule
    combining two or more fields.
    """
    # Every field present on the rule must match (AND, not OR).
    if 'process' in rule:
        process_name = packet_info.get('process_name', '')
        if rule['process'].lower() not in process_name.lower():
            return False

    if 'port' in rule:
        if rule['port'] != packet_info.get('dst_port'):
            return False

    if 'destination' in rule:
        if rule['destination'] not in packet_info.get('dst_ip', ''):
            return False

    if 'protocol' in rule:
        if rule['protocol'].upper() != packet_info.get('protocol', '').upper():
            return False

    return True

def demo_ai_evasion_feature():
    """Exercise the actual headline feature: ai_stealth_rules.json's
    33 AI/security-vendor destination blocks plus its scanning-tool
    process blocks. This is the demonstration the original demo.py
    never did, it only ever ran against default_rules.json's 4 generic
    destination blocks with packets that don't collide with anything.

    This function shows the real behavior, including the real bug:
    destination rules only match when something earlier in the rule
    list hasn't already matched first, and in the live netfilter.py
    engine dst_ip is always a raw IP address pulled from the packet's
    IP layer (see handle_packet(): ip_layer.dst) with no DNS/SNI
    resolution anywhere in the codebase, so a rule like
    "*.openai.com" can never match real traffic regardless of order.
    """
    print("\n" + "=" * 50)
    print("AI Evasion Feature Demo (ai_stealth_rules.json)")
    print("=" * 50)

    rules = load_rules("ai_stealth_rules.json")
    print(f"Loaded {len(rules)} rules from the actual headline rule file\n")

    def first_match(packet):
        for rule in rules:
            if rule_matches(rule, packet):
                return rule
        return None

    # Case 1: a real, uncontested block. No port/destination rule earlier
    # in the list can match a non-standard port, so the process-based
    # scanning-tool block at the bottom of the list is reached and fires.
    case1 = {'process_name': 'nmap', 'dst_ip': '45.33.32.156', 'dst_port': 9999, 'protocol': 'TCP'}
    r1 = first_match(case1)
    print("Case 1: nmap scan on an uncommon port (no earlier rule collides)")
    print(f"  Packet: {case1}")
    print(f"  Result: {r1['action'].upper() if r1 else 'NO MATCH'} - {r1.get('description') if r1 else ''}")

    # Case 2: the headline AI-telemetry block, run against a REALISTIC
    # packet, i.e. dst_ip is a raw IP the way the live engine always
    # populates it (ip_layer.dst from scapy, never a hostname). The
    # "*.openai.com" rule cannot match a raw IP, and even before that,
    # the generic "allow port 443" rule (loaded earlier in the file)
    # already wins first, since this script's rule_matches, correctly
    # mirroring netfilter.py, stops at the first match in list order.
    case2_real = {'process_name': 'curl', 'dst_ip': '104.18.7.12', 'dst_port': 443, 'protocol': 'TCP'}
    r2 = first_match(case2_real)
    print("\nCase 2: HTTPS request to an OpenAI-owned IP (realistic packet)")
    print(f"  Packet: {case2_real}")
    print(f"  Result: {r2['action'].upper() if r2 else 'NO MATCH'} - {r2.get('description') if r2 else ''}")
    print("  -> This is the bug: the AI-evasion block never fires because")
    print("     (a) rule 3 ('allow' port 443) matches first in list order, and")
    print("     (b) even without that, dst_ip is a raw IP, not 'api.openai.com',")
    print("         so the destination rule has nothing to match against.")

    # Case 3: isolate whether the destination-matching CODE itself is
    # sound, independent of the two problems above. Synthetic packet:
    # dst_ip is set to a literal hostname string (impossible in real
    # traffic, this never happens outside this isolated check) and the
    # port is moved off 443 so the generic allow rule can't intercept it.
    case3_synthetic = {'process_name': 'curl', 'dst_ip': 'api.openai.com', 'dst_port': 8443, 'protocol': 'TCP'}
    r3 = first_match(case3_synthetic)
    print("\nCase 3: same destination, synthetic hostname-as-dst_ip, non-443 port")
    print("  (isolates the matcher logic itself, not a live-traffic scenario)")
    print(f"  Packet: {case3_synthetic}")
    print(f"  Result: {r3['action'].upper() if r3 else 'NO MATCH'} - {r3.get('description') if r3 else ''}")
    print("  -> Confirms the destination-matching logic is correct in isolation.")
    print("     The feature is defeated by rule ordering and the absence of any")
    print("     hostname-resolution step feeding dst_ip, not by the match code.")


def show_usage():
    """Show usage examples"""
    print("\n" + "=" * 50)
    print("Usage Examples:")
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
    
    print("\nPro Tips:")
    print("- Run without sudo first to check dependencies")
    print("- Use --stealth for red team operations")
    print("- Create custom rule files for specific engagements")
    print("- Monitor /var/log/netfilter.log for activity")

def run_demo():
    """Main entry point for the demo simulation"""
    print("[*] Starting Flea Flicker NetFilter Validation Suite...")
    demo_rule_matching()
    demo_ai_evasion_feature()
    show_usage()
    print("\n[+] Validation suite complete.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
    else:
        print("Flea Flicker NetFilter Demo Script")
        print("Run with --demo to see rule matching demonstration")
        print("Or use netfilter.py for the actual network filter")
