#!/bin/bash

# AscendNet Unified System Setup Script
# Sets up the complete AscendNet system with universal pathing

set -e

echo "🚀 AscendNet Unified System Setup"
echo "================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# AscendNet root directory
ASCENDNET_ROOT="$HOME/AscendNet"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as correct user
if [ "$USER" != "statiksmoke8" ]; then
    print_error "This script should be run as user 'statiksmoke8'"
    exit 1
fi

# Ensure we're in the right directory
cd "$ASCENDNET_ROOT" || {
    print_error "Could not change to AscendNet root directory: $ASCENDNET_ROOT"
    exit 1
}

print_status "Setting up AscendNet unified system..."

# Create virtual environment
print_status "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Initialize the orchestrator
print_status "Initializing AscendNet orchestrator..."
python ascendnet_orchestrator.py

# Create necessary directories if they don't exist
print_status "Ensuring directory structure..."
mkdir -p storage/{cold,memory,expansion}
mkdir -p logs
mkdir -p cache
mkdir -p config
mkdir -p temp
mkdir -p sandbox
mkdir -p tests

# Set up configuration files
print_status "Setting up configuration..."

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cat > .env << EOF
# AscendNet Environment Configuration
ASCENDNET_HOST=0.0.0.0
ASCENDNET_PORT=8000
ASCENDNET_DEBUG=true

# P2P Configuration
P2P_PORT=8001
P2P_BOOTSTRAP_NODES=
P2P_NODE_ID=

# Storage Configuration
IPFS_API=/ip4/127.0.0.1/tcp/5001
CACHE_DIR=$ASCENDNET_ROOT/cache

# AI Core Configuration
MEMORY_DEPTH=2048
RECURSION_LIMIT=512

# Payment Configuration (leave empty for development)
ETHEREUM_RPC=
SOLANA_RPC=
FEE_PERCENTAGE=3.0
EOF
    print_status "Created .env configuration file"
else
    print_warning ".env file already exists"
fi

# Create systemd service file
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/ascendnet.service > /dev/null << EOF
[Unit]
Description=AscendNet Unified System
After=network.target

[Service]
Type=simple
User=statiksmoke8
WorkingDirectory=$ASCENDNET_ROOT
Environment=PATH=$ASCENDNET_ROOT/venv/bin
ExecStart=$ASCENDNET_ROOT/venv/bin/python -m backend.api.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload

print_status "Systemd service created (not started yet)"

# Make scripts executable
chmod +x scripts/*.sh 2>/dev/null || true

# Set up git hooks if this is a git repository
if [ -d ".git" ]; then
    print_status "Setting up git hooks..."
    mkdir -p .git/hooks
    
    # Pre-commit hook for code formatting
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# AscendNet pre-commit hook
echo "Running pre-commit checks..."

# Activate virtual environment
source venv/bin/activate

# Format Python code
black --line-length 100 backend/ || exit 1

# Check types
mypy backend/ --ignore-missing-imports || exit 1

echo "Pre-commit checks passed!"
EOF
    chmod +x .git/hooks/pre-commit
    print_status "Git hooks configured"
fi

# Create launch script
print_status "Creating launch script..."
cat > launch_ascendnet.sh << 'EOF'
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
EOF

chmod +x launch_ascendnet.sh

# Create development launch script
cat > dev_launch.sh << 'EOF'
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
EOF

chmod +x dev_launch.sh

print_status "Launch scripts created"

# Final setup completion
print_status "Running final system initialization..."
python -c "
from backend.ai_core.unified_core import AscendNetAICore
import asyncio

async def init():
    config = {
        'memory_depth': 2048,
        'recursion_limit': 512,
        'gremlin_gpt_enabled': True,
        'god_core_enabled': True,
        'signal_core_enabled': True
    }
    ai_core = AscendNetAICore(config)
    await ai_core.initialize()
    print('AI Core initialized successfully')

asyncio.run(init())
"

echo ""
echo "✅ AscendNet Unified System Setup Complete!"
echo "==========================================="
echo ""
echo "📁 Root Directory: $ASCENDNET_ROOT"
echo "🐍 Virtual Environment: $ASCENDNET_ROOT/venv"
echo "⚙️  Configuration: $ASCENDNET_ROOT/.env"
echo "📝 Logs: $ASCENDNET_ROOT/logs/"
echo ""
echo "🚀 To start AscendNet:"
echo "   ./launch_ascendnet.sh"
echo ""
echo "🛠️  For development:"
echo "   ./dev_launch.sh"
echo ""
echo "🔧 To enable as system service:"
echo "   sudo systemctl enable ascendnet"
echo "   sudo systemctl start ascendnet"
echo ""
echo "📖 API Documentation available at: http://localhost:8000/docs"
echo ""

print_status "Setup completed successfully! 🎉"
