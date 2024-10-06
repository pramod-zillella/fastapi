# Pydantic BseSettings class is moved to pydantic-settings class
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_username: str
    database_password: str
    database_name: str
    database_port: str
    secret_key: str
    access_token_expire_minutes: int
    algorithm: str

    class Config:
        env_file = ".env"

settings = Settings()