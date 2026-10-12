from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Sentinel API"
    app_env: str = "development"
    debug: bool = True

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""

    # Supabase PostgreSQL
    database_url: str = ""

    # Gemini
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"

    # Google Maps
    google_maps_api_key: str = ""

    # Frontend
    cors_origins: str = "http://localhost:5173"

    # Optional ML model
    model_path: str = "model/sentinel.joblib"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
