# PentestNetFilter Makefile
# Simplified project management for pentesters

.PHONY: help install demo test clean deps status

help:
	@echo "🔥 PentestNetFilter - Quick Commands"
	@echo "=================================="
	@echo "make install    - Install dependencies and setup"
	@echo "make demo       - Run rule matching demo" 
	@echo "make test       - Test without root privileges"
	@echo "make deps       - Install Python dependencies only"
	@echo "make status     - Show current system status"
	@echo "make clean      - Clean up iptables rules"
	@echo ""
	@echo "🚨 Main Usage (requires sudo):"
	@echo "sudo python3 netfilter.py --interactive"

install:
	@echo "🔧 Installing PentestNetFilter..."
	chmod +x install.sh netfilter.py demo.py
	./install.sh

demo:
	@echo "🎯 Running rule matching demo..."
	python3 demo.py --demo

test:
	@echo "🧪 Testing script functionality..."
	python3 netfilter.py --help || echo "Dependencies needed - run 'make deps'"

deps:
	@echo "📦 Installing Python dependencies..."
	pip3 install --user psutil scapy

status:
	@echo "📊 System Status Check:"
	@echo "Python3: $$(which python3 || echo 'NOT FOUND')"
	@echo "Pip3: $$(which pip3 || echo 'NOT FOUND')"
	@echo "Iptables: $$(which iptables || echo 'NOT FOUND')"
	@echo "Psutil: $$(python3 -c 'import psutil; print("OK")' 2>/dev/null || echo 'NOT INSTALLED')"
	@echo "Scapy: $$(python3 -c 'import scapy; print("OK")' 2>/dev/null || echo 'NOT INSTALLED')"

clean:
	@echo "🧹 Cleaning up iptables rules..."
	@sudo iptables -F OUTPUT 2>/dev/null || echo "No cleanup needed (or no sudo access)"

# Quick start targets
interactive: deps
	@echo "🔥 Starting interactive mode (requires sudo)..."
	sudo python3 netfilter.py --interactive

stealth: deps
	@echo "👻 Starting stealth mode (requires sudo)..."
	sudo python3 netfilter.py --stealth

config: deps
	@echo "⚙️ Starting with custom config (requires sudo)..."
	sudo python3 netfilter.py --config default_rules.json
