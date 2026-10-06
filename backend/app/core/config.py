"""Application settings using Pydantic BaseSettings."""

from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Gesture-AI Configuration Settings."""

    # Project metadata
    PROJECT_NAME: str = "Gesture-AI"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Server configuration
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    SECRET_KEY: str = "gesture-ai-insecure-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # CORS origins
    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    DATABASE_URL: str = (
        "postgresql+asyncpg://gesture_admin:gesture_secure_password@localhost:5432/gesture_ai"
    )

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # ML Inference Service
    ML_SERVICE_URL: str = "http://localhost:8001"
    CONFIDENCE_THRESHOLD: float = 0.80

    # System Automation Safety Controls
    ENABLE_SYSTEM_ACTIONS: bool = False
    ACTION_EXECUTION_COOLDOWN_SECONDS: float = 1.0
    SAFETY_FAILSAFE_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
