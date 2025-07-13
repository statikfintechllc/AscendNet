#!/bin/zsh

set -e

cd "$(dirname "$0")"

# --- Config ---
ENV_NAME="runmistral"
BACKEND_DIR="$(pwd)"
FRONTEND_DIR="$BACKEND_DIR/../frontend"
FRONTEND_LOG="$BACKEND_DIR/logs/frontend.log"
ROUTER_LOG="$BACKEND_DIR/logs/router.log"
MIS_LOG="$BACKEND_DIR/logs/mis_handler.log"
GPT_LOG="$BACKEND_DIR/logs/gpt_handler.log"
MIS_FILE="$BACKEND_DIR/MIS_handler.py"
GPT_FILE="$BACKEND_DIR/GPT_handler.py"
ROUTER_FILE="$BACKEND_DIR/router.py"

FRONTEND_PORT=3000
MIS_PORT=8000
GPT_PORT=8080
ROUTER_PORT=8088

echo "BACKEND_DIR: $BACKEND_DIR"
echo "FRONTEND_DIR: $FRONTEND_DIR"
echo "MIS_LOG: $MIS_LOG"
echo "GPT_LOG: $GPT_LOG"
echo "ROUTER_LOG: $ROUTER_LOG"
echo "FRONTEND_LOG: $FRONTEND_LOG"

export LLAMA_CPP_FORCE_CUDA=1
export GGML_CUDA_FORCE_MMQ=1
export GGML_CUDA_PEER_ACCESS=0

source ~/miniconda3/etc/profile.d/conda.sh || { echo '[FATAL] Could not source conda. Aborting.'; exit 1; }
conda activate $ENV_NAME || { echo '[FATAL] Could not activate env. Aborting.'; exit 1; }

# --- Start MIS_handler ---
echo "\n[*] Starting MIS_handler (Mistral) on port $MIS_PORT..."
nohup python "$MIS_FILE" --port $MIS_PORT --host 0.0.0.0 > "$MIS_LOG" 2>&1 &
echo "[*] MIS_handler log: $MIS_LOG"

# --- Start GPT_handler ---
echo "\n[*] Starting GPT_handler (Monday/ChatGPT) on port $GPT_PORT..."
nohup python "$GPT_FILE" --port $GPT_PORT --host 0.0.0.0 > "$GPT_LOG" 2>&1 &
echo "[*] GPT_handler log: $GPT_LOG"

# --- Start Router ---
echo "\n[*] Starting router.py (API router) on port $ROUTER_PORT..."
nohup python "$ROUTER_FILE" --port $ROUTER_PORT --host 0.0.0.0 > "$ROUTER_LOG" 2>&1 &
echo "[*] Router log: $ROUTER_LOG"

sleep 5  # Give backends time to start

# --- Start Frontend (React) ---
echo "\n[*] Starting frontend (React)..."
cd "$FRONTEND_DIR"
if [ ! -d node_modules ]; then
    npm install
fi
nohup npm start > "$FRONTEND_LOG" 2>&1 &
echo "[*] Frontend log: $FRONTEND_LOG"

# --- Print ALL Accessible URLs ---
LOCAL_IP=$(ip addr | awk '/inet / && $2 !~ /^127/ {split($2,a,"/"); print a[1]; exit}')
echo "\n[*] All backend services and frontend are starting up."
echo "    MIS_handler (localhost):   http://localhost:$MIS_PORT"
echo "    GPT_handler (localhost):   http://localhost:$GPT_PORT"
echo "    Router (localhost):        http://localhost:$ROUTER_PORT"
echo "    Frontend (localhost):      http://localhost:$FRONTEND_PORT"
echo "    MIS_handler (LAN):         http://$LOCAL_IP:$MIS_PORT"
echo "    GPT_handler (LAN):         http://$LOCAL_IP:$GPT_PORT"
echo "    Router (LAN):              http://$LOCAL_IP:$ROUTER_PORT"
echo "    Frontend (LAN):            http://$LOCAL_IP:$FRONTEND_PORT"
echo "[*] To stop: pkill -f MIS_handler.py && pkill -f GPT_handler.py && pkill -f router.py && pkill -f react-scripts"
echo "[*] Tail logs: tail -f $MIS_LOG $GPT_LOG $ROUTER_LOG $FRONTEND_LOG"

# --- Wait for frontend to be ready ---
echo "[*] Waiting for frontend to be ready on port $FRONTEND_PORT..."
success=0
for i in {1..30}; do
  if lsof -i:$FRONTEND_PORT | grep LISTEN; then
    echo "[+] Frontend running on port $FRONTEND_PORT"
    success=1
    break
  fi
  sleep 1
done

if [ $success -eq 0 ]; then
  echo "[FATAL] Frontend did not start on port $FRONTEND_PORT after 30 seconds!"
  echo "==== Last 40 lines of frontend log ===="
  tail -40 "$FRONTEND_LOG"
  exit 1
fi

# --- Start ngrok in the background ---
echo "[*] Starting ngrok tunnel to frontend (http://$LOCAL_IP:$FRONTEND_PORT)..."

pkill -f "ngrok http $FRONTEND_PORT" || true

NGROK_LOG="/tmp/ngrok.log"
ngrok http $FRONTEND_PORT --log=stdout > "$NGROK_LOG" 2>&1 &

# Wait for ngrok to start and print the public URL
NGROK_URL=""
for i in {1..20}; do
  NGROK_URL=$(grep -oE "https://[a-zA-Z0-9.-]+\.ngrok-free\.app" "$NGROK_LOG" | head -n1)
  if [[ -n "$NGROK_URL" ]]; then
    break
  fi
  sleep 1
done

if [[ -z "$NGROK_URL" ]]; then
    echo "[FATAL] ngrok did not return a valid URL. See log below:"
    tail -20 "$NGROK_LOG"
    exit 1
fi
echo "[+] ngrok tunnel is live: $NGROK_URL"

# --- QR Code for ngrok (global access) ---
if command -v qrencode > /dev/null; then
    echo "\n[+] Scan this QR code with your phone to open the UI (ANYWHERE):"
    echo "$NGROK_URL" | qrencode -t ansiutf8
    echo "\n[+] Or open this URL on your phone: $NGROK_URL"
else
    echo "[!] qrencode not installed. Install with: sudo apt install qrencode"
fi

# --- QR Code for local LAN access (home/office only) ---
LAN_URL="http://$LOCAL_IP:$FRONTEND_PORT"
if command -v qrencode > /dev/null; then
    echo "\n[+] Scan this QR code with your phone to open the UI (LAN only):"
    echo "$LAN_URL" | qrencode -t ansiutf8
    echo "\n[+] Or open this URL on your phone: $LAN_URL"
fi
echo "\n[+] Open this URL on your phone to access the UI:"
echo "$NGROK_URL"
echo "\n[*] Done."

# Optionally: Do not clean up $NGROK_LOG in case you want to review ngrok output
