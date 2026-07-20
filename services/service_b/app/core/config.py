from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

SERVICE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    service_name: str = "service-b"
    environment: str = "local"
    database_url: str | None = None
    database_pool_size: int = 5
    database_max_overflow: int = 10
    database_pool_timeout: int = 30

    model_config = SettingsConfigDict(
        env_file=SERVICE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()
