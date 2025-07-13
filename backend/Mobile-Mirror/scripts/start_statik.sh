#!/usr/bin/env bash
# start_remote_dev.sh - Start Tailscale + code-server with HTTPS + QR code display

set -eu

# Guarantee login+interactive shell for environment
if [[ -z "$LOGIN_SHELL_STARTED" ]]; then
    export LOGIN_SHELL_STARTED=1
    exec "$SHELL" -l -i "$0" "$@"
    exit 1
fi

# Explicitly source Conda setup
CONDA_BASE=$(conda info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh"
conda activate Mob-Dev

# Always activate Mob-Dev conda env, regardless of shell
if command -v conda &>/dev/null; then
    eval "$(conda shell.bash hook)"
    conda activate Mob-Dev
else
    echo "conda not found! Exiting."
    exit 1
fi

LOGFILE="$HOME/statik-server.log"
CERT="$HOME/statik-server.crt"
KEY="$HOME/statik-server.key"
PORT=8888

# Colors for CLI
BOLD='\033[1m'
CYAN='\033[36m'
RESET='\033[0m'

echo -e "${BOLD}${CYAN}[*] Starting Tailscale daemon via systemd...${RESET}"
if command -v pkexec &>/dev/null; then
  pkexec systemctl enable --now tailscaled
else
  echo "[ERROR] pkexec not available, falling back to sudo..."
  sudo systemctl enable --now tailscaled
fi


echo -e "${BOLD}${CYAN}[*] Bringing up Tailscale...${RESET}"
if ! tailscale ip -4 >/dev/null 2>&1; then
    echo -e "${BOLD}${CYAN}[*] Running tailscale up...${RESET}"
if command -v pkexec &>/dev/null; then
  pkexec tailscale up
else
  sudo tailscale up
fi

else
    echo -e "${BOLD}${CYAN}[*] Already connected to Tailnet.${RESET}"
fi

# Pick the first IPv4 Tailscale address
TS_IP=$(tailscale ip -4 | head -n 1)
URL="https://${TS_IP}:${PORT}"

if [[ -z "$TS_IP" ]]; then
    echo -e "${BOLD}ERROR:${RESET} No Tailscale IPv4 found. Is Tailscale up?"
    exit 1
fi

# Generate certs if missing
if [[ ! -f "$CERT" || ! -f "$KEY" ]]; then
    echo -e "${BOLD}${CYAN}[*] Generating self-signed certificate for statik-server HTTPS...${RESET}"
    openssl req -newkey rsa:4096 -nodes -keyout "$KEY" -x509 -days 365 -out "$CERT" -subj "/CN=statik-server"
else
    echo -e "${BOLD}${CYAN}[*] Certificate and key already exist.${RESET}"
fi

echo -e "${BOLD}${CYAN}[*] Starting statik-server with HTTPS on port $PORT...${RESET}"
statik-server --bind-addr 0.0.0.0:$PORT --cert "$CERT" --cert-key "$KEY" >> "$LOGFILE" 2>&1 &

sleep 2

echo -e "${BOLD}${CYAN}[*] Remote dev environment started!${RESET}"

# Generate QR code if qrencode is present
if command -v qrencode >/dev/null 2>&1; then
    echo -e "\n${BOLD}${CYAN}Scan this QR code to access statik-server from your phone:${RESET}"
    echo -e "${BOLD}${CYAN}URL: $URL${RESET}\n"
    qrencode -t ansiutf8 "$URL"
    echo -e "\n${BOLD}${CYAN}Open this in your mobile browser and accept the self-signed cert warning.${RESET}\n"
else
    echo -e "${BOLD}Install qrencode for mobile QR access: sudo apt install qrencode${RESET}"
    echo -e "Or open this URL on your device:\n$URL\n"
fi
echo -e "\n${BOLD}${CYAN}Open this in your mobile browser and accept the self-signed cert warning.${RESET}\n"

echo -e "${BOLD}${CYAN}Press Enter to return to the menu...${RESET}"
read -r

