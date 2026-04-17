#!/bin/bash
# Flea Flicker NetFilter Launcher - Advanced Stealth Operations
# Easy-to-use launcher for different operation modes

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${PURPLE}"
echo "███████╗██╗     ███████╗ █████╗     ███████╗██╗     ██╗ ██████╗██╗  ██╗███████╗██████╗ "
echo "██╔════╝██║     ██╔════╝██╔══██╗    ██╔════╝██║     ██║██╔════╝██║ ██╔╝██╔════╝██╔══██╗"
echo "█████╗  ██║     █████╗  ███████║    █████╗  ██║     ██║██║     █████╔╝ █████╗  ██████╔╝"
echo "██╔══╝  ██║     ██╔══╝  ██╔══██║    ██╔══╝  ██║     ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗"
echo "██║     ███████╗███████╗██║  ██║    ██║     ███████╗██║╚██████╗██║  ██╗███████╗██║  ██║"
echo "╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝     ╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝"
echo ""
echo "███╗   ██╗███████╗████████╗███████╗██╗██╗  ████████╗███████╗██████╗ "
echo "████╗  ██║██╔════╝╚══██╔══╝██╔════╝██║██║  ╚══██╔══╝██╔════╝██╔══██╗"
echo "██╔██╗ ██║█████╗     ██║   █████╗  ██║██║     ██║   █████╗  ██████╔╝"
echo "██║╚██╗██║██╔══╝     ██║   ██╔══╝  ██║██║     ██║   ██╔══╝  ██╔══██╗"
echo "██║ ╚████║███████╗   ██║   ██║     ██║███████╗██║   ███████╗██║  ██║"
echo "╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝     ╚═╝╚══════╝╚═╝   ╚══════╝╚═╝  ╚═╝"
echo -e "${NC}"
echo -e "${CYAN}Advanced Network Filter with Experimental Evasion${NC}"
echo -e "${YELLOW}Version 3.0 - Flea Flicker Edition${NC}"
echo ""

# Function to show usage
show_usage() {
    echo -e "${GREEN}Usage:${NC}"
    echo -e "  ${CYAN}./launch.sh${NC} [MODE] [OPTIONS]"
    echo ""
    echo -e "${GREEN}Operation Modes:${NC}"
    echo -e "  ${BLUE}demo${NC}           - Safe demo mode (no root required)"
    echo -e "  ${BLUE}basic${NC}          - Basic network filtering"
    echo -e "  ${BLUE}stealth${NC}        - Stealth mode with minimal output"
    echo -e "  ${BLUE}ai-evasion${NC}     - Advanced detection evasion"
    echo -e "  ${BLUE}maximum-stealth${NC} - Maximum stealth with all features"
    echo -e "  ${BLUE}kali${NC}           - Kali Linux optimized rules"
    echo -e "  ${BLUE}redteam${NC}        - Red team operations mode"
    echo ""
    echo -e "${GREEN}Special Modes:${NC}"
    echo -e "  ${PURPLE}ghost${NC}          - Ultimate stealth (blocks analysis/telemetry)"
    echo -e "  ${PURPLE}shadow${NC}        - Red team + evasion + Tor routing"
    echo -e "  ${PURPLE}phantom${NC}       - Maximum stealth + traffic mimicry"
    echo ""
    echo -e "${GREEN}Flea Flicker Modes (Experimental):${NC}"
    echo -e "  ${RED}trick-play${NC}     - Basic MAC spoofing + evasion"
    echo -e "  ${RED}misdirection${NC}   - Advanced MAC rotation + honeypots"
    echo -e "  ${RED}deception${NC}      - Full deception suite"
    echo -e "  ${RED}chaos${NC}          - Maximum chaos - all experimental features"
    echo ""
    echo -e "${GREEN}Configurations:${NC}"
    echo -e "  ${YELLOW}--config FILE${NC}   - Use custom config file"
    echo -e "  ${YELLOW}--interface IF${NC}  - Monitor specific interface"
    echo -e "  ${YELLOW}--interactive${NC}   - Prompt for unknown connections"
    echo ""
    echo -e "${GREEN}Examples:${NC}"
    echo -e "  ${CYAN}./launch.sh demo${NC}                    # Safe testing"
    echo -e "  ${CYAN}./launch.sh ai-evasion${NC}              # Block analysis services"
    echo -e "  ${CYAN}./launch.sh ghost${NC}                   # Ultimate stealth"
    echo -e "  ${CYAN}./launch.sh redteam --interactive${NC}   # Interactive red team mode"
    echo -e "  ${CYAN}./launch.sh trick-play${NC}              # Flea Flicker trick play"
    echo ""
}

# Check dependencies
check_dependencies() {
    echo -e "${YELLOW}[*] Checking dependencies...${NC}"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}[!] Python3 not found${NC}"
        exit 1
    fi
    
    # Check required Python packages
    python3 -c "import psutil, scapy" 2>/dev/null || {
        echo -e "${RED}[!] Missing Python dependencies${NC}"
        echo -e "${YELLOW}[*] Installing dependencies...${NC}"
        pip3 install psutil scapy
    }
    
    echo -e "${GREEN}[+] Dependencies OK${NC}"
}

