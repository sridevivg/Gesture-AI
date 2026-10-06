#!/usr/bin/env bash
# ==============================================================================
# Gesture-AI Code Quality and Linting Script
# ==============================================================================
set -euo pipefail

echo "=========================================="
echo "Running Gesture-AI Linters & Format Checks"
echo "=========================================="

# Check Python files
if command -v ruff &> /dev/null; then
    echo "Running Ruff checks on backend, ml, and tests..."
    ruff check backend ml tests
else
    echo "Warning: ruff is not installed. Skipping Ruff linting."
fi

if command -v black &> /dev/null; then
    echo "Running Black formatting check..."
    black --check backend ml tests
else
    echo "Warning: black is not installed. Skipping Black format check."
fi

# Check Frontend files
if [ -d "frontend/node_modules" ]; then
    echo "Running TypeScript typecheck..."
    cd frontend && npm run typecheck && cd ..

    echo "Running ESLint on frontend..."
    cd frontend && npm run lint && cd ..
else
    echo "Frontend node_modules not found. Skipping frontend lint checks."
fi

echo "=========================================="
echo "All linting checks passed successfully!"
echo "=========================================="
