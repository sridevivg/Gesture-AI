# Gesture-AI

AI-powered gesture control platform utilizing computer vision and machine learning to recognize hand gestures, interpret user intent, and execute safe computer and application actions.

---

## Project Purpose

Gesture-AI bridges computer vision intelligence and desktop interaction. By processing video input in real time, extracting 21-point 3D hand landmarks, and classifying spatial and temporal gesture patterns, the platform enables touchless control over host operating system actions such as mouse navigation, media playback, and presentation control. The architecture emphasizes safety guardrails, confidence threshold validation, and strict separation between the web interface, backend orchestration, and machine learning models.

---

## Main Capabilities

* **Hand Landmark Extraction Architecture**: MediaPipe-based 21-point 3D coordinate detection and geometric feature normalization.
* **Dual Recognition Pipelines**: Separation of static hand pose classification and dynamic temporal sequence analysis.
* **Confidence-Based Action Execution**: Safe automation engine enforcing configurable confidence limits and rate-limiting cooldowns.
* **Hardware & Failsafe Guardrails**: Desktop automation integration via PyAutoGUI with corner failsafe killswitches.
* **Real-Time Telemetry Streaming**: Low-latency bidirectional WebSocket communication for live landmark coordinates and recognition feedback.
* **Modern Studio Interface**: React dashboard with HUD camera telemetry overlays, action mapping management, and analytics visualization.
* **Full Containerization**: Multi-service Docker Compose environment with health checks and isolated networking.

---

## System Architecture

The project is structured as a modular monorepo with strict architectural boundaries:

```
                            +-------------------------------+
                            |   Client Camera Video Stream  |
                            +---------------+---------------+
                                            |
                                            v
+-----------------------+       +-----------+-----------+       +-------------------------+
|   PostgreSQL Database | <---> |    FastAPI Backend    | <---> |   ML Inference Engine   |
|   (Relational State)  |       |   (Orchestrator & WS) |       |   (Vision & Models)     |
+-----------------------+       +-----------+-----------+       +-------------------------+
                                            |
+-----------------------+                   |                   +-------------------------+
|      Redis Cache      | <-----------------+-----------------> |  OS Action Controllers  |
|  (Pub/Sub & Streams)  |                                       |  (Pointer/Media/Keys)   |
+-----------------------+                                       +-------------------------+
                                            ^
                                            | REST & WebSockets
                                            v
                                +-----------+-----------+
                                |  React Frontend SPA   |
                                |  (Tailwind & Vite)    |
                                +-----------------------+
```

* **Frontend (`frontend/`)**: React, TypeScript, Vite, Tailwind CSS, TanStack Query, and Recharts. Contains no Python code.
* **Backend (`backend/`)**: FastAPI, Pydantic, SQLAlchemy, Redis, WebSockets, and PyAutoGUI adapters. Contains no React or TypeScript code.
* **Machine Learning (`ml/`)**: OpenCV, MediaPipe, NumPy, Scikit-learn, and PyTorch. Fully decoupled from HTTP and UI concerns.
* **Cross-Service Testing (`tests/`)**: Unit and integration test suites validating schemas, geometry, and API contracts.

---

## Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React, TypeScript, Vite, Tailwind CSS, React Router, TanStack Query, Axios, Zod, Lucide React, Recharts, ESLint, Prettier |
| **Backend** | Python, FastAPI, Pydantic, SQLAlchemy, PostgreSQL, Alembic, Redis, WebSockets, pytest, Ruff, Black |
| **Machine Learning** | Python, OpenCV, MediaPipe, NumPy, Pandas, Scikit-learn, PyTorch, joblib, optional ONNX Runtime |
| **Automation & Adapters** | PyAutoGUI, OS-level input adapters |
| **Infrastructure** | Docker, Docker Compose, GitHub Actions, Make |

---

## Repository Structure

