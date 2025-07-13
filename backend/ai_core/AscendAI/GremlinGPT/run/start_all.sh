#!/usr/bin/env zsh

# --- AscendAI GremlinGPT Start Script ---
# This script launches all GremlinGPT subsystems in separate terminal windows.  

# It ensures that the environment is set up correctly and that all necessary services are running.
setopt NO_GLOB_SUBST

# --- Environment Setup ---
# Ensure the script runs in the user's home directory
# and sets up the necessary environment variables.
# This allows for dynamic project paths and log directories.
# It also ensures that the NLTK data directory is created and configured correctly.
# This script should be run from the GremlinGPT project root directory.
# If run from a different directory, it will still work as long as the environment variables are
GREMLIN_HOME="$HOME"
PYTHONPATH="$GREMLIN_HOME"
LOGDIR="$GREMLIN_HOME/data/logs"

# --- Dynamic Project Path ---
export GREMLIN_HOME="$HOME"
export PYTHONPATH="$GREMLIN_HOME"

# --- Log Directory ---
export LOGDIR="$GREMLIN_HOME/data/logs"


# --- NLTK Bootstrap: Always under repo, not home! ---
python3 - <<'EOF'
import os, nltk
nltk_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data/nltk_data"))
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)
for pkg, path in [
    ("punkt", "tokenizers/punkt"),
    ("averaged_perceptron_tagger", "taggers/averaged_perceptron_tagger"),
    ("wordnet", "corpora/wordnet"),
    ("stopwords", "corpora/stopwords"),
]:
    try: nltk.data.find(path)
    except LookupError: nltk.download(pkg, download_dir=nltk_data_dir)
EOF

# --- Terminal detection ---
TERM_EMU=$(command -v gnome-terminal || command -v xterm)

function launch_terminal() {
  local title="$1"
  local env="$2"
  local cmd="$3"
  local logfile="$4"

  local preamble="
    source \$HOME/miniconda3/etc/profile.d/conda.sh
    conda activate $env || { echo '[${title}] Failed to activate env: $env'; exec zsh; }
    export NLTK_DATA=\"\$GREMLIN_HOME/data/nltk_data\"
    echo '[${title}] ENV:' \$CONDA_DEFAULT_ENV
    echo '[${title}] CWD:' \$PWD
    echo '[${title}] Running: $cmd'
    $cmd | tee $logfile
    EXIT_CODE=\${PIPESTATUS[0]}
    echo '[${title}] Process exited with code' \$EXIT_CODE
    exec zsh
  "

  if command -v gnome-terminal > /dev/null; then
    gnome-terminal --title="$title" -- zsh --login -c "$preamble"
  elif command -v xterm > /dev/null; then
    xterm -T "$title" -e "zsh --login -c '$preamble'"
  else
    echo "No supported terminal emulator found (gnome-terminal or xterm)."
    exit 1
  fi
}

echo "[BOOT] Injecting GremlinGPT watermark to system trace."
echo "Boot ID: $(uuidgen) | Source: GremlinGPT | Time: $(date -u)" | tee -a "$LOGDIR/gremlin_boot_trace.log"

echo "[START] Launching GremlinGPT subsystems in separate terminals..."

launch_terminal "Core Loop" gremlin-orchestrator "python core/loop.py" "$LOGDIR/runtime.log"
launch_terminal "NLP Service" gremlin-nlp "python nlp_engine/nlp_check.py" "$LOGDIR/nlp.out"
launch_terminal "Memory Service" gremlin-memory "python memory/vector_store/embedder.py" "$LOGDIR/memory.out"
launch_terminal "FSM Agent" gremlin-nlp "python -m agent_core.fsm" "$LOGDIR/fsm.out"
launch_terminal "Scraper" gremlin-scraper "python -m scraper.scraper_loop" "$LOGDIR/scraper.out"
launch_terminal "Self-Trainer" gremlin-orchestrator "python -m self_training.trainer" "$LOGDIR/trainer.out"
launch_terminal "Backend Server" gremlin-dashboard "python -m backend.server" "$LOGDIR/backend.out"
launch_terminal "Frontend" gremlin-dashboard "python3 -m http.server 8080 --directory frontend" "$LOGDIR/frontend.out"
launch_terminal "Ngrok Tunnel" gremlin-dashboard "python run/ngrok_launcher.py" "$LOGDIR/ngrok.out"

# --- Playwright install check for scraper (headless) ---
conda activate gremlin-scraper
python -c "import playwright; print('Playwright OK')" 2>/dev/null || playwright install
conda deactivate

# --- Ngrok CLI check ---
if ! command -v ngrok &> /dev/null; then
    echo "[NOTICE] ngrok not found. Visit https://ngrok.com/download or configure pyngrok in config.toml"
else
    echo "[INFO] ngrok installed: $(which ngrok)"
fi

echo "Backend:     http://localhost:8000"
echo "Frontend:    http://localhost:8080"
echo "Logs:        $GREMLIN_HOME/data/logs/"

# --- Dashboard Launch Info ---
if [ -d "$GREMLIN_HOME/frontend" ] && [ -f "$GREMLIN_HOME/frontend/package.json" ]; then
  echo "Detected frontend dashboard source. Run manually if you want React/JS hot reload:"
  echo "  cd frontend && npm install && npm run dev"
fi
