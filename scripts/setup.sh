#!/usr/bin/env bash
# ==============================================================================
# Gesture-AI Workspace Setup Script
# ==============================================================================
set -euo pipefail

echo "=========================================="
echo "Initializing Gesture-AI Workspace"
echo "=========================================="

# Check and configure environment file
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

if [ ! -f backend/.env ]; then
    echo "Creating backend/.env from backend/.env.example..."
    cp backend/.env.example backend/.env
fi

if [ ! -f frontend/.env ]; then
    echo "Creating frontend/.env from frontend/.env.example..."
    cp frontend/.env.example frontend/.env
fi

if [ ! -f ml/.env ]; then
    echo "Creating ml/.env from ml/.env.example..."
    cp ml/.env.example ml/.env
fi

# Setup Frontend dependencies
if command -v npm &> /dev/null; then
    echo "Installing frontend dependencies..."
    cd frontend && npm install && cd ..
else
    echo "Warning: npm is not installed. Skipping frontend dependency installation."
fi

# Setup Python dependencies
if command -v pip3 &> /dev/null || command -v pip &> /dev/null; then
    PIP_CMD="pip3"
    command -v pip3 &> /dev/null || PIP_CMD="pip"
    echo "Installing development tooling and Python dependencies..."
    $PIP_CMD install --upgrade pip
    $PIP_CMD install ruff black pytest
    if [ -f backend/requirements.txt ]; then
        echo "Installing backend requirements..."
        $PIP_CMD install -r backend/requirements.txt || echo "Note: Install in dedicated virtualenv if preferred."
    fi
    if [ -f ml/requirements.txt ]; then
        echo "Installing ML requirements..."
        $PIP_CMD install -r ml/requirements.txt || echo "Note: Install in dedicated virtualenv if preferred."
    fi
fi

echo "=========================================="
echo "Gesture-AI Workspace Setup Complete!"
echo "=========================================="
