from pydantic import BaseSettings, AnyUrl
from typing import Optional

class Settings(BaseSettings):
    BOT_TOKEN: str
    MODERATOR_ID: int = 884963545
    TARGET_CHANNEL: str = "@yallaisrael"
    WEBHOOK_SECRET: str = "supersecret"
    WEBHOOK_PATH: str = "/tg/webhook"
    BASE_URL: AnyUrl
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    DEFAULT_LANG: str = "ru"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
