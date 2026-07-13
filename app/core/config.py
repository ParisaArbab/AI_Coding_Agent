from functools import lru_cache
from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    app_name: str = "AI Coding Agent"
    app_env: str = "development"
    log_level: str = "INFO"
    llm_provider: Literal["mock", "openai", "anthropic"] = "mock"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-sonnet-4-5"
    github_token: str | None = None
    workspace_root: Path = Path("./workspace")
    max_file_bytes: int = 200_000
    allow_pr_creation: bool = False

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.workspace_root.mkdir(parents=True, exist_ok=True)
    return settings
