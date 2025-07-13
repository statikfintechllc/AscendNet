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

# GremlinGPT v1.0.3 – ngrok Integration Guide

This document explains how `ngrok` is integrated into the GremlinGPT system and how to use it to access your dashboard securely from anywhere — including mobile devices.

---

## What is ngrok?

[`ngrok`](https://ngrok.com) is a secure tunneling service that exposes your **local GremlinGPT dashboard (`localhost:5000` or `:5050`)** to the public internet via HTTPS.

GremlinGPT uses **`pyngrok`** to launch and manage this tunnel automatically as part of the system boot process.

---

## When Is ngrok Used?

- When `[ngrok.enabled] = true` in `config/config.toml`
- Automatically triggered by `run/start_all.sh` and/or `run/ngrok_launcher.py`
- Uses your authtoken for authentication and region selection

---

### 1. Enable ngrok

Edit your ngrok config in:

#### `config/config.toml`
```toml
[ngrok]
enabled = true
authtoken = "YOUR_AUTHTOKEN_HERE"
region = "us"
subdomain = ""  # Optional — requires ngrok Pro
```

⸻

2. Start the System
```bash
cd GremlinGPT/run
./start_all.sh
```

**This will:**
- Launch the backend server
- Start the ngrok tunnel via pyngrok (see run/ngrok_launcher.py)
- Print the live HTTPS URL in the terminal
- Save the URL to:
run/current_ngrok_url.txt

⸻

3.a. Access the Dashboard on Your Phone (Manual)
- Watch for console output like:

```log
[*] NGROK Public URL: https://example.ngrok.io
```

- Open the link on your phone
- Tap “Add to Home Screen” to install the PWA

⸻

3.b. Auto QR Code for Mobile Setup (Automatic)

**When enabled, GremlinGPT will:**
- Auto-generate a scannable QR code
- Save it as:
run/ngrok_qr.png

**How to use:**
- Open run/ngrok_qr.png on your computer
- Scan with your phone’s camera or QR app
- Instantly access the mobile dashboard

⸻

## Output Files

| **File**                    | **Purpose**                                |
|-----------------------------|---------------------------------------------|
| `run/current_ngrok_url.txt` | Live ngrok HTTPS link (public endpoint)     |
| `run/ngrok_qr.png`          | QR code for mobile quick connect            |

⸻

## Troubleshooting

| **Issue**                 | **Fix**                                                                 |
|---------------------------|--------------------------------------------------------------------------|
| QR not generated          | Make sure the `qrcode` Python package is installed                      |
| No URL printed            | Check if ngrok is enabled and authtoken is set/valid in config          |
| QR opens localhost        | Use only the ngrok public HTTPS URL (never localhost)                   |
| ngrok fails to connect    | Ensure internet access and set correct region in config                 |

⸻

## Security & Notes

- ngrok provides HTTPS, so your dashboard is encrypted end-to-end.
- Never share your public ngrok URL with untrusted users.
- The tunnel only stays open while GremlinGPT is running.

⸻

## Summary

With ngrok + QR, you can expose your GremlinGPT system securely to any device:
- No ports to open
- No IP configuration
- No tethering or VPN needed

> Just boot and scan. Your dashboard is always in reach.

