# AscendNet Installation Guide

## 📋 Complete Setup Instructions

This guide will walk you through setting up the complete AscendNet system with Statik-Server, unified AI dashboard, and all integrated components.

## 🔧 Prerequisites

### System Requirements

**Hardware:**
- CPU: 4+ cores recommended
- RAM: 8GB minimum, 16GB recommended
- Storage: 50GB+ free space
- Network: Stable internet connection

**Operating System:**
- Ubuntu 20.04+ (recommended)
- Debian 11+
- CentOS 8+
- macOS 11+ (experimental)
- Windows 10+ with WSL2 (experimental)

### Required Software

**Base Dependencies:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y \
    curl wget git build-essential \
    python3 python3-pip python3-venv \
    nodejs npm yarn \
    docker.io docker-compose-v2 \
    nginx-light \
    htop tree jq

# CentOS/RHEL
sudo dnf install -y \
    curl wget git gcc gcc-c++ make \
    python3 python3-pip \
    nodejs npm yarn \
    docker docker-compose \
    nginx \
    htop tree jq

# macOS
brew install node yarn docker docker-compose python@3.11 nginx
```

**Docker Setup:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Start Docker service
sudo systemctl enable docker
sudo systemctl start docker

# Test Docker
docker --version
docker-compose --version
```

**Node.js 20+ Setup:**
```bash
# Install Node.js 20+ via NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify versions
node --version  # Should be 20+
npm --version
yarn --version
```

### Required Accounts & Tokens

**1. GitHub Account Setup:**
- Sign up at https://github.com if you don't have an account
- Subscribe to GitHub Copilot at https://github.com/features/copilot
- Verify Copilot access in your account settings

**2. Generate GitHub Personal Access Token:**
```bash
# Go to: https://github.com/settings/tokens
# Click "Generate new token (classic)"
# Select scopes:
#   ✅ repo (Full control of private repositories)
#   ✅ copilot (GitHub Copilot)
#   ✅ user:email (Access user email addresses)
# Copy the generated token (starts with ghp_)
```

**3. Optional: Docker Hub Account:**
- Sign up at https://hub.docker.com for pushing custom images

## 📦 Installation Steps

### Step 1: Clone Repository

```bash
# Clone the main repository
git clone https://github.com/statikfintechllc/AscendNet.git
cd AscendNet

# Verify structure
tree -L 2
```

### Step 2: Setup Authentication

```bash
# Create Statik auth directory
mkdir -p ~/.statik/keys
mkdir -p ~/.statik/{db,extensions,userdata}

# Add your GitHub token (replace YOUR_TOKEN)
echo "ghp_your_actual_token_here" > ~/.statik/keys/github-token
chmod 600 ~/.statik/keys/github-token

# Verify token file
ls -la ~/.statik/keys/
```

### Step 3: Python Environment Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python -c "import fastapi, uvicorn; print('✅ Python deps installed')"
```

### Step 4: Build Statik-Server

```bash
cd statik-server

# Make scripts executable
chmod +x build.sh startup.sh quick-build.sh

# Run the build process
./build.sh
```

**Build Process Explanation:**
1. Downloads and forks statik-server to Statik-Server
2. Patches VS Code to version 1.102.0+ with Copilot Chat
3. Embeds headscale mesh VPN server
4. Creates Copilot authentication integration
5. Builds unified AI dashboard
6. Configures Docker container

### Step 5: Launch Statik-Server

**Option A: Quick Launch (Recommended)**
```bash
./quick-build.sh
```

**Option B: Manual Launch**
```bash
# Build Docker image
docker build -t statikfintech/statik-server .

# Run container
docker run -d \
  --name statik-server \
  --restart unless-stopped \
  -p 8080:8080 \
  -p 8081:8081 \
  -p 50443:50443 \
  -v $HOME/AscendNet:/mnt/ascendnet \
  -v statik-data:/root/.statik \
  -v /var/run/docker.sock:/var/run/docker.sock \
  statikfintech/statik-server

# Check logs
docker logs -f statik-server
```

### Step 6: Access & Verification

**Primary Access Points:**
- **VS Code Interface:** http://localhost:8080
- **Unified Dashboard:** http://localhost:8080/statik-dashboard
- **Mesh VPN Admin:** http://localhost:8081

**Verification Commands:**
```bash
# Check container status
docker ps | grep statik-server

# Check application health
curl http://localhost:8080/healthz

# Check dashboard access
curl -I http://localhost:8080/statik-dashboard

# View real-time logs
docker logs -f statik-server
```

## 🎛️ Using the Unified Dashboard

### Dashboard Features

**1. Overview Tab:**
- System status monitoring
- Quick navigation panel
- Real-time performance metrics

**2. VS Code Tab:**
- Embedded VS Code interface
- Copilot Chat integration
- Full development environment

**3. GremlinGPT Tab:**
- Autonomous cognitive system control
- FSM state management
- Signal trace visualization

**4. GodCore Tab:**
- Multi-model AI routing
- Model selection and monitoring
- Advanced chat interface

**5. Mobile-Mirror Tab:**
- TouchCore dashboard
- Remote device management
- PWA installation status

**6. AI Memory Tab:**
- Real-time memory feeds
- Cross-module state monitoring
- Soul integrity tracking

**7. Mesh VPN Tab:**
- Network node management
- Preauth key generation
- Connection monitoring

**8. System Tab:**
- Service management
- System administration
- Memory export/import

## 🔧 Advanced Configuration

### Custom Port Configuration

```bash
# Edit docker run command with custom ports
docker run -d \
  --name statik-server \
  -p 9000:8080 \   # VS Code on port 9000
  -p 9001:8081 \   # VPN admin on port 9001
  -p 60443:50443 \ # gRPC on port 60443
  statikfintech/statik-server
