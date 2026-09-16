from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ALGOMIND AI"
    database_url: str = "sqlite:///./algomind.db"
    jwt_secret: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    sandbox_timeout_seconds: float = 5.0
    sandbox_memory_limit_mb: int = 256

    class Config:
        env_file = ".env"


settings = Settings()
