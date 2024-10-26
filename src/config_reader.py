from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    db_host: SecretStr
    db_port: int
    db_name: SecretStr
    db_user: SecretStr
    db_pass: SecretStr
    
    model_config = SettingsConfigDict(env_file='../.env')

config = Settings()