```
Gesture-AI/
├── frontend/             # React TypeScript single-page application
├── backend/              # FastAPI application, database models, and adapters
├── ml/                   # Computer vision, landmark processing, models, and training
├── docs/                 # Architectural documentation and decision records
│   ├── architecture/     # Detailed subsystem and interaction design
│   ├── api/              # REST and WebSocket interface specifications
│   ├── ml/               # Vision pipeline and model taxonomy
│   ├── database/         # Relational schema and migration guides
│   └── decisions/        # Architecture Decision Records (ADRs)
├── scripts/              # Setup, linting, testing, and dev runners
├── tests/                # Unit and integration test suites
│   ├── unit/             # Isolated component tests
│   └── integration/      # End-to-end API and workflow tests
├── docker/               # Dockerfiles for each service
├── .github/              # GitHub Actions CI workflows
├── docker-compose.yml    # Multi-container orchestration definition
├── Makefile              # Convenience task runner
├── pyproject.toml        # Root Python tool configuration (Ruff, Black, pytest)
├── .env.example          # Template environment configuration
├── CONTRIBUTING.md       # Contribution guidelines and coding standards
├── LICENSE               # MIT Open Source License
└── README.md             # Project documentation
```

---

## Local Development Requirements

* **Node.js**: v20 or higher
* **npm**: v10 or higher
* **Python**: 3.9, 3.10, or 3.11
* **Docker & Docker Compose**: Optional for containerized deployment
* **Operating System**: macOS, Linux, or Windows with webcam access

---

## Environment Configuration

Copy the example environment configuration to `.env`:

```bash
cp .env.example .env
```

Key environment settings include:

* `DATABASE_URL`: PostgreSQL connection string.
* `REDIS_URL`: Redis host and port for caching and events.
* `ML_SERVICE_URL`: HTTP endpoint for the standalone ML service (`http://localhost:8001`).
* `ENABLE_SYSTEM_ACTIONS`: Safety toggle to enable or disable actual host keyboard/mouse actions (defaults to `false` for safety).
* `CONFIDENCE_THRESHOLD`: Minimum confidence score required to trigger an action (defaults to `0.80`).

---

## Running the Services Locally

### Automated Setup

Install dependencies across the monorepo:

```bash
make setup
```

### Running the Frontend

Navigate to `frontend/` and start the Vite development server:

```bash
cd frontend
npm install
npm run dev
```

The web application will be accessible at `http://localhost:5173`.

### Running the Backend

Navigate to `backend/` and start the FastAPI ASGI server:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access API documentation at `http://localhost:8000/docs`.

### Running Machine Learning Services

Run the standalone ML inference service:

```bash
cd ml
pip install -r requirements.txt
python -m src.inference.service
```

---

## Docker Usage

Launch the entire stack (PostgreSQL, Redis, Backend, ML Service, and Frontend) with Docker Compose:

```bash
# Build and start all containers
make docker-up

# View live container logs
make docker-logs

# Stop all containers
make docker-down
```

---

## Testing

Execute unit and integration test suites:

```bash
# Run all tests using Makefile
make test

# Or run pytest directly
pytest tests/ -v
```

---

## Code Quality

Ensure code formatting and quality standards prior to committing:

```bash
# Check Python and TypeScript code quality
make lint

# Automatically format Python and TypeScript files
make format
```

* **Python**: Formatted with `black` and linted with `ruff`.
* **TypeScript**: Strict type checking with `tsc` and linted with `eslint`.

---

## Git Workflow

* Use the `main` branch for production-ready code.
* Create descriptive topic branches for new features and bug fixes (e.g. `feature/landmark-smoother`, `fix/websocket-reconnect`).
* Use Conventional Commit messages:
  * `feat: ...`
  * `fix: ...`
  * `docs: ...`
  * `chore: ...`
* Run `make lint` and `make test` before opening pull requests.

---

## Future Capabilities

* Multi-hand interaction tracking (bimanual gesture recognition).
* Custom user gesture enrollment and few-shot fine-tuning.
* Voice command integration fused with hand gesture intent.
* Standalone desktop tray app packaging via Tauri or Electron.
* Embedded ONNX Runtime acceleration for low-power edge hardware.
