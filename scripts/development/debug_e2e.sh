#!/usr/bin/env zsh

# AscendNet E2E Debugging Script
# This script sets up a comprehensive debugging environment for the AscendNet system

echo "🔧 AscendNet E2E Debugging Environment Setup"
echo "=============================================="

# Set environment variables
export ASCENDNET_ROOT="/home/statiksmoke8/AscendNet"
export ASCENDNET_API_URL="http://localhost:8000"
export STATIK_SERVER_URL="http://localhost:8080"
export DEBUG_MODE=true
export LOG_LEVEL=debug

echo "📍 Environment Variables Set:"
echo "   ASCENDNET_ROOT: $ASCENDNET_ROOT"
echo "   ASCENDNET_API_URL: $ASCENDNET_API_URL"
echo "   STATIK_SERVER_URL: $STATIK_SERVER_URL"

# Test API connectivity
echo "🔗 Testing AscendNet API connectivity..."
if curl -s --max-time 5 $ASCENDNET_API_URL/health > /dev/null; then
    echo "✅ AscendNet API is responding"
    curl -s $ASCENDNET_API_URL/ | jq .
else
    echo "❌ AscendNet API is not responding"
fi

# Check system status
echo "📊 System Status Check..."
echo "   🐍 Python Environment: $(python --version 2>&1)"
echo "   📦 Node.js Environment: $(node --version 2>&1)"
echo "   🔧 NPM Version: $(npm --version 2>&1)"

# Check if dash-cli is available
echo "🎯 Dash CLI Status..."
if command -v dash > /dev/null 2>&1; then
    echo "✅ Dash CLI is available: $(which dash)"
else
    echo "❌ Dash CLI not found - installing..."
    npm install -g dash-cli
fi

# Start debugging session with dash
echo "🚀 Starting E2E Debugging Session..."
echo "   Available Commands:"
echo "   • dash test api    - Test API endpoints"
echo "   • dash test ui     - Test UI components"
echo "   • dash monitor     - Monitor system health"
echo "   • dash logs        - View system logs"

# Create debugging alias functions
alias ascend-api="curl -s $ASCENDNET_API_URL"
alias ascend-health="curl -s $ASCENDNET_API_URL/health | jq ."
alias ascend-status="curl -s $ASCENDNET_API_URL/api/status | jq ."
alias ascend-logs="tail -f $ASCENDNET_ROOT/logs/ascendnet.log"

echo "🎛️ Debug Aliases Created:"
echo "   ascend-api     - Quick API calls"
echo "   ascend-health  - Health check"
echo "   ascend-status  - Status check"
echo "   ascend-logs    - Follow logs"

echo ""
echo "🎯 Ready for E2E Debugging!"
echo "Start with: ascend-health"
