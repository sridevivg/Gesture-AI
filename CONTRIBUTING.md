# Contributing to Gesture-AI

Thank you for your interest in contributing to Gesture-AI. This document outlines the development workflow, code quality standards, and submission guidelines.

---

## Code of Conduct

All contributors are expected to uphold a welcoming, inclusive, and professional environment. Respectful collaboration and constructive feedback are essential.

---

## Repository Architecture

Gesture-AI follows a monorepo structure with strict separation of concerns:

* `frontend/`: Web user interface built with React, TypeScript, Vite, and Tailwind CSS.
* `backend/`: REST APIs, WebSockets, database models, and action execution engine built with FastAPI and SQLAlchemy.
* `ml/`: Machine learning models, landmark processing, dataset tooling, and inference pipelines.
* `docs/`: System documentation, architectural decision records, and API specifications.
* `scripts/`: Development, setup, and maintenance automation scripts.
* `tests/`: End-to-end and cross-service integration test suites.
* `docker/`: Docker container definitions for frontend, backend, and machine learning services.
* `.github/`: Continuous integration workflows and repository automation.

### Architectural Rules

* The frontend must never contain Python code.
* The backend must never contain React or TypeScript code.
* Machine-learning training and inference code must reside strictly under `ml/`.
* The backend communicates with the ML layer through clean service interfaces.
* The frontend communicates with the backend via REST APIs and WebSockets.
* Keep business logic out of UI components and API routes thin.

---

## Development Workflow

1. Fork or clone the repository.
2. Create a descriptive feature branch from `main`:
   ```bash
   git checkout -b feature/my-descriptive-feature
   ```
3. Set up the development environment using `.env.example`:
   ```bash
   cp .env.example .env
   ```
4. Follow the commit message conventions (Conventional Commits):
   * `feat: add landmark extraction pipeline`
   * `fix: handle websocket reconnection timeout`
   * `docs: update system overview documentation`
   * `chore: update dependencies`
5. Run linting and test suites before committing:
   ```bash
   make lint
   make test
   ```
6. Open a pull request targeting `main` with a clear description of the changes and testing performed.

---

## Code Quality Standards

* **Python (Backend & ML)**:
  * Formatted with Black.
  * Linted with Ruff.
  * Type-checked where applicable.
  * Tested with pytest.

* **TypeScript / React (Frontend)**:
  * Strict mode enabled in TypeScript.
  * Formatted with Prettier.
  * Linted with ESLint.

---

## Security and Safe Execution

* Never commit `.env` files, credentials, or production secrets.
* Gesture actions executed on the host operating system must adhere to fail-safe limits, confidence thresholds, and explicit user enablement.
