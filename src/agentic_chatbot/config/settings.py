"""Application settings using Pydantic BaseSettings."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    google_api_key: str
    gemini_model: str = "gemini-2.0-flash"
    llm_model: str | None = None
    pushover_token: str | None = None
    pushover_user: str | None = None
    assets_dir: Path = Path("assets")
    request_timeout_secs: float = 10.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def model(self) -> str:
        """Get the LLM model from LLM_MODEL env var or fallback to gemini_model."""
        return self.llm_model or self.gemini_model
