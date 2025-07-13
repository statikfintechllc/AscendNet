#!/bin/zsh

echo "[STOP] Terminating all GremlinGPT processes..."

# Stop Core Loop and Orchestrator
pkill -f "core/loop.py"

# Stop NLP Service
pkill -f "nlp_engine/nlp_check.py"

# Stop Memory Service
pkill -f "memory/vector_store/embedder.py"

# Stop Backend Server (FastAPI or Flask)
pkill -f "backend/server"

# Stop FSM Agent
pkill -f "agent_core/fsm"

# Stop Scraper
pkill -f "scraper/scraper_loop"

# Stop Self-Trainer
pkill -f "self_training/trainer"

# Stop Frontend (http.server)
pkill -f "http.server"

# Stop Ngrok Tunnel
pkill -f "ngrok_launcher.py"

echo "[STOP] All GremlinGPT subsystems stopped."

