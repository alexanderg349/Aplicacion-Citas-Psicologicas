from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    app_name: str = "Consultorio Psicologico API"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = Field("change-this-development-secret-before-production-12345", min_length=32)
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"
    database_url: str = "sqlite:///./data/consultorio_psicologia.db"
    cors_origins: str = "http://localhost:5173"
    seed_demo_data: bool = True
    rate_limit_window_seconds: int = 60
    rate_limit_max_attempts: int = 8
    lock_minutes_after_failures: int = 15
    max_login_failures: int = 5

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
