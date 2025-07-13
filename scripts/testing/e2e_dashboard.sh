#!/usr/bin/env zsh

# AscendNet E2E Debugging Dashboard
# Real-time system monitoring and dash-cli integration

clear
echo "🚀 AscendNet E2E Debugging Dashboard"
echo "====================================="
echo "Linux zsh VM with dash-cli integration"
echo ""

# Configuration
API_BASE="http://localhost:8000"

# Dashboard function
show_dashboard() {
    echo "📊 System Status Dashboard - $(date)"
    echo "======================================="
    
    # API Health
    echo "🔗 API Health:"
    health_response=$(curl -s --max-time 5 "$API_BASE/health" 2>/dev/null)
    if [[ $? -eq 0 ]]; then
        echo "   ✅ API Server: ONLINE"
        echo "   📋 Response: $health_response"
    else
        echo "   ❌ API Server: OFFLINE"
    fi
    
    echo ""
    
    # System Resources
    echo "💻 System Resources:"
    echo "   🖥️  Memory: $(free -h | grep Mem | awk '{print $3"/"$2}')"
    echo "   💾 Disk: $(df -h /home/statiksmoke8/AscendNet | tail -1 | awk '{print $3"/"$2" ("$5" used)"}')"
    echo "   ⚡ Load: $(uptime | awk -F'load average:' '{print $2}')"
    
    echo ""
    
    # Process Status
    echo "🔄 Process Status:"
    python_procs=$(ps aux | grep -E '(python.*api_server|uvicorn)' | grep -v grep | wc -l)
    if [[ $python_procs -gt 0 ]]; then
        echo "   ✅ API Server Process: RUNNING ($python_procs processes)"
    else
        echo "   ❌ API Server Process: NOT FOUND"
    fi
    
    echo ""
    
    # Network Status
    echo "🌐 Network Status:"
    port_8000=$(netstat -tlpn 2>/dev/null | grep :8000 | wc -l)
    if [[ $port_8000 -gt 0 ]]; then
        echo "   ✅ Port 8000: LISTENING"
    else
        echo "   ❌ Port 8000: NOT LISTENING"
    fi
    
    echo ""
    
    # dash-cli Status
    echo "🔧 dash-cli Integration:"
    if command -v dash-cli &> /dev/null; then
        echo "   ✅ dash-cli: INSTALLED"
        echo "   📦 Version: $(npm list -g dash-cli 2>/dev/null | grep dash-cli || echo 'Unknown')"
    else
        echo "   ❌ dash-cli: NOT FOUND"
    fi
    
    echo ""
    
    # Quick Actions
    echo "⚡ Quick Actions:"
    echo "   1. Test API:        curl $API_BASE/health"
    echo "   2. Check Status:    curl $API_BASE/api/status"
    echo "   3. View Docs:       open $API_BASE/docs"
    echo "   4. Restart Server:  python api_server.py"
    echo "   5. Check Logs:      tail -f logs/ascendnet.log"
    echo "   6. Run Tests:       ./production_e2e.sh"
    echo ""
    
    # dash-cli Examples
    echo "🎯 dash-cli Usage Examples:"
    echo "   Search docs:        npx dash-cli javascript"
    echo "   Python docs:        npx dash-cli python"
    echo "   FastAPI docs:       npx dash-cli fastapi"
    echo "   Get help:           npx dash-cli --help"
    echo ""
}

# Interactive menu
interactive_menu() {
    while true; do
        echo "🔧 Interactive Debugging Menu"
        echo "=============================="
        echo "1. 📊 Show Dashboard"
        echo "2. 🧪 Run E2E Tests"
        echo "3. 🔍 Test API Endpoint"
        echo "4. 📚 Search Documentation (dash-cli)"
        echo "5. 🔄 Restart API Server"
        echo "6. 📝 View Logs"
        echo "7. 🚪 Exit"
        echo ""
        echo -n "Select option (1-7): "
        read choice
        
        case $choice in
            1)
                clear
                show_dashboard
                echo ""
                echo "Press Enter to continue..."
                read
                clear
                ;;
            2)
                echo "🧪 Running E2E Tests..."
                ./production_e2e.sh
                echo ""
                echo "Press Enter to continue..."
                read
                clear
                ;;
            3)
                echo "🔍 Testing API Endpoints..."
                echo "Health Check:"
                curl -s "$API_BASE/health" | python -m json.tool 2>/dev/null || echo "Failed to connect"
                echo ""
                echo "Status Check:"
                curl -s "$API_BASE/api/status" | python -m json.tool 2>/dev/null || echo "Failed to connect"
                echo ""
                echo "Press Enter to continue..."
                read
                clear
                ;;
            4)
                echo "📚 dash-cli Documentation Search"
                echo "Available topics: javascript, python, fastapi, react, node, etc."
                echo -n "Enter search term: "
                read search_term
                if [[ -n "$search_term" ]]; then
                    echo "Searching for: $search_term"
                    timeout 10s npx dash-cli "$search_term" || echo "Search completed or timed out"
                else
                    echo "No search term provided"
                fi
                echo ""
                echo "Press Enter to continue..."
                read
                clear
                ;;
            5)
                echo "🔄 Restarting API Server..."
                pkill -f "python.*api_server" 2>/dev/null
                sleep 2
                echo "Starting API server in background..."
                nohup python api_server.py > /dev/null 2>&1 &
                sleep 3
                echo "Server restart attempted"
                echo ""
                echo "Press Enter to continue..."
                read
                clear
                ;;
            6)
                echo "📝 Recent Logs:"
                if [[ -f "logs/ascendnet.log" ]]; then
                    tail -20 logs/ascendnet.log
                else
                    echo "No log file found at logs/ascendnet.log"
                fi
                echo ""
                echo "Press Enter to continue..."
                read
                clear
                ;;
            7)
                echo "👋 Exiting dashboard..."
                exit 0
                ;;
            *)
                echo "❌ Invalid option. Please select 1-7."
                sleep 2
                clear
                ;;
        esac
    done
}

# Check if running interactively
if [[ "$1" == "--interactive" ]] || [[ "$1" == "-i" ]]; then
    clear
    interactive_menu
else
    # Just show dashboard once
    show_dashboard
fi
