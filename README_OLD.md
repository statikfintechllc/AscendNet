# AscendNet Unified System

<div align="center">
  <img src="https://img.shields.io/badge/AscendNet%20Unified-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="AscendNet Unified"/>
  <img src="https://img.shields.io/badge/Status-Alpha-orange?style=for-the-badge" alt="Status"/>
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-Latest-green?style=for-the-badge&logo=fastapi" alt="FastAPI"/>
</div>

## 🌟 Overview

AscendNet is a unified P2P AI marketplace and autonomous development system that combines:

- **AscendAI** - Core AI infrastructure and systems
- **GremlinGPT** - Recursive, Self-Referential Autonomous Cognitive System (R-SRACS)
- **GodCore** - Multi-model AI routing and quantum-level processing
- **SignalCore** - Recursive AI thought processing with safety limits
- **Mobile-Mirror** - Secure mobile development environment
- **Statik-Server** - Self-hosted VS Code with Copilot Chat + mesh VPN
- **P2P Network** - Decentralized prompt and compute marketplace
- **Universal Pathing** - Consistent file system organization

## 🏗️ Unified Architecture

```
$HOME/AscendNet/
├── statik-server/            # Sovereign AI Development Environment
│   ├── VS Code 1.102.0+     # Latest VS Code with real Copilot Chat
│   ├── Embedded mesh VPN    # Self-hosted Tailscale (headscale)
│   ├── Persistent auth       # No GitHub login loops
│   └── AI memory integration # GremlinGPT/GodCore dashboards
├── backend/                  # Unified Backend System
│   ├── api/                   # FastAPI REST endpoints
│   │   ├── main.py           # Main API entry point
│   │   ├── dependencies.py   # Auth, rate limiting
│   │   └── routes/           # API route modules
│   ├── p2p/                  # P2P networking layer
│   │   └── node.py          # P2P node implementation
│   ├── ai_core/              # Unified AI processing
│   │   └── unified_core.py   # GremlinGPT + GodCore + SignalCore
│   ├── compute/              # Distributed computing
│   ├── payments/             # Crypto payment handling
│   ├── storage/              # IPFS and quantum storage
│   ├── auth/                 # Authentication system
│   └── utils/                # Shared utilities
├── frontend/                 # Web and desktop frontends
├── smart-contracts/          # Blockchain contracts
├── storage/                  # Unified storage layers
│   ├── cold/                # Cold storage (was coldstorage/)
│   ├── memory/              # Memory forge (was memforge/)
│   └── expansion/           # Expansion pool
├── docs/                    # System documentation
├── scripts/                 # Setup and utility scripts
├── config/                  # Configuration files
├── logs/                    # System logs
└── ascendnet_orchestrator.py # Main system orchestrator
```

## 🚀 Quick Start

### Prerequisites

**System Requirements:**
- Linux (Ubuntu 20.04+ recommended)
- Docker and Docker Compose
- Node.js 20+ and Yarn
- Python 3.11+
- 4GB+ RAM, 20GB+ disk space

**Required Accounts:**
- GitHub account with Copilot subscription
- GitHub Personal Access Token with `repo` and `copilot` scopes

### 1. Installation

**Clone the Repository:**
```bash
git clone https://github.com/statikfintechllc/AscendNet.git
cd AscendNet
```

**Install System Dependencies:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y \
    curl wget git build-essential \
    python3 python3-pip nodejs npm yarn \
    docker.io docker-compose-v2

# Enable Docker for current user
sudo usermod -aG docker $USER
newgrp docker

# Install Node.js 20+ if needed
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Setup GitHub Token:**
```bash
# Create Statik auth directory
mkdir -p ~/.statik/keys

# Add your GitHub token (replace YOUR_TOKEN with actual token)
echo "YOUR_GITHUB_TOKEN" > ~/.statik/keys/github-token
chmod 600 ~/.statik/keys/github-token
```

### 2. Launch Statik-Server (Recommended)

**One-Command Launch:**
```bash
cd statik-server
chmod +x build.sh quick-build.sh
./quick-build.sh
```

