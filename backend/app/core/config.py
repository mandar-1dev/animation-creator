"""
Central app configuration.
Reads GEMINI_API_KEY from environment (.env file or real env var).
If no key is set, the app runs in MOCK mode: sketch analysis still works
end-to-end using rule-based fallbacks instead of Gemini, so the whole
pipeline is testable before you add your key.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "AI Animation Creator"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    max_upload_mb: int = 8
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"

    @property
    def mock_mode(self) -> bool:
        return not bool(self.gemini_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
