#!/bin/bash
# AscendNet Development Launch Script

set -e

ASCENDNET_ROOT="$HOME/AscendNet"
cd "$ASCENDNET_ROOT"

echo "🛠️  Launching AscendNet in Development Mode..."

# Activate virtual environment
source venv/bin/activate

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)
export ASCENDNET_DEBUG=true

# Start with auto-reload
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
