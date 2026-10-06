#!/usr/bin/env bash
# ==============================================================================
# Gesture-AI Development Runner
# Launches backend and frontend concurrently
# ==============================================================================
set -euo pipefail

echo "Starting Gesture-AI local development services..."

cleanup() {
    echo "Shutting down development servers..."
    kill $(jobs -p) 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# Start Backend
echo "Starting Backend API on http://localhost:8000..."
(cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000) &

# Start Frontend
echo "Starting Frontend UI on http://localhost:5173..."
(cd frontend && npm run dev) &

wait
