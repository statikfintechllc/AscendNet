# AscendNet Troubleshooting Guide

## 🔧 Common Issues and Solutions

This guide covers the most common issues users encounter when setting up and running AscendNet with Statik-Server.

## 🚨 Installation Issues

### Issue: Docker not found or permission denied

**Symptoms:**
```bash
bash: docker: command not found
# OR
Got permission denied while trying to connect to the Docker daemon socket
```

**Solution:**
```bash
# Install Docker (Ubuntu/Debian)
sudo apt update
sudo apt install -y docker.io docker-compose-v2

# Add user to docker group
sudo usermod -aG docker $USER

# Refresh group membership
newgrp docker

# Test Docker access
docker --version
docker ps
```

### Issue: Node.js version too old

**Symptoms:**
```bash
error: The engine "node" is incompatible with this module. Expected version ">=20.0.0"
```

**Solution:**
```bash
# Install Node.js 20+ via NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify version
node --version  # Should show 20.x.x or higher
```

### Issue: Yarn not installed

**Symptoms:**
```bash
yarn: command not found
```

**Solution:**
```bash
# Install Yarn
npm install -g yarn

# OR via package manager
sudo apt install -y yarn

# Verify installation
yarn --version
```

## 🔐 Authentication Issues

### Issue: GitHub token invalid or expired

**Symptoms:**
```bash
curl -H "Authorization: token $(cat ~/.statik/keys/github-token)" https://api.github.com/user
# Returns: {"message":"Bad credentials","documentation_url":"https://docs.github.com/rest"}
```

**Solution:**
```bash
# 1. Generate new token at https://github.com/settings/tokens
# 2. Select scopes: repo, copilot, user:email
# 3. Update token file
echo "ghp_your_new_token_here" > ~/.statik/keys/github-token
chmod 600 ~/.statik/keys/github-token

# 4. Test token
curl -H "Authorization: token $(cat ~/.statik/keys/github-token)" https://api.github.com/user
```

### Issue: Copilot subscription not active

**Symptoms:**
- Token is valid but Copilot features don't work
- "Copilot not available" messages in VS Code

**Solution:**
```bash
# 1. Verify Copilot subscription at https://github.com/settings/copilot
# 2. Ensure you have an active subscription
# 3. Check token scopes include 'copilot'
# 4. Restart Statik-Server container
docker restart statik-server
```

## 🐳 Container Issues

### Issue: Container fails to start

**Symptoms:**
```bash
docker logs statik-server
# Shows errors like "port already in use" or build failures
```

**Solution:**
```bash
# Check for port conflicts
sudo netstat -tulpn | grep -E ':(8080|8081|50443)'

# Kill conflicting processes
sudo lsof -ti:8080 | xargs sudo kill -9
sudo lsof -ti:8081 | xargs sudo kill -9

# Remove existing container
docker stop statik-server 2>/dev/null || true
docker rm statik-server 2>/dev/null || true

# Restart Docker service
sudo systemctl restart docker

# Rebuild and run
cd AscendNet/statik-server
./quick-build.sh
```

### Issue: Container builds but crashes immediately

**Symptoms:**
```bash
docker ps
# Shows container exited immediately (status: Exited (1))
```

**Solution:**
```bash
# Check detailed logs
docker logs --details statik-server

# Common fixes:
# 1. Insufficient memory
docker run -d --name statik-server --memory=4g statikfintech/statik-server

# 2. Missing authentication
ls -la ~/.statik/keys/github-token

# 3. Rebuild without cache
docker build --no-cache -t statikfintech/statik-server .
```

### Issue: Out of disk space during build

**Symptoms:**
```bash
ERROR: failed to solve: write /var/lib/docker/tmp/...: no space left on device
```

**Solution:**
```bash
# Clean Docker system
docker system prune -af
docker volume prune -f

# Check disk space
df -h

# Move Docker to larger partition if needed
sudo systemctl stop docker
sudo mv /var/lib/docker /path/to/larger/partition/docker
sudo ln -s /path/to/larger/partition/docker /var/lib/docker
sudo systemctl start docker
```

