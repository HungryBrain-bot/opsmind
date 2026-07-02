from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # -------------------------------------------------------
    # Application
    # -------------------------------------------------------
    app_name: str
    app_version: str
    app_env: str

    # -------------------------------------------------------
    # API
    # -------------------------------------------------------
    api_host: str
    api_port: int

    # -------------------------------------------------------
    # LLM
    # -------------------------------------------------------
    ollama_host: str

    # -------------------------------------------------------
    # Logging
    # -------------------------------------------------------
    log_level: str = "INFO"
    log_format: str = "text"
    enable_console_logging: bool = True
    enable_file_logging: bool = False
    log_file: Path = Path("logs/opsmind.log")

    # -------------------------------------------------------
    # Directories
    # -------------------------------------------------------
    data_dir: Path = Path("data")
    logs_dir: Path = Path("logs")
    models_dir: Path = Path("models")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # -------------------------------------------------------
    # Chunking
    # -------------------------------------------------------

    chunk_size: int = 1000
    chunk_overlap: int = 200


settings = Settings()
