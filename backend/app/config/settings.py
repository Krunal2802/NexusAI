from functools import lru_cache
from typing import Any, Literal

from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("*", mode="before")
    @classmethod
    def _empty_str_uses_default(cls, value: Any, info: ValidationInfo) -> Any:
        if value == "" and info.field_name != "database_url":
            return cls.model_fields[info.field_name].default
        return value

    # Application
    app_name: str = "NexusAI Backend API"
    app_env: Literal["development", "testing", "production"] = "development"

    # PostgreSQL
    database_url: str

    @field_validator("database_url")
    @classmethod
    def _database_url_required(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError(
                "DATABASE_URL must be provided via environment variables or .env"
            )
        return value.strip()

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    # OpenAI
    openai_api_key: str = ""

    # JWT
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    @property
    def qdrant_url(self) -> str:
        return f"http://{self.qdrant_host}:{self.qdrant_port}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
