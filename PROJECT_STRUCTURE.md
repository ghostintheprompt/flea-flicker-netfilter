# PentestNetFilter Project Structure

This document shows the expected project structure after cloning/downloading.

## 📁 Project Layout

```
pentest_netfilter/
├── README.md                 # Project overview and quick start
├── QUICKSTART.md            # Detailed setup guide  
├── VM_DEPLOYMENT.md         # VMware shared folder guide
├── Makefile                 # Build automation
│
├── netfilter.py            # Main application
├── demo.py                 # Safe testing script
│
├── install.sh              # Linux installation script
├── vmware_setup.sh         # VMware VM setup script
│
├── default_rules.json      # General pentest rules
├── kali_rules.json         # Kali Linux optimized  
├── redteam_rules.json      # Red team operations
└── example_rules.json      # Advanced configuration
```

## 🚀 Setup Paths

### For VMware Shared Folder:
1. **Host Path**: `/path/to/your/pentest_netfilter/`
2. **VM Path**: `/mnt/hgfs/pentest_netfilter/`
3. **Symlink**: `/opt/netfilter` (created by setup script)

### For Native Installation:
1. **Clone to**: `~/tools/pentest_netfilter/`  
2. **Or**: `/opt/pentest_netfilter/`
3. **Scripts in**: `~/bin/` (for easy access)

## 📝 Notes

- All file paths in documentation use generic placeholders
- Replace `/path/to/pentest_netfilter/` with your actual path
- Replace `username` in GitHub URLs with your actual username
- VMware paths may vary by system (`/mnt/hgfs/` vs `/mnt/shared/`)

## 🔧 Customization

Feel free to modify:
- Rule configurations for your specific use cases
- File paths and directory structure  
- GitHub repository URL in documentation
- Author information in headers
