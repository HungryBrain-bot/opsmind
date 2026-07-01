from backend.app.config.settings import Settings, settings


def get_settings() -> Settings:
    """
    Return the application settings instance.
    """
    return settings
