#!/usr/bin/env zsh

# AscendNet E2E Testing Suite with dash-cli integration
# Comprehensive testing for the unified AscendNet system

echo "🧪 AscendNet E2E Testing Suite with dash-cli"
echo "============================================="

# Test configuration
ASCENDNET_API="http://localhost:8000"
TEST_RESULTS_DIR="/tmp/ascendnet_test_results"

# Create test results directory
mkdir -p "$TEST_RESULTS_DIR"

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_pattern="$3"
    
    echo "🔍 Testing: $test_name"
    
    local result
    result=$(eval "$test_command" 2>&1)
    local exit_code=$?
    
    if [[ $exit_code -eq 0 && ( -z "$expected_pattern" || "$result" =~ "$expected_pattern" ) ]]; then
        echo "✅ PASS: $test_name"
        echo "$result" > "$TEST_RESULTS_DIR/${test_name}.pass"
        ((TESTS_PASSED++))
    else
        echo "❌ FAIL: $test_name"
        echo "Exit code: $exit_code"
        echo "Output: $result"
        echo "$result" > "$TEST_RESULTS_DIR/${test_name}.fail"
        ((TESTS_FAILED++))
    fi
    echo "---"
}

# Start E2E Test Suite
echo "🚀 Starting E2E tests..."

# Test 1: API Server Health
run_test "api_health" \
    "curl -s --max-time 10 $ASCENDNET_API/health" \
    '"status".*"healthy"'

# Test 2: API Root Endpoint
run_test "api_root" \
    "curl -s --max-time 10 $ASCENDNET_API/" \
    '"message".*"AscendNet"'

# Test 3: API Status Endpoint
run_test "api_status" \
    "curl -s --max-time 10 $ASCENDNET_API/api/status" \
    '"api_status".*"running"'

# Test 4: API Documentation
run_test "api_docs" \
    "curl -s --max-time 10 $ASCENDNET_API/docs" \
    "AscendNet"

# Test 5: OpenAPI Schema
run_test "api_openapi" \
    "curl -s --max-time 10 $ASCENDNET_API/openapi.json" \
    '"openapi"'

# Test 6: Python Backend Compilation
run_test "python_compilation" \
    "cd /home/statiksmoke8/AscendNet && python -m py_compile api_server.py" \
    ""

# Test 7: Virtual Environment
run_test "venv_check" \
    "cd /home/statiksmoke8/AscendNet && source venv/bin/activate && python -c 'import sys; print(\"venv\" in sys.prefix)'" \
    "True"

# Test 8: Package Dependencies
run_test "dependencies_check" \
    "cd /home/statiksmoke8/AscendNet && source venv/bin/activate && python -c 'import fastapi, uvicorn, pydantic; print(\"Dependencies OK\")'" \
    "Dependencies OK"

# Dash-CLI Tests
echo ""
echo "🎯 dash-cli Integration Tests"
echo "============================="

# Test 9: dash-cli Installation
run_test "dashcli_installed" \
    "npm list -g dash-cli" \
    "dash-cli@"

# Test 10: dash-cli Help
run_test "dashcli_help" \
    "npx dash-cli --help" \
    "Usage:"

# Test 11: dash-cli Version
run_test "dashcli_version" \
    "npx dash-cli --version" \
    ""

# Test 12: Node.js Version
run_test "nodejs_version" \
    "node --version" \
    "v[0-9]"

# Test 13: NPM Version
run_test "npm_version" \
    "npm --version" \
    "[0-9]"

# System Integration Tests
echo ""
echo "🔧 System Integration Tests"
echo "==========================="

# Test 14: File System Structure
run_test "filesystem_structure" \
    "ls -la /home/statiksmoke8/AscendNet/ | grep -E '(api_server.py|requirements.txt|backend)'" \
    "api_server.py"

# Test 15: Backend Directory
run_test "backend_directory" \
    "ls -la /home/statiksmoke8/AscendNet/backend/ | grep -E '(ai_core|api)'" \
    "ai_core"

# Test 16: Config Files
run_test "config_files" \
    "ls -la /home/statiksmoke8/AscendNet/config/" \
    "ascendnet.json"

# Test 17: Logs Directory
run_test "logs_directory" \
    "ls -la /home/statiksmoke8/AscendNet/logs/" \
    ""

# Test 18: Process Check
run_test "process_check" \
    "ps aux | grep -E '(python.*api_server|uvicorn)' | grep -v grep" \
    ""

# Advanced Tests
echo ""
echo "🚀 Advanced Integration Tests"
echo "============================="

# Test 19: API Load Test (simple)
run_test "api_load_test" \
    "for i in {1..5}; do curl -s $ASCENDNET_API/health > /dev/null && echo 'Request $i: OK'; done" \
    "Request.*OK"

# Test 20: JSON Response Validation
run_test "json_validation" \
    "curl -s $ASCENDNET_API/health | python -m json.tool" \
    '"status"'

# Test Results Summary
echo ""
echo "📊 Test Results Summary"
echo "======================="
echo "✅ Tests Passed: $TESTS_PASSED"
echo "❌ Tests Failed: $TESTS_FAILED"
echo "📁 Results saved to: $TEST_RESULTS_DIR"

# Overall status
TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
if [[ $TOTAL_TESTS -gt 0 ]]; then
    echo "📈 Success Rate: $(( TESTS_PASSED * 100 / TOTAL_TESTS ))%"
else
    echo "📈 Success Rate: 0%"
fi

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo "🎉 All tests passed! AscendNet system is fully operational."
    echo ""
    echo "🌟 System Status: READY FOR PRODUCTION"
    echo "🔗 API Endpoints:"
    echo "   Health: $ASCENDNET_API/health"
    echo "   Status: $ASCENDNET_API/api/status"
    echo "   Docs:   $ASCENDNET_API/docs"
    echo ""
    echo "📋 Next Steps:"
    echo "   1. Run production workloads"
    echo "   2. Monitor system performance"
    echo "   3. Scale as needed"
    exit 0
else
    echo "⚠️  Some tests failed. Check the results directory for details."
    echo "Failed test files:"
    ls -la "$TEST_RESULTS_DIR"/*.fail 2>/dev/null || echo "No failed test files found."
    echo ""
    echo "🔧 Debugging Commands:"
    echo "   Check API: curl $ASCENDNET_API/health"
    echo "   Check logs: tail -f /home/statiksmoke8/AscendNet/logs/ascendnet.log"
    echo "   Check process: ps aux | grep python"
    exit 1
fi
