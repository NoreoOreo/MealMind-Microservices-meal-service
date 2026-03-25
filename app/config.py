from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(
        default="postgresql+asyncpg://meal:meal@postgres:5432/meal",
        description="SQLAlchemy database URL",
    )
    reset_schema_on_start: bool = Field(default=False, description="Drop & recreate DB schema on startup (destructive)")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
