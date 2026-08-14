from __future__ import annotations

from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = Field(default="AI Essay Detector")
    app_env: str = Field(default="development")
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    model_path: str = Field(default="./models")
    log_level: str = Field(default="INFO")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
