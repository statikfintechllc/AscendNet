#!/usr/bin/env bash
# stop_remote_dev.sh - Kill statik-server and stop Tailscale

set -eu

echo "[*] Killing all statik-server processes owned by user $USER..."
pkill -9 -u "$USER" -f "statik-server" || echo "[!] No statik-server process found."

echo "[*] Stopping Tailscale daemon..."
sudo systemctl stop tailscaled || true
sudo pkill -9 tailscaled || true
sudo pkill -9 tailscale || true

echo "[*] Cleaning up stale TUN interface (tailscale0)..."
sudo ip link delete tailscale0 2>/dev/null || true

echo "[✓] Remote dev environment fully stopped."

