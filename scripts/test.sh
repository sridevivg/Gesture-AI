#!/usr/bin/env bash
# ==============================================================================
# Gesture-AI Test Runner
# Runs unit and integration tests across subsystems
# ==============================================================================
set -euo pipefail

echo "=========================================="
echo "Executing Gesture-AI Test Suites"
echo "=========================================="

# Python tests
if command -v pytest &> /dev/null; then
    echo "Running Pytest across tests/ and submodules..."
    pytest tests/ -v
else
    echo "Warning: pytest is not installed. Skipping Python tests."
fi

# Frontend tests if configured
if [ -d "frontend/node_modules" ] && [ -f "frontend/package.json" ]; then
    if grep -q '"test"' frontend/package.json; then
        echo "Running frontend test suite..."
        cd frontend && npm test -- --run && cd ..
    fi
fi

echo "=========================================="
echo "All tests executed successfully!"
echo "=========================================="
