from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    app_secret_key: str = "change-me"

    database_url: str = (
        "postgresql+psycopg://facturacion:facturacion@localhost:5432/facturacion"
    )

    sifen_ambiente: str = "test"
    sifen_cert_path: Path = Path("./secrets/certificado.pfx")
    sifen_cert_password: str = ""
    sifen_csc: str = ""
    sifen_csc_id: str = ""

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = ""

    var_dir: Path = Path("./var")


@lru_cache
def get_settings() -> Settings:
    return Settings()
