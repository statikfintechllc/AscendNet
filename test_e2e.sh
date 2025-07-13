#!/usr/bin/env zsh

# AscendNet E2E Testing Suite
# Comprehensive testing for the unified AscendNet system

echo "🧪 AscendNet E2E Testing Suite"
echo "==============================="

# Test configuration
ASCENDNET_API="http://localhost:8000"
STATIK_SERVER="http://localhost:8080"
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
    
    if [[ $exit_code -eq 0 && "$result" =~ "$expected_pattern" ]]; then
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
    "AscendNet Unified API"

# Test 5: OpenAPI Schema
run_test "api_openapi" \
    "curl -s --max-time 10 $ASCENDNET_API/openapi.json" \
    '"openapi"'

# Test 6: Python Backend Compilation
run_test "python_compilation" \
    "cd /home/statiksmoke8/AscendNet && python -m py_compile api_server.py" \
    ""

# Test 7: Python Ask Monday Handler
run_test "python_ask_monday" \
    "cd /home/statiksmoke8/AscendNet && python -m py_compile backend/ai_core/AscendAI/GremlinGPT/scraper/ask_monday_handler.py" \
    ""

# Test 8: Environment Variables
run_test "environment_check" \
    "python -c 'import os; print(\"✓ Python:\", os.sys.version.split()[0]); print(\"✓ Path:\", os.getcwd())'" \
    "Python"

# Test 9: Virtual Environment
run_test "venv_check" \
    "cd /home/statiksmoke8/AscendNet && source venv/bin/activate && python -c 'import sys; print(\"venv\" in sys.prefix)'" \
    "True"

# Test 10: Package Dependencies
run_test "dependencies_check" \
    "cd /home/statiksmoke8/AscendNet && source venv/bin/activate && python -c 'import fastapi, uvicorn, pydantic; print(\"Dependencies OK\")'" \
    "Dependencies OK"

# Test Results Summary
echo ""
echo "📊 Test Results Summary"
echo "======================="
echo "✅ Tests Passed: $TESTS_PASSED"
echo "❌ Tests Failed: $TESTS_FAILED"
echo "📁 Results saved to: $TEST_RESULTS_DIR"

# Overall status
TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
echo "📈 Success Rate: $(( TESTS_PASSED * 100 / TOTAL_TESTS ))%"

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo "🎉 All tests passed! AscendNet system is fully operational."
    exit 0
else
    echo "⚠️  Some tests failed. Check the results directory for details."
    echo "Failed test files:"
    ls -la "$TEST_RESULTS_DIR"/*.fail 2>/dev/null || echo "No failed test files found."
    exit 1
fi
