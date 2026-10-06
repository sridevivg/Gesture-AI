"""Machine Learning subsystem configuration."""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class MLSettings(BaseSettings):
    """Configuration for ML training and inference."""

    ML_SERVICE_HOST: str = "0.0.0.0"
    ML_SERVICE_PORT: int = 8001
    MODELS_DIR: str = os.path.join(os.path.dirname(__file__), "..", "models")
    DATASETS_DIR: str = os.path.join(os.path.dirname(__file__), "..", "datasets")
    CONFIDENCE_THRESHOLD: float = 0.80
    DETECTION_FPS: int = 30
    NUM_LANDMARKS: int = 21
    TEMPORAL_WINDOW_SIZE: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


ml_settings = MLSettings()
