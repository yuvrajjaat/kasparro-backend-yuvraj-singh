from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/postgres"
    
    COINGECKO_BASE_URL: str = "https://api.coingecko.com/api/v3"
    COINPAPRIKA_BASE_URL: str = "https://api.coinpaprika.com/v1"

settings = Settings()
