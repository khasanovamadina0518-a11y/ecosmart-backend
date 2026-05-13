"""
Application configuration — loads values from .env
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# .env fayl yo'li
ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"


class Settings(BaseSettings):
    """Global application settings backed by environment variables."""

    # ── App ───────────────────────────────────────
    APP_NAME: str = "EcoSmart Waste"
    DEBUG: bool = False
    PORT: int = 7860

    # ── Database ──────────────────────────────────
    DATABASE_URL: str

    # ── JWT / Auth ────────────────────────────────
    SECRET_KEY: str = "vaqtincha_juda_uzun_va_murakkab_shifr_123456789"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Bu qator eng muhim!
    )


settings = Settings()