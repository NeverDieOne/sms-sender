from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    login: Optional[str]
    password: Optional[str]
    message: Optional[str]
    phone: Optional[str]
    redis_url: str

    class Config:
        env_file = '.env'


settings = Settings()
