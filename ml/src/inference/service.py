"""Standalone ML inference microservice."""

from typing import Any, Dict, List
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ml.src.config import ml_settings
from ml.src.inference.pipeline import GestureInferencePipeline

app = FastAPI(
    title="Gesture-AI ML Service",
    version="0.1.0",
    description="Dedicated inference microservice for hand landmark gesture classification.",
)

pipeline = GestureInferencePipeline()


class PredictRequest(BaseModel):
    landmarks: List[Dict[str, float]]


class PredictResponse(BaseModel):
    gesture_name: str
    confidence: float
    category: str


@app.get("/health")
def health():
    return {"status": "healthy", "service": "gesture_ml"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    result = pipeline.process_landmarks(request.landmarks)
    return PredictResponse(
        gesture_name=result.gesture_name,
        confidence=result.confidence,
        category=result.category,
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=ml_settings.ML_SERVICE_HOST,
        port=ml_settings.ML_SERVICE_PORT,
    )