# Check if running in VM
check_vm_environment() {
    if [ -f "/proc/version" ] && grep -q "VMware\|VirtualBox\|QEMU" /proc/version 2>/dev/null; then
        echo -e "${CYAN}[*] VM environment detected${NC}"
        export VM_MODE=true
    fi
}

# Function to run different modes
run_mode() {
    local mode="$1"
    shift
    local extra_args="$@"
    
    case "$mode" in
        "demo")
            echo -e "${GREEN}[*] Starting Demo Mode${NC}"
            python3 netfilter.py --demo $extra_args
            ;;
        "basic")
            echo -e "${GREEN}[*] Starting Basic Mode${NC}"
            sudo bash -c 'exec -a "[kworker/u2:1]" python3 netfilter.py "$@"' -- $extra_args
            ;;
        "stealth")
            echo -e "${GREEN}[*] Starting Stealth Mode${NC}"
            sudo bash -c 'exec -a "[kworker/u2:1]" python3 netfilter.py "$@"' -- --stealth --stealth-mode basic $extra_args
            ;;
        "ai-evasion")
            echo -e "${GREEN}[*] Starting Evasion Mode${NC}"
            echo -e "${YELLOW}[*] Loading detection evasion rules...${NC}"
            sudo bash -c 'exec -a "[kworker/u2:1]" python3 netfilter.py "$@"' -- --ai-evasion --stealth-mode advanced \
                --config ai_stealth_rules.json $extra_args
            ;;
        "maximum-stealth")
            echo -e "${GREEN}[*] Starting Maximum Stealth Mode${NC}"
            echo -e "${YELLOW}[*] Activating all stealth features...${NC}"
            sudo bash -c 'exec -a "[kworker/u2:1]" python3 netfilter.py "$@"' -- --stealth --stealth-mode maximum \
                --config advanced_stealth_rules.json $extra_args
            ;;
        "kali")
            echo -e "${GREEN}[*] Starting Kali Linux Mode${NC}"
            sudo bash -c 'exec -a "[kworker/u2:1]" python3 netfilter.py "$@"' -- --config kali_rules.json $extra_args
            ;;
        "redteam")
            echo -e "${GREEN}[*] Starting Red Team Mode${NC}"
            sudo bash -c 'exec -a "[kworker/u2:1]" python3 netfilter.py "$@"' -- --config redteam_rules.json $extra_args
            ;;
        "ghost")
            echo -e "${PURPLE}[*] GHOST MODE ACTIVATED${NC}"
            echo -e "${YELLOW}[*] Ultimate stealth - blocking analysis/telemetry${NC}"
            sudo bash -c 'exec -a "[kworker/u2:1]" python3 netfilter.py "$@"' -- --ai-evasion --stealth-mode maximum \
                --config advanced_stealth_rules.json --stealth $extra_args
            ;;
        "shadow")
            echo -e "${PURPLE}[*] SHADOW MODE ACTIVATED${NC}"
            echo -e "${YELLOW}[*] Red team + evasion + Tor routing${NC}"
            # Check if Tor is available
            if command -v tor &> /dev/null; then
                echo -e "${GREEN}[+] Tor service detected${NC}"
                sudo bash -c 'exec -a "[kworker/u2:1]" python3 netfilter.py "$@"' -- --config redteam_rules.json \
                    --ai-evasion --stealth-mode advanced --stealth $extra_args
            else
                echo -e "${RED}[!] Tor not found. Install with: sudo apt install tor${NC}"
                echo -e "${YELLOW}[*] Continuing without Tor routing...${NC}"
                sudo bash -c 'exec -a "[kworker/u2:1]" python3 netfilter.py "$@"' -- --config redteam_rules.json \
                    --ai-evasion --stealth-mode advanced --stealth $extra_args
            fi
            ;;
        "phantom")
            echo -e "${PURPLE}[*] PHANTOM MODE ACTIVATED${NC}"
            echo -e "${YELLOW}[*] Maximum stealth + traffic mimicry${NC}"
            echo -e "${CYAN}[*] Starting background traffic generation...${NC}"
            sudo bash -c 'exec -a "[kworker/u2:1]" python3 netfilter.py "$@"' -- --stealth-mode maximum \
                --config advanced_stealth_rules.json --ai-evasion --stealth $extra_args
            ;;
        "trick-play")
            echo -e "${RED}[*] FLEA FLICKER: TRICK PLAY MODE ACTIVATED${NC}"
            echo -e "${YELLOW}[*] Basic MAC spoofing + evasion tactics${NC}"
            echo -e "${CYAN}[*] Initializing experimental evasion module...${NC}"
            sudo bash -c 'exec -a "[kworker/u2:1]" python3 netfilter.py "$@"' -- --flea-flicker basic \
                --config ai_stealth_rules.json --stealth $extra_args
            ;;
        "misdirection")
            echo -e "${RED}[*] FLEA FLICKER: MISDIRECTION MODE ACTIVATED${NC}"
            echo -e "${YELLOW}[*] Advanced MAC rotation + honeypots${NC}"
            echo -e "${CYAN}[*] Deploying misdirection protocols...${NC}"
            sudo bash -c 'exec -a "[kworker/u2:1]" python3 netfilter.py "$@"' -- --flea-flicker advanced \
                --config advanced_stealth_rules.json --ai-evasion --stealth $extra_args
            ;;
        "deception")
            echo -e "${RED}[*] FLEA FLICKER: DECEPTION MODE ACTIVATED${NC}"
            echo -e "${YELLOW}[*] Full deception suite + Web3 attack simulation${NC}"
            echo -e "${CYAN}[*] Activating all deception protocols...${NC}"
            sudo bash -c 'exec -a "[kworker/u2:1]" python3 netfilter.py "$@"' -- --flea-flicker maximum \
                --config advanced_stealth_rules.json --ai-evasion --stealth $extra_args
            ;;
        "chaos")
            echo -e "${RED}[*] FLEA FLICKER: MAXIMUM CHAOS MODE ACTIVATED${NC}"
            echo -e "${YELLOW}[*] WARNING: ALL EXPERIMENTAL FEATURES ENABLED${NC}"
            echo -e "${RED}[*] MAC rotation, traps, Web3 attacks, MitM feints${NC}"
            echo -e "${CYAN}[*] Entering maximum chaos mode...${NC}"
            sudo bash -c 'exec -a "[kworker/u2:1]" python3 netfilter.py "$@"' -- --flea-flicker chaos \
                --config advanced_stealth_rules.json --ai-evasion --stealth $extra_args
            ;;
        *)
            echo -e "${RED}[!] Unknown mode: $mode${NC}"
            show_usage
            exit 1
            ;;
    esac
}

