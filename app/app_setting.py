import oracledb
from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    user:str
    password:str
    dsn:str

 #To see the secret_key type in terminal => python -c "import secrets; print(secrets.token_hex(32))"
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRATION_MINUTES:int

    model_config = SettingsConfigDict(
    env_file=BASE_DIR / ".env"
)


@lru_cache
def get_settings():
    return Settings()