## 🌐 Network Issues

### Issue: Cannot access Statik-Server from browser

**Symptoms:**
- Browser shows "This site can't be reached"
- Connection refused errors

**Solution:**
```bash
# 1. Verify container is running
docker ps | grep statik-server

# 2. Check if ports are bound
docker port statik-server

# 3. Test local connection
curl http://localhost:8080/healthz

# 4. Check firewall settings
sudo ufw status
sudo ufw allow 8080
sudo ufw allow 8081

# 5. Try different port binding
docker run -d --name statik-server -p 9000:8080 statikfintech/statik-server
# Then access via http://localhost:9000
```

### Issue: Mesh VPN not working

**Symptoms:**
- Devices can't connect to mesh
- Preauth keys not working

**Solution:**
```bash
# 1. Check headscale service
docker exec statik-server ps aux | grep headscale

# 2. Generate new preauth key
docker exec statik-server ./internal/mesh/headscale preauthkeys create --namespace statik --reusable

# 3. Check headscale logs
docker exec statik-server tail -f /var/log/headscale.log

# 4. Verify headscale config
docker exec statik-server cat /app/internal/mesh/headscale.yaml
```

## 🎛️ Dashboard Issues

### Issue: Unified dashboard not loading

**Symptoms:**
- http://localhost:8080/statik-dashboard returns 404 or 500 error
- Dashboard shows blank page

**Solution:**
```bash
# 1. Check if dashboard files exist
docker exec statik-server ls -la /app/src/browser/pages/

# 2. Verify API endpoints
curl http://localhost:8080/api/statik/memory

# 3. Check dashboard route registration
docker logs statik-server | grep "statik-dashboard"

# 4. Restart container
docker restart statik-server

# 5. Rebuild if files are missing
cd AscendNet/statik-server
./build.sh
docker build -t statikfintech/statik-server .
```

### Issue: Real-time feeds not updating

**Symptoms:**
- AI Memory tab shows static data
- No live updates from modules

**Solution:**
```bash
# 1. Test SSE endpoint
curl http://localhost:8080/api/statik/memory/live

# 2. Check browser console for JavaScript errors
# Open browser dev tools (F12) and look for errors

# 3. Verify WebSocket connections
# Check Network tab in browser dev tools

# 4. Restart container
docker restart statik-server
```

## 🤖 AI Module Issues

### Issue: GremlinGPT not responding

**Symptoms:**
- Dashboard shows GremlinGPT as offline
- Chat interface not working

**Solution:**
```bash
# 1. Check if AscendNet modules are accessible
ls -la $HOME/AscendNet/backend/ai_core/AscendAI/

# 2. Test direct module access
cd $HOME/AscendNet/backend/ai_core/AscendAI/GremlinGPT
python3 -c "import gremlin_gpt; print('Module OK')"

# 3. Check Python dependencies
source $HOME/AscendNet/venv/bin/activate
pip install -r $HOME/AscendNet/requirements.txt

# 4. Verify module paths in container
docker exec statik-server ls -la /mnt/ascendnet/backend/
```

### Issue: GodCore models not loading

**Symptoms:**
- Model status shows "offline"
- Chat interface returns errors

**Solution:**
```bash
# 1. Check GodCore directory
ls -la $HOME/AscendNet/backend/GodCore/

# 2. Install missing dependencies
cd $HOME/AscendNet/backend/GodCore/backend
pip install -r requirements.txt

# 3. Download required models (if applicable)
# Follow GodCore-specific model setup instructions

# 4. Check model paths and permissions
docker exec statik-server ls -la /mnt/ascendnet/backend/GodCore/
```

## 🔧 Performance Issues

### Issue: High memory usage

**Symptoms:**
- System becomes slow
- Container restarts frequently
- Out of memory errors

