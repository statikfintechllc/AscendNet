<link rel="stylesheet" type="text/css" href="docs/custom.css">
<div align="center">
  <a
href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE">
    <img src="https://img.shields.io/badge/FAIR%20USE-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Fair Use License"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE">
    <img src="https://img.shields.io/badge/GREMLINGPT%20v1.0.3-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT License"/>
  </a>
</div>

<div align="center">
  <a
href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/WHY_GREMLINGPT.md">
    <img src="https://img.shields.io/badge/Why-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Why"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/WHY_GREMLINGPT.md">
    <img src="https://img.shields.io/badge/GremlinGPT-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT"/>
  </a>
</div>

  <div align="center">
  <a href="https://ko-fi.com/statikfintech_llc">
    <img src="https://img.shields.io/badge/Support-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Support"/>
  </a>
  <a href="https://patreon.com/StatikFinTech_LLC?utm_medium=unknown&utm_source=join_link&utm_campaign=creatorshare_creator&utm_content=copyLink">
    <img src="https://img.shields.io/badge/SFTi-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="SFTi"/>
  </a>
</div>

# GremlinGPT v1.0.3 Linux Service (Systemd)

This unit file installs GremlinGPT as a **persistent autonomous Linux service** that runs without user intervention.

## Features

- ✅ **No user interaction required** - Runs completely autonomously
- ✅ **Proper conda environment activation** - Uses bash with conda profile sourcing
- ✅ **Comprehensive environment setup** - All necessary env vars configured
- ✅ **Robust restart handling** - Graceful shutdown with 30s timeout
- ✅ **Journal logging** - Logs to systemd journal for easy monitoring
- ✅ **Network dependency** - Waits for network before starting

## Setup Path

```bash
GremlinGPT/systemd/gremlin.service
```

⸻

## Install the Service

**Option 1: Automatic (Recommended)**
Run the install script which will configure everything automatically:
```bash
./install.sh
```

**Option 2: Manual Installation**

1. Copy service file to systemd:
```bash
sudo cp systemd/gremlin.service /etc/systemd/system/
```

2. Edit the service file to match your paths:
```bash
sudo nano /etc/systemd/system/gremlin.service
# Update WorkingDirectory, User, Group, and paths to match your setup
```

3. Reload systemd and enable on boot:
```bash
sudo systemctl daemon-reexec && \
sudo systemctl daemon-reload && \
sudo systemctl enable gremlin
```

4. Start the service:
```bash
sudo systemctl start gremlin
```

⸻

Check Runtime Status
```bash
sudo systemctl status gremlin
```

View Logs
```bash
journalctl -u gremlin -n 50 --no-pager
```

Restart the Kernel Manually
```bash
sudo systemctl restart gremlin
```

⸻

Recovery After Reboot

Gremlin automatically runs:
```bash
python3 core/loop.py
```

⸻

Which:
	•	Resumes FSM agent loop
	•	Watches for retrain triggers
	•	Monitors code diffs
	•	Logs events + reward scores

⸻

Notes
	•	Be sure to set the correct User and WorkingDirectory in gremlin.service
	•	It is recommended to run reboot_recover.sh inside the loop for full restore mode
