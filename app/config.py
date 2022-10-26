"""Configuration for the app."""
# flake8: noqa: E501
# Dependencies

from functools import lru_cache
from os import environ
from typing import Optional

import structlog
from pydantic import BaseSettings, Field

log = structlog.get_logger()

###### SETTINGS #######

## Note: Pydantic reads in .env files without explicit need to call load_dotenv()
class Settings(BaseSettings):
    app_env: Optional[str] = Field("LOCAL", title="App Environment")
    app_version: Optional[str] = Field(None, title="App Version")
    app_port: Optional[int] = Field(
        8000,
        title="Application Port",
        description="Port to run the application on, defaults to 8000",
    )
    access_key_id: Optional[str] = Field(None, title="AWS Access Key")
    region: Optional[str] = Field(None, title="AWS Region")
    secret_access_key: Optional[str] = Field(None, title="AWS Secret Key")
    hugging_face_api_key: Optional[str] = Field(title="Huggingface API Key")
    
    class Config:
        env_file = "app/.local.env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings(env=None):
    if not env:
        env = environ.get("ENV")
    elif env == "INTEGRATION":
        return Settings(app_env="INTEGRATION", _env_file="app/.integration.env")
    else:
        return Settings()

settings = get_settings()