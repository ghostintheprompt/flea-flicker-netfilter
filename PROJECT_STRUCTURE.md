# Project Architecture & Structure

This document outlines the architectural components and directory layout of the Flea Flicker NetFilter framework.

## Component Overview

### Core Framework
- **`netfilter.py`**: Principal application logic for packet interception, rule processing, and SIEM logging.
- **`stealth_mode.py`**: Advanced module for behavioral obfuscation, traffic mimicry, and anti-forensics.
- **`flea_flicker_evasion.py`**: Experimental module for identity rotation, heuristic manipulation, and protocol feints.

### Configuration Profiles
- **`default_rules.json`**: Baseline assessment ruleset.
- **`kali_rules.json`**: Optimization for Kali Linux environments.
- **`redteam_rules.json`**: Specialized ruleset for covert operations.
- **`ai_stealth_rules.json`**: Baseline detection evasion profile.
- **`advanced_stealth_rules.json`**: Comprehensive evasion profile for high-assurance engagements.

### Deployment & Tooling
- **`Makefile`**: Automation for installation, capability management, and diagnostic execution.
- **`install.sh`**: Provisioning script for Linux environments.
- **`launch.sh`**: Centralized wrapper for framework execution across various operation modes.
- **`vmware_setup.sh`**: Environment preparation for virtualized deployment.
- **`demo.py`**: Non-intrusive diagnostic script for rule validation.

### Documentation
- **`README.md`**: Framework overview and primary entry point.
- **`QUICKSTART.md`**: Rapid deployment and usage guide.
- **`STEALTH_GUIDE.md`**: Technical reference for evasion capabilities.
- **`FLEA_FLICKER_GUIDE.md`**: Manual for experimental evasion features.
- **`VM_DEPLOYMENT.md`**: Guidelines for virtualized environment integration.
- **`EVASION_METHODOLOGY.md`**: Technical analysis of evasion "physics" and IDS bypass logic.

## Standardized Paths

### Virtualized Deployment (VMware)
- **Host System Path**: User-defined local directory.
- **Guest System Mount**: `/mnt/hgfs/pentest_netfilter/`
- **Standardized Alias**: `/opt/netfilter` (established via symbolic link).

### Native Deployment
- **Recommended Location**: `/opt/flea-flicker-netfilter/` or `~/tools/flea-flicker-netfilter/`.

## Operational Integrity
All framework components are designed to be modular. Configuration profiles can be extended or replaced without modification to the core application logic, facilitating rapid adaptation to emerging defensive technologies.
