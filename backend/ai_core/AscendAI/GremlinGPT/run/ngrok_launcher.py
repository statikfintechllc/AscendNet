# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# !/usr/bin/env python3

"""
GremlinGPT v5 :: Module Integrity Directive

run/ngrok_launcher.py

- Launches and manages Ngrok tunnel for backend server access.
- Pulls configuration from TOML, supports region/subdomain, QR for mobile entry.
- State-of-the-art, no placeholders. Full error handling.
"""

from pyngrok import ngrok, conf
import toml
import qrcode
import os
import sys

# ──────────────── CONFIG LOAD ────────────────
CFG_PATH = os.path.join("config", "config.toml")
if not os.path.exists(CFG_PATH):
    print(f"[NGROK] FATAL: Config not found: {CFG_PATH}")
    sys.exit(1)

try:
    config = toml.load(CFG_PATH)
except Exception as e:
    print(f"[NGROK] FATAL: Failed to parse config: {e}")
    sys.exit(2)

ngrok_cfg = config.get("ngrok", {})
if not ngrok_cfg.get("enabled", False):
    print("[NGROK] Disabled in config.")
    sys.exit(0)

auth = ngrok_cfg.get("authtoken")
region = ngrok_cfg.get("region", "us")
subdomain = ngrok_cfg.get("subdomain") or None

# ──────────────── TUNNEL LAUNCH ────────────────
if auth:
    conf.get_default().auth_token = auth

try:
    # Port detection: try backend.api_port from config, fallback to 8000
    backend_cfg = config.get("backend", {})
    port = int(backend_cfg.get("api_port", 8000))
    tunnel_opts = {"region": region}
    if subdomain:
        tunnel_opts["subdomain"] = subdomain

    public_url = ngrok.connect(port, **tunnel_opts)
    print(f"[NGROK] Public URL: {public_url}")

    # ──────────────── QR OUTPUT ────────────────
    qr_path = os.path.join("run", "ngrok_qr.png")
    img = qrcode.make(str(public_url))
    img.save(qr_path)
    print(f"[NGROK] QR code saved to {qr_path}")

except Exception as e:
    print(f"[NGROK] ERROR: Ngrok tunnel failed: {e}")
    sys.exit(3)
