# Gesture-AI API Documentation

## Overview

The Gesture-AI backend exposes two primary communication interfaces:
1. **RESTful HTTP API**: Handles resource management, user preferences, gesture action mappings, system configuration, and analytics retrieval.
2. **WebSocket Interface**: Handles real-time streaming of video frames, hand landmark vectors, gesture recognition events, and execution status.

---

## Base URLs

* Local Development REST API: `http://localhost:8000/api/v1`
* Local Development WebSocket: `ws://localhost:8000/api/v1/ws/gesture-stream`
* Interactive API Documentation (Swagger / OpenAPI): `http://localhost:8000/docs`
* Alternative Documentation (ReDoc): `http://localhost:8000/redoc`

---

## Core Endpoint Specifications

### Health & Diagnostics

* `GET /api/v1/health`
  * Returns system health, database status, and ML service connectivity.
  * Response:
    ```json
    {
      "status": "healthy",
      "timestamp": "2026-10-06T09:00:00Z",
      "version": "0.1.0",
      "services": {
        "database": "connected",
        "redis": "connected",
        "ml_engine": "available"
      }
    }
    ```

### Gesture Management

* `GET /api/v1/gestures`
  * Lists registered static and dynamic gestures supported by the recognition pipeline.
* `POST /api/v1/gestures`
  * Registers a new custom gesture definition with metadata.
* `GET /api/v1/gestures/{gesture_id}`
  * Retrieves details for a specific gesture.

### Action Mappings

* `GET /api/v1/actions/mappings`
  * Retrieves user-defined mappings between gesture triggers and operating system actions.
* `POST /api/v1/actions/mappings`
  * Creates or updates a gesture-to-action binding (e.g., `PINCH` -> `LEFT_CLICK`).
* `DELETE /api/v1/actions/mappings/{mapping_id}`
  * Removes an action binding.

### Real-Time WebSocket Streaming

* `WS /api/v1/ws/gesture-stream`
  * Bidirectional stream for real-time telemetry.
  * Inbound message format:
    ```json
    {
      "type": "frame_landmarks",
      "timestamp": 1728200000.123,
      "landmarks": [[0.5, 0.4, 0.0], ...]
    }
    ```
  * Outbound message format:
    ```json
    {
      "type": "gesture_detected",
      "gesture": "SWIPE_RIGHT",
      "confidence": 0.94,
      "action_triggered": "PRESENTATION_NEXT_SLIDE",
      "timestamp": 1728200000.150
    }
    ```
