#!/bin/zsh

set -e

# Always run from backend directory
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

# --- Function: Start MIS_handler (Mistral) ---
start_mis() {
    echo "\n[*] Starting MIS_handler (Mistral) on port 8000..."
    nohup python "$MIS_FILE" --port 8000 --host 0.0.0.0 > "$MIS_LOG" 2>&1 &
    echo "[*] MIS_handler log: $MIS_LOG"
}

# --- Function: Start GPT_handler (Monday) ---
start_gpt() {
    echo "\n[*] Starting GPT_handler (Monday/ChatGPT) on port 8080..."
    nohup python "$GPT_FILE" --port 8080 --host 0.0.0.0 > "$GPT_LOG" 2>&1 &
    echo "[*] GPT_handler log: $GPT_LOG"
}

# --- Function: Start Router ---
start_router() {
    echo "\n[*] Starting router.py (API router) on port 8088..."
    nohup python "$ROUTER_FILE" --port 8088 --host 0.0.0.0 > "$ROUTER_LOG" 2>&1 &
    echo "[*] Router log: $ROUTER_LOG"
}

# --- Function: Start Frontend (React) ---
start_frontend() {
    echo "\n[*] Starting frontend (React)..."
    cd "$FRONTEND_DIR"
    if [ ! -d node_modules ]; then
        npm install
    fi
    nohup npm start > "$FRONTEND_LOG" 2>&1 &
    echo "[*] Frontend log: $FRONTEND_LOG"
}

# --- Main Execution ---
echo "\n[*] Launching GodCore Full Stack..."

cd "$BACKEND_DIR"
start_mis
sleep 5  # Give MIS_handler a head start

start_gpt
sleep 5  # Give GPT_handler a head start

start_router
sleep 5  # Give router a head start

start_frontend

echo "\n[*] All backend services and frontend are starting up."
echo "    MIS_handler (Mistral):  http://localhost:8000"
echo "    GPT_handler (Monday):   http://localhost:8080"
echo "    Router:                 http://localhost:8088"
echo "    Frontend:               http://localhost:3000"
echo "[*] To stop: pkill -f MIS_handler.py && pkill -f GPT_handler.py && pkill -f router.py && pkill -f react-scripts"
echo "[*] Tail logs: tail -f $MIS_LOG $GPT_LOG $ROUTER_LOG $FRONTEND_LOG"

FRONTEND_URL="http://localhost:3000"
LAN_IP=$(hostname -I | awk '{print $1}')
LAN_URL="http://$LAN_IP:3000"

echo "\n[*] Access frontend via:"
echo "    $FRONTEND_URL"
echo "    $LAN_URL"
echo "\n[*] Scan QR code below (LAN):"

python3 -c "
import qrcode
import sys
qr = qrcode.QRCode(border=2)
qr.add_data('$LAN_URL')
qr.make(fit=True)
qr.print_ascii(invert=True)
" || echo "Install python 'qrcode' module to print QR code."
