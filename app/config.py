from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str
    log_level: str
    external_api_key: str
    server_name: str = "FastMCP Playground"
    model_config = ConfigDict(env_file=".env")  # tells pydantic to load from .env file

settings = Settings()