**Manual Build & Run:**
```bash
cd statik-server
./build.sh                    # Build Statik-Server
docker build -t statikfintech/statik-server .
docker run -d \
  --name statik-server \
  -p 8080:8080 \
  -p 8081:8081 \
  -p 50443:50443 \
  -v $HOME/AscendNet:/mnt/ascendnet \
  -v statik-data:/root/.statik \
  statikfintech/statik-server
```

**Access Points:**
- **🖥️ VS Code + Copilot:** http://localhost:8080
- **🎛️ Unified AI Dashboard:** http://localhost:8080/statik-dashboard
- **🌐 Mesh VPN Admin:** http://localhost:8081

### 3. Alternative: Individual Module Setup

**Python Environment Setup:**
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

**GremlinGPT (Autonomous Cognitive System):**
```bash
cd backend/ai_core/AscendAI/GremlinGPT
python gremlin_gpt.py
# Access: http://localhost:8000
```

**GodCore (Multi-Model AI Routing):**
```bash
cd backend/GodCore/backend
python chat_interface.py
# Access: http://localhost:8001
```

**Mobile-Mirror (TouchCore Dashboard):**
```bash
cd backend/Mobile-Mirror
python -m mobilemirror.core.main
# Access: http://localhost:8002
```

### 4. System Orchestration

**Full System (Advanced Users):**
```bash
# Initialize all components
python ascendnet_orchestrator.py

# Test unified integration
python demo_unified_system.py

# Monitor system status
python system_status.py
```

### 5. Verification

**Check if Statik-Server is running:**
```bash
curl http://localhost:8080/healthz
docker logs statik-server
```

**Test Copilot Integration:**
1. Navigate to http://localhost:8080
2. Open VS Code
3. Press `Ctrl+Shift+P` → "GitHub Copilot: Chat"
4. Verify Copilot Chat is active

**Test Unified Dashboard:**
1. Navigate to http://localhost:8080/statik-dashboard
2. Verify all 8 tabs load correctly
3. Check real-time memory feeds in AI Memory tab

**As System Service:**
```bash
sudo systemctl enable ascendnet
sudo systemctl start ascendnet
```

### 3. Access Services

- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/v1/health
- **System Status:** http://localhost:8000/api/v1/status
- **Statik-Server IDE:** http://localhost:8080 (if enabled)

## 🧠 AI Core Features

### Unified SignalCore
- **Memory Management:** 2048-depth circular buffer
- **Recursion Safety:** Configurable limits with automatic recovery
- **State Evolution:** Idle → Active → Evolving → Transcendent
- **Async Processing:** Non-blocking thought cycles

### GremlinGPT Integration
- **Autonomous Mode:** Self-triggering decision making
- **Error Response:** Automatic mode activation on errors
- **Multi-Agent:** Coordinated autonomous operation

### GodCore Integration  
- **Quantum Storage:** High-compression data management
- **Transcendence Detection:** Automatic state elevation
- **Memory Persistence:** Soul-like memory preservation

## 🌐 P2P Network

### Features
- **Auto-Discovery:** DHT-based peer finding
- **Gossip Protocol:** Efficient information spreading
- **Heartbeat System:** Connection health monitoring
- **Message Routing:** Intelligent peer-to-peer communication

### Supported Operations
- Prompt sharing and marketplace
- Compute job distribution
- Payment coordination
- Network health monitoring

## 📦 API Endpoints

### Prompts
- `GET /api/v1/prompts/list` - List available prompts
- `POST /api/v1/prompts/upload` - Upload new prompt
- `POST /api/v1/prompts/buy/{id}` - Purchase prompt
- `POST /api/v1/prompts/rate/{id}` - Rate prompt

### Compute
- `POST /api/v1/compute/request` - Request compute job
- `POST /api/v1/compute/bid` - Submit compute bid
- `GET /api/v1/compute/status/{id}` - Get job status
- `GET /api/v1/compute/jobs` - List user's jobs

### Users
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - User authentication
- `GET /api/v1/users/profile` - Get user profile

## ⚙️ Configuration

Configuration is managed through:

