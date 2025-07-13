#!/usr/bin/env zsh

# This script is used to start the GremlinGPT core headless services.
# GremlinGPT Trading Core Headless Startup
source $HOME/miniconda3/etc/profile.d/conda.sh
export GREMLIN_HOME="$HOME/AscendNet/server/AscendAI/GremlinGPT"
export PYTHONPATH="$GREMLIN_HOME:$GREMLIN_HOME/backend:$GREMLIN_HOME/core:$GREMLIN_HOME/agent_core:$GREMLIN_HOME/nlp_engine:$GREMLIN_HOME/memory"
export LOGDIR="$GREMLIN_HOME/data/logs"
export NLTK_DATA="$GREMLIN_HOME/data/nltk_data"

# Launch each subsystem in the background, log output
conda activate gremlin-orchestrator && nohup python core/loop.py >> "$LOGDIR/runtime.log" 2>&1 &
conda activate gremlin-nlp && nohup python nlp_engine/nlp_check.py >> "$LOGDIR/nlp.out" 2>&1 &
conda activate gremlin-memory && nohup python memory/vector_store/embedder.py >> "$LOGDIR/memory.out" 2>&1 &
conda activate gremlin-nlp && nohup python -m agent_core.fsm >> "$LOGDIR/fsm.out" 2>&1 &
conda activate gremlin-scraper && nohup python -m scraper.scraper_loop >> "$LOGDIR/scraper.out" 2>&1 &
conda activate gremlin-orchestrator && nohup python -m self_training.trainer >> "$LOGDIR/trainer.out" 2>&1 &
conda activate gremlin-dashboard && nohup python -m backend.server >> "$LOGDIR/backend.out" 2>&1 &
conda activate gremlin-dashboard && nohup python3 -m http.server 8080 --directory frontend >> "$LOGDIR/frontend.out" 2>&1 &
conda activate gremlin-dashboard && nohup python run/ngrok_launcher.py >> "$LOGDIR/ngrok.out" 2>&1 &

wait
