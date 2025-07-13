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

This unit file installs GremlinGPT as a **persistent autonomous Linux service**.

## Setup Path

```bash
GremlinGPT/systemd/gremlin.service
```

⸻

Install the Service
	1.	Copy service file to systemd:
```bash
sudo cp GremlinGPT/systemd/gremlin.service /etc/systemd/system/
```

2.	Reload systemd and enable on boot:
```bash
sudo systemctl daemon-reexec && \
sudo systemctl daemon-reload && \
sudo systemctl enable gremlin
```

3.	Start the service:
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