# Main execution
main() {
    # Check if no arguments provided
    if [ $# -eq 0 ]; then
        show_usage
        exit 0
    fi
    
    # Parse arguments
    local mode="$1"
    shift
    
    # Special cases
    case "$mode" in
        "-h"|"--help"|"help")
            show_usage
            exit 0
            ;;
        "install")
            echo -e "${GREEN}[*] Installing Flea Flicker NetFilter...${NC}"
            chmod +x install.sh
            ./install.sh
            exit 0
            ;;
        "vmware-setup")
            echo -e "${GREEN}[*] Setting up VMware environment...${NC}"
            chmod +x vmware_setup.sh
            ./vmware_setup.sh
            exit 0
            ;;
    esac
    
    # Environment checks
    check_dependencies
    check_vm_environment
    
    # Check if files exist
    if [ ! -f "netfilter.py" ]; then
        echo -e "${RED}[!] netfilter.py not found${NC}"
        exit 1
    fi
    
    # Display current setup
    echo -e "${CYAN}[*] Current Setup:${NC}"
    echo -e "    Mode: ${GREEN}$mode${NC}"
    echo -e "    Directory: ${BLUE}$(pwd)${NC}"
    echo -e "    Args: ${YELLOW}$@${NC}"
    echo ""
    
    # Warning for stealth modes
    case "$mode" in
        "ghost"|"shadow"|"phantom"|"ai-evasion"|"maximum-stealth")
            echo -e "${RED}[!] WARNING: Advanced stealth mode activated${NC}"
            echo -e "${YELLOW}   This will block analysis services and may affect normal browsing${NC}"
            echo -e "${YELLOW}   Press Ctrl+C to cancel, or Enter to continue...${NC}"
            read -t 5 || true
            echo ""
            ;;
        "trick-play"|"misdirection"|"deception"|"chaos")
            echo -e "${RED}[!] FLEA FLICKER: EXPERIMENTAL MODE WARNING${NC}"
            echo -e "${YELLOW}   This mode uses EXPERIMENTAL evasion techniques:${NC}"
            echo -e "${RED}   • MAC address spoofing and rotation${NC}"
            echo -e "${RED}   • Evasion traps and confusion tactics${NC}"
            echo -e "${RED}   • Simulated Web3 attacks and MitM feints${NC}"
            echo -e "${RED}   • Protocol confusion and heuristic manipulation${NC}"
            echo ""
            echo -e "${YELLOW}   These features are for AUTHORIZED TESTING ONLY${NC}"
            echo -e "${YELLOW}   Use only in controlled environments with permission${NC}"
            echo -e "${YELLOW}   Press Ctrl+C to cancel, or Enter to continue...${NC}"
            read -t 10 || true
            echo ""
            ;;
    esac
    
    # Run the mode
    run_mode "$mode" "$@"
}

# Trap Ctrl+C
trap 'echo -e "\n${YELLOW}[*] Shutting down...${NC}"; exit 0' INT

# Run main function
main "$@"
