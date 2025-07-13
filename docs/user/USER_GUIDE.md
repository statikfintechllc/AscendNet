# AscendNet User Guide

## 🎯 Getting Started

Welcome to AscendNet - your complete sovereign AI development environment! This guide will help you get the most out of all the features available in the unified Statik-Server system.

## 🚀 First Time Setup

### 1. Quick Installation

Follow the complete installation process:

```bash
# Clone repository
git clone https://github.com/statikfintechllc/AscendNet.git
cd AscendNet

# Setup GitHub authentication
mkdir -p ~/.statik/keys
echo "your_github_token_here" > ~/.statik/keys/github-token
chmod 600 ~/.statik/keys/github-token

# Build and launch
cd statik-server
chmod +x quick-build.sh
./quick-build.sh
```

### 2. First Access

Open your browser and navigate to:
- **Main Interface:** http://localhost:8080
- **Unified Dashboard:** http://localhost:8080/statik-dashboard

## 🎛️ Using the Unified Dashboard

### Overview Tab

**What you'll see:**
- System health indicators
- Quick navigation panel
- Real-time performance metrics
- Service status overview

**Key features:**
- 🟢 Green indicators = services running
- 🔴 Red indicators = services offline
- 📊 Memory usage visualization
- ⚡ Quick access buttons to all modules

### VS Code Tab

**Complete development environment:**
- Full VS Code interface in your browser
- GitHub Copilot Chat integration
- File explorer with your projects
- Integrated terminal

**Getting started:**
1. Click "Open Folder" to select your project
2. Install extensions as needed
3. Press `Ctrl+Shift+P` to open command palette
4. Type "GitHub Copilot" to access AI features

**Copilot Chat Usage:**
- Press `Ctrl+Shift+I` to open Copilot Chat
- Ask questions like "Explain this code" or "Add error handling"
- Use `/` commands for specific actions
- Chat persists across sessions

### GremlinGPT Tab

**Autonomous AI system control:**

**FSM States:**
- **Idle:** Waiting for input
- **Thinking:** Processing information
- **Active:** Executing tasks
- **Evolving:** Self-improvement mode
- **Autonomous:** Self-directed operation

**Controls:**
- **Autonomous Toggle:** Enable/disable self-directed mode
- **Step:** Manually advance to next state
- **Reset:** Return to idle state
- **Pause:** Temporarily halt processing

**Chat Interface:**
- Direct communication with GremlinGPT
- View decision pathways
- Monitor signal traces

### GodCore Tab

**Multi-model AI routing:**

**Model Selection:**
- **Auto:** Intelligent routing based on query type
- **Mistral:** Open-source model for general tasks
- **GPT-4:** Advanced reasoning (if configured)
- **Claude:** Anthropic model for analysis
- **Monday.AI:** Custom business logic model

**Features:**
- Model load monitoring
- Response time tracking
- Routing optimization
- Chat interface with model selection

**Usage Tips:**
- Use "Auto" for best results
- Monitor model loads to avoid overuse
- Switch models for different task types

### Mobile-Mirror Tab

**Remote development environment:**

**TouchCore Dashboard:**
- Device management interface
- Remote debugging tools
- PWA installation controls
- Cross-device synchronization

**Connected Devices:**
- View all connected mobile devices
- Monitor connection status
- Start/stop tunnels
- Access device debugging

**Features:**
- Real-time mobile development
- Remote debugging capabilities
- PWA testing environment
- Cross-platform compatibility

### AI Memory Tab

**Real-time system monitoring:**

**Live Memory Feeds:**
- GremlinGPT state changes
- GodCore model activities
- Mobile-Mirror connections
- SignalCore processing

**Memory Metrics:**
- Memory depth tracking
- Recursion count monitoring
- Soul integrity percentage
- Cross-module synchronization

**Controls:**
- Export memory snapshots
- Clear memory states
- Monitor real-time updates
- View historical data

### Mesh VPN Tab

**Network management:**

**Node Management:**
- View connected devices
- Monitor connection status
- Check network latency
- Manage device access

