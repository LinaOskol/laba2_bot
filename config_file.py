from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    token_api: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

config = Settings()