from typing import Set
from typing import Optional, Dict, Any
from pydantic import AnyUrl, BaseSettings, SecretStr, AnyHttpUrl, PostgresDsn, validator
import logging

log = logging.getLogger(__name__)

class Settings(BaseSettings):
    PROJECT_TITLE: str
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl

    # Mode
    DEBUG: bool = False

    # Security
    SECRET_KEY: SecretStr
    ALLOWED_HOSTS: Set[str]
    HTTPS_REDIRECT: bool = True
    BACKEND_CORS_ORIGINS: Set[str]

    DATABASE_URL: str

    # POSTGRES_SERVER: str
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str
    # DATABASE_URL: Optional[PostgresDsn] = None

    # @validator("DATABASE_URL", pre=True)
    # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         scheme="postgres",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_SERVER"),
    #         path=f"/{values.get('POSTGRES_DB') or ''}",
    #     )

    # Caching
    REDIS_URL: AnyUrl

    # Tortoise
    TORTOISE_MODEL_MODULES: Set[str] = {
        "app.models.features",
        "app.models.guests",
        "app.models.presenters",
    }

    class Config:
        case_sensitive = True

settings = Settings()