**Key Generation:**
- Create preauth keys for new devices
- Generate unlimited device keys
- No expiration limits
- Reusable keys for easy onboarding

**Network Statistics:**
- Bytes in/out monitoring
- Connection latency tracking
- Node discovery status
- Mesh topology visualization

### System Tab

**Complete system administration:**

**Service Management:**
- Start/stop individual services
- Monitor service health
- View service logs
- Restart system components

**System Controls:**
- Full system restart
- Update system components
- Memory management
- Configuration backup

**Monitoring:**
- CPU usage tracking
- Memory consumption
- Disk space monitoring
- Network activity

## 📱 Mobile Device Setup

### Connecting Devices to Mesh VPN

**1. Generate Device Key:**
- Go to Mesh VPN tab in dashboard
- Click "Generate Preauth Key"
- Copy the generated key

**2. Install Tailscale:**
- **iOS:** Download from App Store
- **Android:** Download from Google Play
- **Windows/Mac/Linux:** Download from tailscale.com

**3. Connect Device:**
- Open Tailscale app
- Select "Add Account" or "Connect to tailnet"
- Enter your server IP: `your-server-ip:8081`
- Use the preauth key from step 1
- Device will automatically join the mesh

**4. Access Development Environment:**
- Once connected, access via mesh IP
- Usually `http://100.64.0.1:8080`
- Full VS Code access from mobile browser
- TouchCore dashboard for mobile-specific tools

## 💻 Development Workflows

### Standard Development

**1. Project Setup:**
```bash
# Access VS Code tab in dashboard
# Click "Open Folder" and select your project
# Or clone directly in terminal
git clone https://github.com/your-project.git
```

**2. Coding with Copilot:**
- Write code with AI assistance
- Use Copilot Chat for explanations
- Get suggestions for improvements
- Generate tests and documentation

**3. Testing and Debugging:**
- Use integrated terminal
- Run tests in VS Code
- Debug with breakpoints
- Monitor performance in System tab

### AI-Assisted Development

**1. Using GremlinGPT:**
- Enable autonomous mode for background assistance
- Chat directly for complex problem solving
- Monitor FSM states for AI decision making
- Use signal traces to understand AI reasoning

**2. Multi-Model Queries:**
- Use GodCore tab for complex questions
- Switch between models based on task
- Compare responses from different models
- Optimize routing for best performance

**3. Cross-Platform Development:**
- Connect mobile devices via mesh VPN
- Test mobile apps in real-time
- Use TouchCore for mobile-specific debugging
- Deploy PWAs directly to devices

### Collaborative Development

**1. Team Mesh Setup:**
- Generate preauth keys for team members
- Share server access details
- Each member connects via mesh VPN
- Collaborative editing through VS Code Live Share

**2. AI Model Sharing:**
- Team members share GodCore model access
- Collaborative GremlinGPT sessions
- Shared memory states across team
- Real-time project synchronization

## 🔧 Customization

### VS Code Extensions

**Install extensions through VS Code interface:**
- Click Extensions icon in VS Code tab
- Search and install preferred extensions
- Extensions persist across sessions
- Sync settings across devices

**Recommended Extensions:**
- GitHub Copilot (pre-installed)
- GitLens
- Docker
- Python
- JavaScript/TypeScript

### Dashboard Customization

**Theme Customization:**
- Dark theme is default
- Modify CSS in dashboard files
- Custom color schemes
- Responsive layout adjustments

**Widget Configuration:**
- Customize overview panel
- Add/remove monitoring widgets
- Adjust update frequencies
- Configure alert thresholds

### AI Model Configuration

**GodCore Model Setup:**
- Add custom models to routing
- Configure model endpoints
- Set load balancing preferences
- Adjust response timeouts

**GremlinGPT Tuning:**
- Modify FSM state transitions
- Adjust autonomous behavior
- Configure decision trees
- Set memory retention policies

## 🔍 Monitoring and Debugging

### System Health Monitoring

**Dashboard Indicators:**
- Green = Healthy
- Yellow = Warning
- Red = Error/Offline

