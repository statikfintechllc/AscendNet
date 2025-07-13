#!/usr/bin/env bash

# Launch LLaMA backend in new terminal
gnome-terminal -- zsh -c 'cd ~/godcore/llama-cpp-python && conda run -n runmistral python3 run_llama.py; exec zsh'

# Wait for backend to initialize (adjust as needed; can use health-check in future)
sleep 30

# Launch dashboard in second terminal
gnome-terminal -- zsh -c 'cd ~/AscendAI/GremlinGPT/llama_api/dashboard && conda run -n runmistral uvicorn app:app --port 8500; exec zsh'

# Wait briefly, then open browser
sleep 5
xdg-open http://localhost:8500/