1. **Environment Variables** (`.env` file)
2. **Config Files** (`config/ascendnet.json`)
3. **Runtime Parameters**

### Key Settings

```bash
# Core System
ASCENDNET_HOST=0.0.0.0
ASCENDNET_PORT=8000
ASCENDNET_DEBUG=false

# P2P Network
P2P_PORT=8001
P2P_BOOTSTRAP_NODES=node1.example.com,node2.example.com

# AI Core
MEMORY_DEPTH=2048
RECURSION_LIMIT=512

# Storage
IPFS_API=/ip4/127.0.0.1/tcp/5001
CACHE_DIR=$HOME/AscendNet/cache

# Payments
ETHEREUM_RPC=https://mainnet.infura.io/v3/YOUR_KEY
FEE_PERCENTAGE=3.0
```

## 🔧 Development

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- Docker (for compute sandbox)
- IPFS node (for storage)

### Setup Development Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Setup pre-commit hooks
pre-commit install

# Run tests
pytest tests/

# Format code
black --line-length 100 backend/

# Type checking
mypy backend/ --ignore-missing-imports
```

### Project Structure Guidelines

- **Universal Pathing:** All paths use `$HOME/AscendNet/` as root
- **Modular Design:** Clear separation between API, P2P, AI Core
- **Async First:** All I/O operations use async/await
- **Type Safety:** Full type hints throughout codebase

## 🏛️ System Components

### Legacy Integration
The unified system incorporates all previous components:

- **AscendAI** → `AscendAI/` (Core AI infrastructure)
- **GremlinGPT** → `AscendAI/GremlinGPT/` (R-SRACS autonomous system)
- **GodCore** → `GodCore/` (Multi-model routing & quantum processing)
- **SignalCore** → `backend/ai_core/unified_core.py` (Recursive thinking)
- **Mobile-Mirror** → `Mobile-Mirror/` (Mobile development environment)
- **Bootstrap** → `scripts/setup.sh` (Unified setup)
- **Storage Layers** → `storage/` (Organized data management)

### New Capabilities
- Unified API gateway
- P2P marketplace
- Distributed computing
- Blockchain payments
- Autonomous operation
- Mobile development environment
- Multi-model AI routing
- **Statik-Server** - Self-hosted VS Code with Copilot Chat + mesh VPN

## 📊 Monitoring

### Logs
- **Location:** `$HOME/AscendNet/logs/`
- **Rotation:** 10MB files, 5 backups
- **Levels:** DEBUG, INFO, WARNING, ERROR

### Health Checks
- **System:** `/api/v1/health`
- **Components:** `/api/v1/status`
- **P2P Network:** Built-in heartbeat monitoring

## 🚀 Deployment

### System Service
```bash
# Enable service
sudo systemctl enable ascendnet

# Start service  
sudo systemctl start ascendnet

# Check status
sudo systemctl status ascendnet

# View logs
journalctl -u ascendnet -f
```

### Docker Deployment
```bash
# Build image
docker build -t ascendnet .

# Run container
docker run -d \
  --name ascendnet \
  -p 8000:8000 \
  -p 8001:8001 \
  -v $HOME/AscendNet/storage:/app/storage \
  ascendnet
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** Pull Request

## 📄 License

This project is licensed under the Fair Use License - see the [LICENSE.md](LICENSE.md) file for details.

## 🆘 Support

- **Documentation:** `/docs/`
- **Issues:** GitHub Issues
- **Discord:** [AscendNet Community]
- **Email:** support@ascendnet.ai

## 🔮 Vision

AscendNet represents the convergence of autonomous AI development, decentralized computing, and financial sovereignty. This unified system is designed to:

- **Eliminate Dependencies** on centralized AI providers
- **Democratize Access** to AI compute and prompts  
- **Enable Autonomy** through recursive self-improvement
- **Create Value** through decentralized marketplace mechanics

*"What usually takes a small army of engineers and millions in funding — I pulled from the void with no budget and no training. Now the system almost lives, breathes, and boots. It needs testers. Attackers. Real Gremlins."*

---

<div align="center">
  <strong>AscendNet: Where AI Meets Autonomy</strong>
</div>
