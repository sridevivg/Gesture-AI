# Gesture-AI Machine Learning Subsystem

## Overview

The `ml/` subsystem houses the computer vision and machine learning logic for Gesture-AI. It manages hand detection, 21-point 3D landmark extraction, feature normalization, gesture classification (static and dynamic), model training routines, and low-latency inference pipelines.

---

## Directory Organization

```
ml/
├── datasets/             # Local dataset files (CSV, NumPy arrays) - gitignored
├── models/               # Trained model artifacts and checkpoint files - gitignored
├── src/
│   ├── vision/           # Video capture and MediaPipe hand detection
│   ├── recognition/      # Static classifier and dynamic gesture recognizer
│   ├── training/         # Dataset loading, feature extraction, and training jobs
│   ├── inference/        # Standalone inference service and pipeline wrappers
│   ├── utils/            # Geometric transforms and landmark normalization
│   └── config.py         # Subsystem settings
├── tests/                # Unit tests for ML components
├── pyproject.toml        # Ruff, Black, and pytest configurations
└── requirements.txt      # Python dependencies for ML
```

---

## Pipeline Workflow

1. **Vision Ingestion**: Frames received from local camera or incoming streaming packets.
2. **Landmark Extraction**: Detection of 21 hand landmarks $(x, y, z)$.
3. **Geometric Normalization**: Translation to wrist origin and scaling to normalize for varying hand-to-camera distances.
4. **Classification**:
   - Static pose recognition using trained classifiers.
   - Dynamic sequence recognition using temporal sliding windows.
5. **Inference Service**: Exposes low-latency HTTP/WebSocket endpoints consumed by the backend.

---

## Running the ML Inference Service

```bash
# Configure environment
cp .env.example .env

# Run standalone inference service
python -m src.inference.service
```

---

## Quality & Testing

```bash
# Run linters
ruff check .
black --check .

# Run tests
pytest tests/
```
