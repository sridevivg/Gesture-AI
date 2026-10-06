# Machine Learning Subsystem Documentation

## Overview

The `ml/` subsystem handles all computer vision processing, feature extraction from hand landmarks, and classification of both static hand poses and dynamic spatio-temporal gestures.

---

## Directory Organization

```
ml/
├── datasets/             # Directory for collected raw and processed landmark datasets
├── models/               # Serialized model weights, checkpoints, and scalers
├── src/
│   ├── vision/           # Video frame capture, OpenCV utilities, MediaPipe hand detection
│   ├── recognition/      # Static classifier and dynamic temporal sequence recognizer
│   ├── training/         # Dataset loaders, feature engineering, and model training routines
│   ├── inference/        # Low-latency inference pipeline and ML service wrapper
│   └── utils/            # Geometric calculations, normalization, and visual debug overlays
├── tests/                # Unit tests for ML components and geometric transforms
├── pyproject.toml        # ML specific configuration
├── requirements.txt      # Python dependencies for ML
└── README.md             # Subsystem guide
```

---

## Pipeline Architecture

1. **Frame Ingestion**: Video stream captured at 30 FPS using OpenCV or incoming client WebSocket frames.
2. **Hand Detection & Landmark Extraction**: MediaPipe Hands extracts 21 key points in 3D normalized coordinates $(x, y, z)$.
3. **Feature Preprocessing**:
   - Landmark origin translation to wrist point $(x_0, y_0, z_0)$.
   - Scale normalization by maximum distance across hand key points.
   - Rotational alignment for orientation invariance where applicable.
4. **Classification**:
   - **Static Gestures**: Multi-class classification using trained models (e.g., Random Forest, Multi-Layer Perceptron, or Support Vector Machines).
   - **Dynamic Gestures**: Sliding window temporal analysis over consecutive landmark frames using recurrent or temporal convolutional networks.
5. **Confidence Scoring & Intent Verification**:
   - Softmax probabilities are checked against configured confidence thresholds (default: 0.80).
   - Temporal smoothing (majority voting or EMA) filters out single-frame jitter.

---

## Supported Gesture Taxonomy (Target Specification)

| Gesture Name | Category | Primary Action Mapping |
| :--- | :--- | :--- |
| `OPEN_PALM` | Static | Stop / Pause / Disarm |
| `FIST` | Static | Hold / Drag |
| `POINTING` | Static | Cursor Track / Direct |
| `PINCH` | Static | Primary Click / Select |
| `VICTORY_PEACE` | Static | Toggle Application Mode |
| `THUMBS_UP` | Static | Confirm / Volume Up |
| `THUMBS_DOWN` | Static | Cancel / Volume Down |
| `SWIPE_LEFT` | Dynamic | Previous Slide / Previous Track |
| `SWIPE_RIGHT` | Dynamic | Next Slide / Next Track |
| `SWIPE_UP` | Dynamic | Page Up / Volume Increment |
| `SWIPE_DOWN` | Dynamic | Page Down / Volume Decrement |
