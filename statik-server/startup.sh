#!/bin/bash
# Statik-Server: Sovereign AI Dev Mesh Boot

set -e

echo "🔥 Booting Statik-Server..."
echo "=========================="

# Ensure all directories exist
mkdir -p /root/.statik/{keys,db}
mkdir -p $HOME/AscendNet/storage/memory

# Start headscale mesh VPN in background
echo "🌐 Starting mesh VPN..."
cd /app/internal/mesh
./headscale.sh &

# Wait for headscale to initialize
sleep 3

# Start VS Code with Copilot and memory integration
echo "💻 Starting Statik-Server with Copilot Chat..."
cd /app

# Inject environment variables for Copilot
export GITHUB_TOKEN=$(cat /root/.statik/keys/github-token 2>/dev/null || echo "")
export COPILOT_ENABLED=true
export STATIK_MEMORY_PATH="$HOME/AscendNet/storage/memory"

# Launch statik-server with all integrations
exec ./lib/statik-server \
  --auth none \
  --port 8080 \
  --host 0.0.0.0 \
  --disable-telemetry \
  --disable-update-check \
  --extensions-dir /root/.statik/extensions \
  --user-data-dir /root/.statik/userdata
