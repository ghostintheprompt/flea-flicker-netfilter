# VMware Shared Folder Deployment Guide

## Deployment Environment: macOS Host & Kali Linux Guest

### 1. Configure VMware Shared Folders

1. **Host Configuration (macOS):**
   Navigate to the project directory on your host system.
   ```bash
   cd /path/to/pentest_netfilter
   ```

2. **VMware Guest Settings:**
   - **Virtual Machine** → **Settings** → **Sharing**.
   - Enable **Shared Folders**.
   - Add the project directory path.
   - Assign the name `pentest_netfilter`.
   - Set permissions to **Read/Write**.

### 2. Access within Guest OS (Kali Linux)

The shared directory is typically mounted at `/mnt/hgfs/`.

```bash
# Verify mount point
ls /mnt/hgfs/pentest_netfilter/

# Establish symbolic link for standardized access
sudo ln -s /mnt/hgfs/pentest_netfilter /opt/netfilter
cd /opt/netfilter
```

### 3. Initial Provisioning

Execute the following commands within the guest OS to prepare the environment:

```bash
cd /opt/netfilter

# Ensure execution permissions
chmod +x install.sh netfilter.py demo.py

# Execute installation script
./install.sh
```

### 4. Operational Workflow

Establish aliases in `~/.bashrc` or `~/.zshrc` for efficient management:

```bash
echo "alias netfilter='cd /opt/netfilter'" >> ~/.bashrc
echo "alias nf='python3 /opt/netfilter/netfilter.py'" >> ~/.bashrc
source ~/.bashrc
```

#### Assessment Scenarios:

**Pre-Engagement Configuration:**
```bash
# Create engagement-specific ruleset
cp example_rules.json project_alpha.json
nano project_alpha.json

# Initiate monitoring
nf --config project_alpha.json --stealth
```

**Covert Operations:**
```bash
# Utilize stealth mode with Red Team ruleset
nf --stealth --config redteam_rules.json
```

### 5. Automated Management Scripts

For rapid deployment, establish the following management scripts:

**`~/bin/nf-interactive`**
```bash
#!/bin/bash
cd /opt/netfilter
python3 netfilter.py --interactive
```

**`~/bin/nf-stealth`**
```bash
#!/bin/bash
cd /opt/netfilter
python3 netfilter.py --stealth &
echo "[+] Netfilter background process initiated (PID: $!)"
```

### 6. Security & Persistence Benefits

- **Environment Isolation**: Execution is restricted to the virtualized environment.
- **Data Persistence**: Configuration changes and logs are preserved on the host filesystem.
- **Version Control Integration**: Git operations can be managed from the host OS while changes are reflected immediately in the guest.
- **Telemetry Masking**: Prevents the guest OS from transmitting telemetry to external vendors during sensitive assessments.

---
**Note**: Ensure that the Python binary has been granted the necessary capabilities (`CAP_NET_ADMIN`, `CAP_NET_RAW`) via the provided installation script or `make setcap` to avoid requirement of root execution.
