# System Overview: Mobile Developer

---

### Executive Summary

**Mobile Developer** enables secure, on-demand remote coding from any mobile device, directly on your home/server machine. With one-click tunnel creation, instant QR mobile onboarding, and seamless HTTPS VSCode (code-server) delivery, you can develop and deploy as if you’re sitting at your desk—no matter where you are.

---

## 1. Problem

Developers increasingly need secure, real-time access to their coding environment from anywhere—traveling, commuting, or working outside the office. Current “remote dev” options are often clunky, insecure, or difficult to configure, especially for mobile.

---

## 2. Solution

Mobile Developer automates the setup and lifecycle of a private mobile dev tunnel:

- **Tailscale** creates a secure, peer-to-peer VPN tunnel between your phone and home/server.
- **code-server** serves the full VSCode IDE (with HTTPS) to your device.
- **CLI UI** provides easy controls and QR onboarding.
- **Self-signed certs** ensure end-to-end encryption even on untrusted networks.

---

## 3. Architecture & Pipeline

#### **A. Tailscale**

- Provides a private, device-to-device WireGuard VPN mesh.
- Ensures traffic between your phone and server never leaves encrypted channels.
- Mobile onboarding is trivial via the Tailscale app and QR code login.

#### **B. code-server**

- Spins up a VSCode IDE on your server, accessible over HTTPS (`0.0.0.0:8888` by default).
- Uses self-signed certificates (generated if missing) to force encrypted access.
- Runs under your user, logs to `~/code-server.log`, never exposes to public internet.

#### **C. QR Onboarding**

- After launch, a QR code with the Tailscale VPN IP + HTTPS port is displayed in the terminal.
- Scan it on your phone—immediate, direct access to your home VSCode from anywhere.

#### **D. Desktop Entry**

- One-click “Mobile Developer” icon is installed to your system dash.
- Clicking opens the menu/CLI: Start or Stop the tunnel, Check Logs, Exit, and Uninstall from within your remote dev CLI terminal.

---

## 4. Lifecycle Flow

### Startup (`start_all.sh`)
1. **Enable and start Tailscale daemon.**
2. **Bring up Tailscale:** Auth via browser if not yet connected.
3. **Fetch VPN IP:** Pick primary Tailscale IPv4.
4. **Generate HTTPS certs** if missing.
5. **Launch code-server** (HTTPS, specified port).
6. **Show QR code** for direct mobile access.

### Shutdown (`stop_all.sh`)
1. Kill all code-server processes on the target port.
2. Stop Tailscale and kill residual tunnels/processes.
3. Clean up stale tunnel interfaces (`tailscale0`).

---

## 5. Security Model

- **No open ports to public internet**: Access is strictly via Tailscale private IPs.
- **End-to-end encryption**: Both VPN (WireGuard) and HTTPS (self-signed cert).
- **Ephemeral access**: Stop_all kills all tunnels, clears interfaces.
- **Process cleanup**: No zombies, no leaked ports.

---

## 6. Key Benefits

- **Zero config for users**: Just run `install.sh`, then use the app icon or scripts.
- **Ultra-portable**: Works on Ubuntu, Debian, most Linux desktops, and any iOS/Android with Tailscale app.
- **No cloud, no vendor lock-in**: 100% local, you control your environment.
- **Instant onboarding**: QR code means no typing URLs or IPs.
- **Battle-tested for devs**: Designed for robust restarts, multiple runs, and busy real-life usage.

---

## 7. How It Works: Developer Journey

1. **Install:** Clone repo, run `env/install.sh`. Everything needed is set up, including a desktop icon.
2. **Start Remote Tunnel:** Click “Mobile Developer” in your app menu or run `start_all.sh`. Scan the QR code on your phone.
3. **Code from Anywhere:** Full VSCode, live on your phone, backed by your home machine’s compute/storage.
4. **Stop (Cleanup):** Stop everything with one click (`stop_all.sh`)—nothing remains running or exposed.

---

## 8. Extensibility

- Swap code-server for other local web services (Jupyter, RStudio, etc) via script mods.
- Add 2FA, automatic cert trust for advanced users.
- Integrate with other VPN providers as needed (see `apt.txt` for expansion).
- Extend mobile_dev_cli.sh with more controls (restart, status, logs).

---

## 9. Dependencies

- Ubuntu/Debian system
- Tailscale (VPN)
- code-server (VSCode in browser)
- openssl, qrencode, whiptail (for full experience)

---

## 10. Troubleshooting

- **If code-server is inaccessible:** Confirm both the server and phone are connected to the same Tailscale tailnet and that code-server is running.
- **Certificate warnings:** Expected, accept the warning or trust the cert manually for a smoother experience.
- **QR code won’t scan:** The IP in the code must match your Tailscale address; run `tailscale ip -4` to verify.

---

*For full folder layout and script details, see the [STRUCTURE.md](https://github.com/statikfintechllc/Mobile-Developer/blob/master/STRUCTURE.md)

## Mobile-Developer: Mobile-Mirror
```text
Mobile-Developer: Mobile-Mirror/
│
├── mobile-mirror/ # 🔥 New Subsystem
│   ├── backend/
│   │   ├── app.py
│   │   ├── screen_streamer.py
│   │   ├── file_ops.py
│   │   ├── terminal_bridge.py
│   │   ├── mouse_input.py
│   │   └── utils/
│   │       ├── auth.py
│   │       ├── qr_generator.py
│   │       └── logger.py
│   ├── frontend/
│   │   ├── public/
│   │   │   └── manifest.json
│   │   └── src/
│   │       ├── App.jsx
│   │       ├── Terminal.jsx
│   │       ├── Editor.jsx
│   │       ├── FileManager.jsx
│   │       ├── ScreenView.jsx
│   │       ├── MouseController.js
│   │       └── api.js
│   ├── config/
│   │   ├── system.toml
│   │   └── tailscale_setup.sh
│   └── start_touchcore.sh     # 👈 Optional standalone start script       
```

> Coming Soon. Like, Now?

---

> *Built to let you *actually* code on the move. No cloud. No lock-in. No bullshit.*

*StatikFinTech, LLC*
