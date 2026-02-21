from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

    ENVIRONMENT: str = "development"

    APP_NAME: str = "Arcana Vault API 2026"
    APP_VERSION: str = "2026"
    APP_PORT: int = 8000
    APP_ENABLE_DOCS: bool = False

    API_PREFIX: str = "/api"
    API_ALLOW_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    DB_HOST: str = ""
    DB_PORT: str = "5432"
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""
    DB_SCHEMA: str = "public"

    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    SUPABASE_BUCKET_NAME: str = ""

    JWT_PRIVATE_KEY: str = ""
    JWT_PUBLIC_KEY: str = ""
    JWT_ALGORITHM: str = "RS256"

    KEY_EXPIRATION_MINUTES: int = 15

    TELEGRAM_BOT_TOKEN: str = ""


settings = Settings()
