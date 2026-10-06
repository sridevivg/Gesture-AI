# Gesture-AI Backend Subsystem

## Overview

The Gesture-AI backend service is built with FastAPI, SQLAlchemy (asyncpg), Redis, and WebSockets. It serves as the orchestrator connecting the web client, the machine learning inference services, persistence layers, and desktop automation adapters.

---

## Architecture and Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── router.py             # Root API router
│   │   └── v1/
│   │       ├── router.py         # Version 1 router
│   │       ├── endpoints/        # Thin REST endpoints
│   │       │   ├── health.py     # System health and status checks
│   │       │   ├── gestures.py   # Gesture taxonomy and registry
│   │       │   ├── actions.py    # Action mapping definitions
│   │       │   └── sessions.py   # Active session tracking
│   │       └── websockets/
│   │           └── gesture_stream.py # Real-time stream handler
│   ├── core/
│   │   ├── config.py             # Pydantic BaseSettings configuration
│   │   ├── database.py           # SQLAlchemy async engine and session factory
│   │   ├── redis.py              # Redis client connection pool
│   │   └── logging.py            # Structured logging configuration
│   ├── models/                   # SQLAlchemy ORM models
│   ├── schemas/                  # Pydantic input/output schemas
│   ├── services/                 # Domain business logic & ML integration
│   │   ├── gesture_service.py    # Gesture query and registry logic
│   │   ├── action_executor.py    # Cooldown verification & safe dispatch
│   │   └── ml_client.py          # Clean interface to ML inference layer
│   └── adapters/                 # Hardware & operating system automation
│       ├── system_controller.py  # Pointer and keyboard emulation
│       └── media_controller.py   # Media playback controls
├── alembic/                      # Database migrations
├── alembic.ini                   # Alembic configuration
├── pyproject.toml                # Linters and test settings
└── requirements.txt              # Production and development dependencies
```

---

## Local Development

### 1. Environment Configuration

```bash
cp .env.example .env
```

### 2. Dependency Installation

```bash
pip install -r requirements.txt
```

### 3. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Interactive Documentation

Once the server is running, explore the interactive OpenAPI documentation:
* Swagger UI: `http://localhost:8000/docs`
* ReDoc UI: `http://localhost:8000/redoc`

---

## Code Quality Standards

```bash
# Run Ruff lint check
ruff check .

# Run Black formatting check
black --check .

# Run backend unit tests
pytest
```