**Solution:**
```bash
# 1. Monitor resource usage
docker stats statik-server

# 2. Increase container memory
docker stop statik-server
docker rm statik-server
docker run -d --name statik-server --memory=8g --cpus=4 \
  -p 8080:8080 -p 8081:8081 -p 50443:50443 \
  -v $HOME/AscendNet:/mnt/ascendnet \
  -v statik-data:/root/.statik \
  statikfintech/statik-server

# 3. Optimize VS Code settings
# Disable heavy extensions, reduce file watchers
```

### Issue: Slow dashboard loading

**Symptoms:**
- Dashboard takes long time to load
- API requests timeout

**Solution:**
```bash
# 1. Check system resources
htop
free -h
df -h

# 2. Optimize memory settings
# Add to docker run: --memory=8g --memory-swap=16g

# 3. Use SSD for Docker volumes
docker volume create --driver local \
  --opt type=none \
  --opt o=bind \
  --opt device=/path/to/ssd/statik-data \
  statik-data
```

## 🔍 Debugging Commands

### System Information

```bash
# Check system specs
uname -a
lscpu
free -h
df -h

# Docker information
docker version
docker info
docker system df

# Container inspection
docker inspect statik-server
docker logs --tail 100 statik-server
docker exec statik-server ps aux
```

### Network Debugging

```bash
# Check port usage
sudo netstat -tulpn | grep -E ':(8080|8081|50443)'
sudo lsof -i :8080

# Test connectivity
curl -v http://localhost:8080/healthz
curl -v http://localhost:8080/api/statik/memory
ping localhost

# DNS resolution
nslookup localhost
dig localhost
```

### Application Debugging

```bash
# Check application files
docker exec statik-server find /app -name "*.html" -o -name "*.js" -o -name "*.css" | grep statik

# Test API endpoints
curl -X GET http://localhost:8080/api/statik/memory
curl -X GET http://localhost:8080/api/statik/gremlin
curl -X GET http://localhost:8080/api/statik/godcore

# Monitor logs in real-time
docker logs -f statik-server
```

## 🆘 Getting Help

### Before Asking for Help

1. **Check this troubleshooting guide** for your specific issue
2. **Search existing issues** on the GitHub repository
3. **Collect system information** using the debugging commands above
4. **Try the basic fixes** (restart container, rebuild, check logs)

### When Reporting Issues

Include the following information:

**System Details:**
```bash
# Run these commands and include output
uname -a
docker --version
node --version
python3 --version
```

**Error Information:**
```bash
# Include full error messages and logs
docker logs statik-server
curl -v http://localhost:8080/healthz
```

**Configuration:**
```bash
# Include relevant config (remove sensitive data)
cat ~/.statik/keys/github-token | wc -c  # Should show token length
ls -la ~/.statik/
docker ps
```

### Support Channels

- **GitHub Issues:** https://github.com/statikfintechllc/AscendNet/issues
- **Documentation:** [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- **API Reference:** [docs/API.md](docs/API.md)

## 🔄 Recovery Procedures

### Complete Reset

If all else fails, perform a complete reset:

```bash
# 1. Stop and remove everything
docker stop statik-server 2>/dev/null || true
docker rm statik-server 2>/dev/null || true
docker rmi statikfintech/statik-server 2>/dev/null || true
docker volume rm statik-data 2>/dev/null || true

# 2. Clean Docker system
docker system prune -af
docker volume prune -f

# 3. Remove local data (optional - backup first)
rm -rf ~/.statik/

# 4. Fresh start
cd AscendNet/statik-server
./quick-build.sh
```

### Backup Important Data

Before major changes, backup your configuration:

```bash
# Backup Statik data
tar -czf statik-backup-$(date +%Y%m%d).tar.gz ~/.statik/

# Backup AscendNet project data
tar -czf ascendnet-backup-$(date +%Y%m%d).tar.gz $HOME/AscendNet/

# List backups
ls -la *backup*.tar.gz
```

---

🔧 **Still having issues?** Check the [GitHub Issues](https://github.com/statikfintechllc/AscendNet/issues) or create a new issue with the system information and error details listed above.
