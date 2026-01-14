from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration for PromptScope, powered by Pydantic.

    Values are loaded from environment variables with sensible defaults.
    """
    ENABLED: bool = True
    STORAGE_BACKEND: str = "sqlite"
    REMOTE_URL: Optional[str] = None
    API_KEY: Optional[str] = None
    DB_PATH: str = "promptscope.db"

    # --- Telemetry Settings ---
    TELEMETRY_ENABLED: bool = True
    TELEMETRY_LOG_DIR: str = "telemetry_logs"
    TELEMETRY_BATCH_SIZE: int = 50
    TELEMETRY_FLUSH_INTERVAL: float = 5.0

    class Config:
        # All environment variables will be prefixed with `PROMPTSCOPE_`
        # e.g. `PROMPTSCOPE_ENABLED`
        env_prefix = "PROMPTSCOPE_"
        case_sensitive = False


# Instantiate the config so it can be imported and used elsewhere.
# e.g. `from promptscope.config import settings`
settings = Settings()