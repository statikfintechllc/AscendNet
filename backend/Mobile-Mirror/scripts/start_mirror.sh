#!/usr/bin/env bash
# start_touchcore.sh – Launch TouchCore broadcast services (backend + frontend)

set -e

APPDIR="$HOME/.local/share/applications"
LOGDIR="$APPDIR/system/services"

echo "[*] Starting TouchCore backend..."
nohup python3 "$APPDIR/app.py" > "$LOGDIR/touchcore_backend.log" 2>&1 &

echo "[*] Starting TouchCore frontend..."
nohup npx serve -s "$APPDIR/build" -l 5000 > "$LOGDIR/touchcore_frontend.log" 2>&1 &

TAIL_IP=$(tailscale ip --4 | head -n1)
echo "[✓] TouchCore Broadcast Live at: https://$TAIL_IP:5000"
