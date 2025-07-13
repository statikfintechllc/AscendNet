#!/bin/bash
# AscendNet Launch Script

set -e

ASCENDNET_ROOT="$HOME/AscendNet"
cd "$ASCENDNET_ROOT"

echo "🚀 Launching AscendNet Unified System..."

# Activate virtual environment
source venv/bin/activate

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Start the system
python -m backend.api.main
