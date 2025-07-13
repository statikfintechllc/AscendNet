#!/usr/bin/env bash
# tailscale_setup.sh — One-time tailscale auth flow

set -e

echo "[*] Checking for Tailscale..."
if ! command -v tailscale >/dev/null 2>&1; then
    echo "[!] tailscale not found. Please install it first."
    exit 1
fi

echo "[*] Starting Tailscale daemon..."
sudo tailscaled &

sleep 2

echo "[*] Authenticating to Tailscale..."
sudo tailscale up --ssh

TAIL_IP=$(tailscale ip --4 | head -n1)
echo "[✓] Tailscale IP: $TAIL_IP"
echo "[✓] System ready at: https://$TAIL_IP:5000"