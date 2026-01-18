from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application configuration via Environment Variables.
    """
    PROJECT_NAME: str = "Infinite Echoes"
    VERSION: str = "0.1.0"
    DEBUG_MODE: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://admin:password@localhost:5432/infinite_echoes"
    
    # AI / LLM
    OPENAI_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()