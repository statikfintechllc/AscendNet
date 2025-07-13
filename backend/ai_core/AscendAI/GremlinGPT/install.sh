#!/usr/bin/env zsh

# === Move all files and subdirectories (including hidden ones) from GremlinGPT to $HOME, overwriting existing ===
REPO="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
SRC="$REPO/GremlinGPT"
DEST="$HOME"

setopt extended_glob
for item in "$SRC"/*(N) "$SRC"/.*(N); do
  [[ "$(basename "$item")" == "." || "$(basename "$item")" == ".." ]] && continue
  # Do not move the icon directory to avoid overwriting/corrupting the icon, as it is used by the application
  if [[ "$(basename "$item")" == "Icon_Logo" ]]; then
    continue
  fi
  # Do not move the currently running install.sh, as it would cause issues
  if [[ "$item" == "$0" ]]; then
    continue
  fi
  target="$DEST/$(basename "$item")"
  if [ -e "$target" ]; then
    rm -rf "$target"
  fi
  mv -f "$item" "$DEST/"
done
unsetopt extended_glob

# Update the repository, ensuring we are in the correct directory
banner "Updating GremlinGPT repository..."

# Ensure the log directory exists, create it if not
git stash || echo "${YELLOW}[WARNING] git stash failed, continuing...${NC}"
git pull --rebase || { echo "${RED}[ERROR] git pull failed!${NC}"; exit 1; }
cd $HOME || { echo "[ERROR] Failed to change directory to $HOME"; exit 1; }

# === Set up logging and variables AFTER move ===
LOGFILE="data/logs/install.log"
: > "$LOGFILE"         # Overwrite log file
exec > >(tee -a "$LOGFILE") 2>&1

setopt NO_GLOB_SUBST
set +u
set -o pipefail

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# --- Banner helper, to print messages in a consistent format ---
# Usage: banner "Your message here"
# This function prints a message in cyan color with a prefix [INSTALL]
# It can be used to highlight important steps in the installation process.
function banner() {
  echo -e "\n\033[1;36m[INSTALL] $1\033[0m\n"
}

echo "${GREEN}[INSTALL] Initializing GremlinGPT installation...${NC}"
banner "Initializing GremlinGPT installation..."

# Proper definition of variables, ensuring they are set before use
APPDIR="$HOME/.local/share/applications"
ICNDIR="$HOME/.local/share/icons"
APPLOC="$HOME"
WAKE_SCRIPT="/usr/local/bin/set-wake-timer.sh"
LOGIN_SCRIPT="$APPLOC/utils/tws_stt_autologin.sh"
CONFIG_PATH="$APPLOC/config/config.toml"
SYSTEMD_UNIT_PATH="/etc/systemd/system/gremlin.service"
START_SCRIPT="$APPLOC/start_all.sh"
ICON_SRC="$HOME/frontend/Icon_Logo/App_Icon_&_Loading_&_Inference_Image.png"
ICON_DEST="$ICNDIR/AscendAI-v1.0.3.png"
SCRIPT="$APPLOC/utils/dash_cli.sh"
ICON=$ICON_DEST
APP=$SCRIPT

# Ensure the application has the correct permissions, if the script exists
if [ -f "$SCRIPT" ]; then
  chmod +x "$SCRIPT"
else
  echo "${YELLOW}[WARNING] $SCRIPT not found. Using python fallback.${NC}"
  SCRIPT="python3 $APPLOC/utils/dash_cli.py"
fi >> "$LOGFILE" 2>&1

if [ -f "$ICON_SRC" ]; then
  if file "$ICON_SRC" | grep -q "PNG image data"; then
    cp "$ICON_SRC" "$ICON_DEST"
  else
    echo "${YELLOW}[WARNING] $ICON_SRC is not a valid PNG. Skipping icon copy.${NC}"
  fi
else
  echo "${YELLOW}[WARNING] Icon file not found at $ICON_SRC. Skipping icon copy.${NC}"
fi

# Ensure the icon directory exists, if not create it
TWS_USER=$(grep -oP '(?<=tws_username\\s?=\\s?")[^"]*' "$CONFIG_PATH")
TWS_PASS=$(grep -oP '(?<=tws_password\\s?=\\s?")[^"]*' "$CONFIG_PATH")
STT_USER=$(grep -oP '(?<=stt_username\\s?=\\s?")[^"]*' "$CONFIG_PATH")
STT_PASS=$(grep -oP '(?<=stt_password\\s?=\\s?")[^"]*' "$CONFIG_PATH")

# 1. Directory structure, if not already created
banner "Creating directory structure..."

DIRS=(
  "data/logs"
  "run/checkpoints"
  "data/prompts"
  "data/raw_scrapes"
  "data/embeddings"
  "data/nlp_training_sets"
  "data/logs"
  "memory/vector_store/faiss"
  "memory/vector_store/chroma"
  "memory/local_index/documents"
  "memory/local_index/scripts"
  "scraper/persistence/cookies"
  "scraper/profiles/chromium_profile"
  "frontend/components"
  "tests"
  "docs"
  "data/nltk_data"
)
for dir in "${DIRS[@]}"; do
  [ ! -d "$dir" ] && mkdir -p "$dir" && echo "Created: $dir" || echo "Exists:  $dir"
done

banner "Ensuring conda is initialized..."

# 2. Conda init, if not already initialized
echo "[*] Ensuring conda is initialized..."
if ! command -v conda &> /dev/null; then
    if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
        source "$HOME/miniconda3/etc/profile.d/conda.sh"
    fi
fi
eval "$(conda shell.zsh hook 2>/dev/null)" || eval "$(conda shell.bash hook 2>/dev/null)"

# 3. Build all conda environments, if not already built
banner "Building all conda environments via ./conda_envs/create_envs.sh..."

# Add this block before running conda commands as root, to ensure conda is sourced correctly
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
fi

if [ -f "./conda_envs/create_envs.sh" ]; then
    chmod +x ./conda_envs/create_envs.sh
    ./conda_envs/create_envs.sh || { echo "${RED}[ERROR] Failed creating envs${NC}"; exit 1; }
else
    echo "${RED}[ERROR] ./conda_envs/create_envs.sh not found!${NC}"
fi

# Function to check CUDA availability in the current environment
# This function will print the CUDA availability status and device information.
# It is useful for verifying that PyTorch can utilize GPU resources if available.
# Usage: check_cuda
# This function will print the CUDA availability status and device information.
# It is useful for verifying that PyTorch can utilize GPU resources if available.
# Usage: check_cuda
# This function will print the CUDA availability status and device information.
function check_cuda {
  echo "[*] Checking CUDA in current environment:"
  python -c "
import torch
print('[CUDA] torch.cuda.is_available:', torch.cuda.is_available())
print('[CUDA] torch.cuda.device_count:', torch.cuda.device_count())
print('[CUDA] torch.cuda.current_device:', torch.cuda.current_device() if torch.cuda.is_available() else None)
print('[CUDA] torch.cuda.get_device_name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)
" || echo "${RED}[CUDA] PyTorch not installed or failed.${NC}"
}

# Function to install pip packages and handle failures
# This function will attempt to upgrade pip and install the specified packages.
# If any installation fails, it will print an error message and exit with a non-zero status.
# Usage: pip_install_or_fail package1 package2 ...
# This function will attempt to upgrade pip and install the specified packages.
# If any installation fails, it will print an error message and exit with a non-zero status
function pip_install_or_fail {
  pip install --upgrade pip || { echo '${RED}[FAIL] pip upgrade${NC}'; exit 1; }
  for pkg in "$@"; do
    pip install "$pkg" || { echo "${RED}[FAIL] pip install $pkg${NC}"; exit 1; }
  done
}

# Function to download NLTK data packages
# This function will download the specified NLTK data packages to the user's home directory.
# If the download fails, it will print an error message and exit with a non-zero status
# Usage: download_nltk
function download_nltk {
  python3 -m nltk.downloader --dir=$HOME/data/nltk_data punkt averaged_perceptron_tagger wordnet stopwords || \
  { echo "${RED}[FAIL] NLTK data download${NC}"; exit 1; }
}

# 4. gremlin-nlp env setup, if not already set up
banner "Activating gremlin-nlp and installing deps..."
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
fi

conda activate gremlin-nlp >> "$LOGFILE" 2>&1
pip_install_or_fail spacy torch torchvision torchaudio sentence-transformers transformers bs4 nltk pytesseract playwright pyautogui flask flask-socketio watchdog eventlet >> "$LOGFILE" 2>&1
python -m spacy download en_core_web_sm >> "$LOGFILE" 2>&1 || { echo "${RED}[FAIL] spaCy model${NC}"; exit 1; }
playwright install >> "$LOGFILE" 2>&1 || { echo "${RED}[FAIL] playwright${NC}"; exit 1; }
pip install nltk >> "$LOGFILE" 2>&1
export NLTK_DATA=$HOME/data/nltk_data
python -m nltk.downloader -d "$NLTK_DATA" punkt >> "$LOGFILE" 2>&1
download_nltk >> "$LOGFILE" 2>&1
check_cuda >> "$LOGFILE" 2>&1
sudo apt-get install python3-tk python3-dev
python -c "
from transformers import AutoTokenizer, AutoModel
import torch
print('[GPU-TEST] Loading BERT on', 'cuda' if torch.cuda.is_available() else 'cpu')
AutoTokenizer.from_pretrained('bert-base-uncased')
AutoModel.from_pretrained('bert-base-uncased').to('cuda' if torch.cuda.is_available() else 'cpu')
" >> "$LOGFILE" 2>&1
python -c "
from sentence_transformers import SentenceTransformer
import torch
print('[GPU-TEST] Loading MiniLM on', 'cuda' if torch.cuda.is_available() else 'cpu')
SentenceTransformer('all-MiniLM-L6-v2', device='cuda' if torch.cuda.is_available() else 'cpu')
" >> "$LOGFILE" 2>&1
conda deactivate >> "$LOGFILE" 2>&1

# 5. gremlin-scraper env setup, if not already set up
banner "Activating gremlin-scraper..."
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
fi
conda activate gremlin-scraper >> "$LOGFILE" 2>&1
pip_install_or_fail torch torchvision watchdog torchaudio sentence-transformers transformers playwright pyautogui flask flask-socketio eventlet >> "$LOGFILE" 2>&1
python -m spacy download en_core_web_sm >> "$LOGFILE" 2>&1
playwright install >> "$LOGFILE" 2>&1
check_cuda >> "$LOGFILE" 2>&1
sudo apt-get install python3-tk python3-dev
conda deactivate >> "$LOGFILE" 2>&1

# 5. gremlin-scraper env setup, if not already set up. This is a duplicate of the previous step, but for gremlin-memory
# This is a duplicate of the previous step, but for gremlin-memory
# This is necessary to ensure that the gremlin-memory environment is set up correctly
# and to avoid conflicts with the gremlin-scraper environment.
banner "Activating gremlin-memory..."
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
fi
conda activate gremlin-memory >> "$LOGFILE" 2>&1
pip_install_or_fail eventlet flask chromadb watchdog faiss-cpu >> "$LOGFILE" 2>&1
conda deactivate >> "$LOGFILE" 2>&1

# 6. gremlin-dashboard env setup, if not already set up
banner "Activating gremlin-dashboard..."
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
fi
conda activate gremlin-dashboard >> "$LOGFILE" 2>&1
pip_install_or_fail flask eventlet torch watchdog torchvision torchaudio sentence-transformers transformers pyautogui >> "$LOGFILE" 2>&1
sudo apt-get install python3-tk python3-dev tesseract-ocr
check_cuda >> "$LOGFILE" 2>&1
conda deactivate >> "$LOGFILE" 2>&1

# 7. gremlin-orchestrator env setup, if not already set up
banner "Activating gremlin-orchestrator..."
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
fi
conda activate gremlin-orchestrator >> "$LOGFILE" 2>&1
pip_install_or_fail torch torchvision torchaudio watchdog bs4 nltk langdetect pytesseract sentence-transformers transformers playwright pyautogui flask flask-socketio eventlet >> "$LOGFILE" 2>&1
sudo apt-get install python3-tk python3-dev tesseract-ocr
python -m spacy download en_core_web_sm >> "$LOGFILE" 2>&1
playwright install >> "$LOGFILE" 2>&1
pip install nltk >> "$LOGFILE" 2>&1
export NLTK_DATA=$HOME/data/nltk_data
python -m nltk.downloader -d "$NLTK_DATA" punkt >> "$LOGFILE" 2>&1
download_nltk >> "$LOGFILE" 2>&1
check_cuda >> "$LOGFILE" 2>&1
python -c "
from transformers import AutoTokenizer, AutoModel
import torch
print('[GPU-TEST] Loading BERT on', 'cuda' if torch.cuda.is_available() else 'cpu')
AutoTokenizer.from_pretrained('bert-base-uncased')
AutoModel.from_pretrained('bert-base-uncased').to('cuda' if torch.cuda.is_available() else 'cpu')
" >> "$LOGFILE" 2>&1
python -c "
from sentence_transformers import SentenceTransformer
import torch
print('[GPU-TEST] Loading MiniLM on', 'cuda' if torch.cuda.is_available() else 'cpu')
SentenceTransformer('all-MiniLM-L6-v2', device='cuda' if torch.cuda.is_available() else 'cpu')
" >> "$LOGFILE" 2>&1
conda deactivate >> "$LOGFILE" 2>&1

# 8. ngrok CLI check, if not already installed, attempt automatic installation, if not found
banner "Checking for ngrok CLI..."

if ! command -v ngrok &> /dev/null; then
    echo "${YELLOW}[NOTICE] ngrok not found. Attempting automatic installation...${NC}"
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        wget -O /tmp/ngrok.zip https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.zip && \
        unzip -o /tmp/ngrok.zip -d "$HOME/.local/bin" && \
        chmod +x "$HOME/.local/bin/ngrok" && \
        rm /tmp/ngrok.zip && \
        echo "${GREEN}[INFO] ngrok installed to $HOME/.local/bin/ngrok${NC}" || \
        echo "${RED}[ERROR] Failed to install ngrok automatically.${NC}"
        export PATH="$HOME/.local/bin:$PATH"
        # Instruct user to persist PATH for future shells, if not already done
        SHELL_PROFILE=""
        if [ -n "$ZSH_VERSION" ]; then
          SHELL_PROFILE="$HOME/.zshrc"
        elif [ -n "$BASH_VERSION" ]; then
          SHELL_PROFILE="$HOME/.bashrc"
        else
          SHELL_PROFILE="$HOME/.profile"
        fi
        if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_PROFILE"; then
          echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_PROFILE"
          echo "${YELLOW}[NOTICE] Added ngrok path to $SHELL_PROFILE. Restart your terminal or run: source $SHELL_PROFILE${NC}"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ngrok || echo "${RED}[ERROR] Failed to install ngrok via Homebrew.${NC}"
    else
        echo "${YELLOW}[NOTICE] Please install ngrok manually for your OS: https://ngrok.com/download${NC}"
    fi
else
    echo "[INFO] ngrok installed: $(which ngrok)"
fi >> "$LOGFILE" 2>&1

# === System package dependencies ===
echo "[*] Installing required system packages (including python3-tk for GUI support and tesseract-ocr for OCR)..."
sudo apt install -y xdotool util-linux python3-tk python3-dev tesseract-ocr

# set -x  # Enable command tracing for debugging. Uncomment if needed.

# 9. Setup systemd service, if not already set up, to manage GremlinGPT processes, if not already set up
# This service will ensure that GremlinGPT starts on boot and can be managed via systemctl
banner "Setup systemd service"

# Ensure the start script exists, if not this creates it
echo "APPLOC=$APPLOC"
echo "START_SCRIPT=$START_SCRIPT"
echo "USER=$USER"


sudo tee "$SYSTEMD_UNIT_PATH" > /dev/null <<EOF
[Unit]
Description=GremlinGPT Autonomous Agent
After=network.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=$APPLOC
ExecStart=/bin/bash -c 'source $HOME/miniconda3/etc/profile.d/conda.sh && conda activate gremlin-orchestrator && python3 core/loop.py'
Restart=always
RestartSec=10
User=$USER
Group=$USER
Environment="PYTHONPATH=$APPLOC"
Environment="PATH=$HOME/miniconda3/envs/gremlin-orchestrator/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Environment="CONDA_DEFAULT_ENV=gremlin-orchestrator"
Environment="CONDA_PREFIX=$HOME/miniconda3/envs/gremlin-orchestrator"
Environment="HOME=$HOME"
StandardOutput=journal
StandardError=journal
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable gremlin.service
sudo systemctl restart gremlin.service

echo "[✓] Systemd service registered and running." >> "$LOGFILE" 2>&1

# 10. Setup RTC wake & login filler from config, if available, to automate wake timer and GUI login
# This script will set the RTC wake timer and automatically log in to TWS and STT
# It will run on system boot via cron and ensure the system wakes up at the specified time
# and logs in to the GUI automatically, if credentials are available in config.toml
banner "Setting RTC wake + GUI login automation..."

sudo tee "$WAKE_SCRIPT" > /dev/null <<EOF
#!/bin/zsh
rtcwake -m no -t $(date -d 'tomorrow 03:30' +%s)
EOF
sudo chmod +x "$WAKE_SCRIPT"
(crontab -l 2>/dev/null | grep -v "$WAKE_SCRIPT"; echo "@reboot $WAKE_SCRIPT") | crontab -

# 11. Pulling login creds from config.toml, if available, to automate TWS and STT login
# This script will automatically log in to TWS and STT using xdotool
# It will run on system boot via cron and ensure the user is logged in to both applications
banner "Setting up TWS and STT auto-login script..."
tee "$LOGIN_SCRIPT" > /dev/null <<EOF
#!/bin/zsh
sleep 20

# TWS Auto-login
xdotool search --name "Trader Workstation" windowactivate --sync \
  key Tab key Tab type '$TWS_USER' key Tab \
  type '$TWS_PASS' key Return

# STT Auto-login
xdotool search --name "StocksToTrade" windowactivate --sync \
  key Tab type '$STT_USER' key Tab \
  type '$STT_PASS' key Return
EOF

# Ensure the login script is executable and set up to run on boot
chmod +x "$LOGIN_SCRIPT"

(crontab -l 2>/dev/null | grep -v "$LOGIN_SCRIPT"; echo "@reboot $LOGIN_SCRIPT") | crontab -

echo "${GREEN}[✓] Wake timer, autologin, and systemd service bootstrapped.${NC}"

# 12. Finalize installation, create desktop entry, and icon, if not already created
# This will create a .desktop file for GremlinGPT to allow launching from the desktop environment
# It will also ensure the icon is set up correctly for the application
banner "Finalizing installation and creating desktop entry..."

# Create .desktop file with required fields and validate, if missing, create a fallback, if not already created
cat > "$APPDIR/AscendAI-v1.0.3.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=AscendAI-v1.0.3
Comment=SFTi
Exec=$APP
Icon=$ICON
Terminal=true
Categories=Utility;Development;Application;
StartupNotify=true
EOF

chmod +x "$APP"
chmod 644 "$ICON"

update-desktop-database "$APPDIR" >> "$LOGFILE" 2>&1 || echo "${YELLOW}[WARNING] update-desktop-database failed. Continuing...${NC}"

set -u  # Reset to default shell behavior, ensuring undefined variables cause an error

# 13. Final message, indicating successful installation
banner "GremlinGPT installation completed successfully!"
echo "${GREEN}[✓] GremlinGPT installation completed successfully!${NC}"
banner "You can now run GremlinGPT using the command: $APP"
echo "${GREEN}[INSTALL] GremlinGPT installation completed successfully.${NC}"
banner "Installation log saved to $LOGFILE('~/data/logs/install.log')"
