"""
PrepForge — Application Configuration

Loads all settings from environment variables.
In local development, values are read from backend/.env (never committed).
See backend/.env.example for the list of required variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration model.

    pydantic-settings automatically reads values from:
    1. Environment variables (highest priority)
    2. The .env file specified in model_config (if present)
    3. Field default values (lowest priority)

    All fields are typed and validated on startup.
    Missing required fields (no default, no env value) raise a
    clear ValidationError immediately — not silently at runtime.
    """

    # ----------------------------------------------------------
    # Application
    # ----------------------------------------------------------
    ENVIRONMENT: str = "development"
    API_PREFIX: str = "/api/v1"

    # ----------------------------------------------------------
    # MongoDB
    # ----------------------------------------------------------
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "prepforge_dev"

    # ----------------------------------------------------------
    # CORS
    # Comma-separated list of allowed origins for the frontend.
    # Example: "http://localhost:5173,http://localhost:3000"
    # Kept here so CORS behaviour is config-driven rather than
    # hardcoded. Unused until the frontend is scaffolded.
    # ----------------------------------------------------------
    CORS_ORIGINS: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        # Load from backend/.env when running from the backend/ directory.
        # If the file does not exist, env vars still work — no error raised.
        env_file=".env",
        env_file_encoding="utf-8",
        # Do not crash if extra env vars are present in the .env file.
        extra="ignore",
    )


# Single shared instance — imported by the rest of the application.
settings = Settings()
