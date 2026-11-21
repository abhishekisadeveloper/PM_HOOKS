from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PM Hooks API"
    app_version: str = "0.1.0"
    debug: bool = False

    db_name: str = Field(validation_alias="POSTGRES_DB")
    db_user: str = Field(validation_alias="POSTGRES_USER")
    db_password: str = Field(validation_alias="POSTGRES_PASSWORD")

    db_host: str = Field(
        default="localhost",
        validation_alias="PM_HOOK_DB_HOST",
    )
    db_port: int = Field(
        default=5432,
        validation_alias="PM_HOOK_DB_PORT",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="PM_HOOK_",
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()