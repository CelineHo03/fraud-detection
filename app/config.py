from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0

    ingest_stream: str = 'fraud:ingest'
    result_stream: str = 'fraud:results'

    ingest_group: str = 'fraud-processors'

    class Config:
        env_file = '.venv'

settings = Settings()