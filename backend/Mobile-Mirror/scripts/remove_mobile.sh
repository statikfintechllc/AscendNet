#!/usr/bin/env bash
# env/remove_mobile.sh - Full uninstall for Mobile Developer (scripts, .desktop, icons, conda, log)

set -eu

ENV_NAME="Mob-Dev"
APPDIR="$HOME/.local/share/applications"
ICNDIR="$HOME/.local/share/icons"
LOGFILE="$APPDIR/statik-server.log"
DESKTOP_FILE="$APPDIR/MobileDeveloper.desktop"

echo "[*] Removing Mobile Developer files..."

# Remove installed files
rm -f \
  "$APPDIR/mobile_cli.sh" \
  "$APPDIR/start_statik.sh" \
  "$APPDIR/stop_code.sh" \
  "$LOGFILE" \
  "$DESKTOP_FILE" || true

# Remove icon
rm -f "$ICNDIR/MobileDeveloper.png" || true

# Remove conda environment
if command -v conda &>/dev/null; then
    if conda info --envs | awk '{print $1}' | grep -qx "$ENV_NAME"; then
        echo "[*] Removing conda env '$ENV_NAME'..."
        conda remove -y -n "$ENV_NAME" --all
    else
        echo "[*] Conda env '$ENV_NAME' does not exist."
    fi
else
    echo "[!] Conda not found — skipping environment removal."
fi

# Refresh application database
update-desktop-database ~/.local/share/applications || true
gtk-update-icon-cache "$ICNDIR" || true

echo "[✔] Mobile Developer fully removed."
