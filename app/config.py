from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_title: str = 'Authentication microservice'
    app_name: str = 'auth'

    api_root_path: str = ''
    api_http_port: int = 8001
    api_db_url: str = 'mongodb://root:example@localhost:27017/'
    api_db_name: str = 'auth_service'

    # trace
    api_trace_url: str = 'http://localhost:4317'

    # auth settings
    # to get a viable secret run:
    # openssl rand -hex 32
    api_secret_key: str = 'SECRET_REPLACE_ME'
    api_jwt_algorithm: str = 'HS256'
    api_token_expire_min: int = 60

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