```

### External Database Integration

```bash
# Create custom headscale config
mkdir -p ~/.statik/config

cat > ~/.statik/config/headscale.yaml << 'EOF'
database:
  type: postgres
  postgres:
    host: your-postgres-host
    port: 5432
    name: headscale
    user: headscale
    pass: your-password
EOF

# Mount config in container
docker run -d \
  -v ~/.statik/config:/root/.statik/config \
  statikfintech/statik-server
```

### SSL/TLS Configuration

```bash
# Generate SSL certificates
mkdir -p ~/.statik/ssl
openssl req -x509 -newkey rsa:4096 -keyout ~/.statik/ssl/key.pem -out ~/.statik/ssl/cert.pem -days 365 -nodes

# Update nginx configuration
cat > ~/.statik/config/nginx.conf << 'EOF'
server {
    listen 443 ssl;
    ssl_certificate /root/.statik/ssl/cert.pem;
    ssl_certificate_key /root/.statik/ssl/key.pem;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF
```

## 📱 Mobile Device Setup

### Connect Mobile Devices to Mesh VPN

**1. Generate Preauth Key:**
```bash
# Access VPN admin at http://localhost:8081
# Or generate via CLI:
docker exec statik-server ./internal/mesh/headscale preauthkeys create --namespace statik --reusable
```

**2. Install Tailscale on Mobile:**
- iOS: Download Tailscale from App Store
- Android: Download Tailscale from Google Play Store

**3. Connect with Preauth Key:**
- Open Tailscale app
- Select "Connect to tailnet"
- Enter the preauth key from step 1
- Configure login URL: `http://your-server-ip:8081`

## 🔍 Troubleshooting

### Common Issues

**Issue: Container won't start**
```bash
# Check Docker logs
docker logs statik-server

# Check port conflicts
sudo netstat -tulpn | grep -E ':(8080|8081|50443)'

# Restart Docker service
sudo systemctl restart docker
```

**Issue: GitHub token not working**
```bash
# Verify token file
cat ~/.statik/keys/github-token

# Test token validity
curl -H "Authorization: token $(cat ~/.statik/keys/github-token)" \
     https://api.github.com/user

# Regenerate token if needed
```

**Issue: Copilot not activating**
```bash
# Check VS Code settings
# Go to: http://localhost:8080
# Open Command Palette (Ctrl+Shift+P)
# Type: "GitHub Copilot: Check Status"
# Verify authentication
```

**Issue: Dashboard not loading**
```bash
# Check if dashboard files exist
docker exec statik-server ls -la /app/src/browser/pages/

# Check API endpoints
curl http://localhost:8080/api/statik/memory

# Restart container
docker restart statik-server
```

### Performance Optimization

**Increase Container Resources:**
```bash
docker run -d \
  --name statik-server \
  --memory=8g \
  --cpus=4 \
  statikfintech/statik-server
```

**Enable SSD Caching:**
```bash
# Use SSD for Docker volumes
docker volume create --driver local \
  --opt type=none \
  --opt o=bind \
  --opt device=/path/to/ssd/statik-data \
  statik-data
```

## 🚀 Next Steps

### Development Workflow

**1. Access Development Environment:**
- Navigate to http://localhost:8080
- Open a project folder
- Start coding with Copilot assistance

**2. Monitor AI Systems:**
- Check unified dashboard at http://localhost:8080/statik-dashboard
- Monitor real-time memory feeds
- Control autonomous systems

**3. Mobile Development:**
- Connect mobile devices via mesh VPN
- Access development server from mobile
- Test applications in real-time

### Advanced Features

**Enable Individual AI Modules:**
```bash
# From host machine (if needed)
source venv/bin/activate

# Start GremlinGPT
cd backend/ai_core/AscendAI/GremlinGPT
python gremlin_gpt.py &

# Start GodCore
cd backend/GodCore/backend  
python chat_interface.py &

# Start Mobile-Mirror
cd backend/Mobile-Mirror
python -m mobilemirror.core.main &
```

## 📚 Additional Resources

- **Main Documentation:** `/docs/README.md`
- **API Reference:** `/docs/API.md`
- **Architecture Guide:** `/docs/ARCHITECTURE.md`
- **Troubleshooting:** `/docs/TROUBLESHOOTING.md`
- **Contributing:** `/CONTRIBUTING.md`

## ⚡ Quick Reference

**Essential Commands:**
```bash
# Start system
cd AscendNet/statik-server && ./quick-build.sh

# Check status
docker ps && curl http://localhost:8080/healthz

# View logs
docker logs -f statik-server

# Stop system
docker stop statik-server

# Restart system
docker restart statik-server

# Clean up
docker stop statik-server && docker rm statik-server
```

**Access Points:**
- VS Code: http://localhost:8080
- Dashboard: http://localhost:8080/statik-dashboard  
- VPN Admin: http://localhost:8081
- API Base: http://localhost:8080/api/statik/

---

🎉 **Congratulations!** You now have a complete sovereign AI development environment running with unified dashboard, Copilot Chat, and mesh VPN integration.
