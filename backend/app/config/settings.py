from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_version: str
    app_env: str

    api_host: str
    api_port: int

    ollama_host: str

    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "text"          # text | json
    enable_console_logging: bool = True
    enable_file_logging: bool = False
    log_file: str = "logs/opsmind.log"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
