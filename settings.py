from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    login: Optional[str]
    password: Optional[str]
    message: Optional[str]
    phone: Optional[str]
    debug: bool = False
    secret_key: str = 'change_me'

    class Config:
        env_file = '.env'


settings = Settings()