**Key Metrics to Watch:**
- Memory usage (should stay under 80%)
- CPU usage (spikes normal, sustained high concerning)
- Disk space (ensure adequate free space)
- Network latency (under 100ms optimal)

### Troubleshooting Common Issues

**Container Won't Start:**
1. Check Docker status: `docker ps`
2. View logs: `docker logs statik-server`
3. Check port conflicts: `sudo netstat -tulpn | grep 8080`
4. Restart Docker: `sudo systemctl restart docker`

**Dashboard Not Loading:**
1. Check API endpoints: `curl http://localhost:8080/api/statik/memory`
2. Verify dashboard files exist
3. Check browser console for errors
4. Restart container: `docker restart statik-server`

**Copilot Not Working:**
1. Verify GitHub token: `cat ~/.statik/keys/github-token`
2. Test token: `curl -H "Authorization: token $(cat ~/.statik/keys/github-token)" https://api.github.com/user`
3. Check Copilot subscription status
4. Regenerate token if needed

### Performance Optimization

**Container Resources:**
```bash
# Increase memory and CPU allocation
docker run -d --name statik-server \
  --memory=8g --cpus=4 \
  statikfintech/statik-server
```

**SSD Optimization:**
```bash
# Use SSD for Docker volumes
docker volume create --driver local \
  --opt type=none \
  --opt o=bind \
  --opt device=/path/to/ssd \
  statik-data
```

## 🚀 Advanced Features

### API Integration

**Custom Scripts:**
```python
import requests

# Get system status
status = requests.get('http://localhost:8080/api/statik/status').json()
print(f"System health: {status['status']}")

# Chat with AI modules
gremlin_response = requests.post(
    'http://localhost:8080/api/statik/gremlin/chat',
    json={'message': 'Hello from script'}
).json()
```

### Automation

**Automated Monitoring:**
```bash
#!/bin/bash
# System health check script

# Check container status
if ! docker ps | grep -q statik-server; then
    echo "Container not running, restarting..."
    docker restart statik-server
fi

# Check API health
if ! curl -s http://localhost:8080/healthz > /dev/null; then
    echo "API not responding, investigating..."
    docker logs --tail 50 statik-server
fi
```

### Custom Integrations

**Webhook Setup:**
- Configure webhooks for external integrations
- Set up notifications for AI state changes
- Integrate with project management tools
- Connect to CI/CD pipelines

## 📚 Learning Resources

### Documentation

- **Installation Guide:** Complete setup instructions
- **API Reference:** All available endpoints
- **Troubleshooting:** Common issues and solutions
- **Architecture:** System design overview

### Tutorials

**Basic Usage:**
1. Setting up your first project
2. Using Copilot Chat effectively
3. Connecting mobile devices
4. Monitoring AI systems

**Advanced Topics:**
1. Custom AI model integration
2. Multi-user collaboration setup
3. Performance optimization
4. Security best practices

### Community

- **GitHub Issues:** Report bugs and request features
- **Discussions:** Community support and ideas
- **Wiki:** User-contributed guides
- **Examples:** Sample projects and configurations

## 🎯 Best Practices

### Security

**Token Management:**
- Keep GitHub tokens secure
- Regularly rotate access tokens
- Use environment variables for sensitive data
- Monitor access logs

**Network Security:**
- Use mesh VPN for remote access
- Configure firewall rules appropriately
- Monitor unauthorized access attempts
- Keep system updated

### Performance

**Resource Management:**
- Monitor memory usage regularly
- Clean up unused Docker images
- Optimize VS Code extensions
- Use SSD storage when possible

**AI Model Usage:**
- Use appropriate models for tasks
- Monitor model load balancing
- Optimize query patterns
- Cache frequent responses

### Maintenance

**Regular Tasks:**
- Backup configuration files
- Update system components
- Clean temporary files
- Monitor log files

**Scheduled Maintenance:**
- Weekly system health checks
- Monthly security updates
- Quarterly performance reviews
- Annual architecture reviews

---

🎉 **You're now ready to make the most of your AscendNet sovereign AI development environment!** Explore all the features, experiment with the AI modules, and build amazing projects with your complete development stack.
