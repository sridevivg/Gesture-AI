# ==============================================================================
# Gesture-AI Monorepo Makefile
# ==============================================================================

.PHONY: help setup dev dev-backend dev-frontend dev-ml lint format test docker-up docker-down docker-logs clean

help:
	@echo "Gesture-AI Development Commands:"
	@echo "  make setup          - Install all frontend, backend, and ML dependencies"
	@echo "  make dev            - Run backend and frontend concurrently"
	@echo "  make dev-backend    - Run FastAPI backend development server"
	@echo "  make dev-frontend   - Run Vite React frontend development server"
	@echo "  make dev-ml         - Run ML development service"
	@echo "  make lint           - Run linting checks across frontend, backend, and ML"
	@echo "  make format         - Auto-format code using Black, Ruff, and Prettier"
	@echo "  make test           - Run all unit and integration test suites"
	@echo "  make docker-up      - Start all services with Docker Compose"
	@echo "  make docker-down    - Stop and remove Docker Compose containers"
	@echo "  make docker-logs    - Tail logs from Docker Compose services"
	@echo "  make clean          - Remove temporary build, cache, and test artifacts"

setup:
	@echo "Setting up Gesture-AI workspace..."
	@bash scripts/setup.sh

dev:
	@bash scripts/dev.sh

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

dev-ml:
	python3 -m ml.src.inference.service

lint:
	@bash scripts/lint.sh

format:
	@echo "Formatting Python files with Ruff & Black..."
	ruff format backend ml tests
	black backend ml tests
	@echo "Formatting Frontend files with Prettier..."
	cd frontend && npm run format || true

test:
	@bash scripts/test.sh

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

clean:
	@echo "Cleaning temporary files and caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf frontend/dist
