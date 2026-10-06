# Architecture Decision Records (ADRs)

## Purpose

This directory contains Architecture Decision Records (ADRs) for the Gesture-AI platform. Each record documents a significant architectural or technical decision, its context, alternatives considered, and consequences.

---

## Decision Record Format

New decision records should follow this standardized template:

* **Title**: Descriptive name of the decision (e.g. `adr-monorepo-structure.md`, `adr-websocket-streaming.md`).
* **Status**: Proposed | Accepted | Deprecated | Superseded.
* **Context**: The background, problem statement, and forces influencing the decision.
* **Decision**: The specific technical choice and implementation strategy.
* **Consequences**: Positive outcomes, trade-offs, and downstream impacts.

---

## Log of Architectural Decisions

| Decision Reference | Title | Status | Date |
| :--- | :--- | :--- | :--- |
| ADR-Monorepo-Architecture | Monorepo Structure with Strict Subsystem Boundaries | Accepted | 2026-10-06 |
| ADR-Dual-Interface | REST API for State and WebSockets for Telemetry | Accepted | 2026-10-06 |
| ADR-Independent-ML | Separation of Computer Vision and ML from HTTP Runtime | Accepted | 2026-10-06 |
| ADR-Action-Safety | Failsafe Guardrails and Cooldown Limits for OS Automation | Accepted | 2026-10-06 |
