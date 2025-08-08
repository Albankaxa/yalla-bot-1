from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: List[int] = Field(default_factory=list)

    POSTGRES_USER: str = "bot"
    POSTGRES_PASSWORD: str = "botpass"
    POSTGRES_DB: str = "botdb"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    ENV: str = "dev"

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
