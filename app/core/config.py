from pydantic_settings import BaseSettings
from pydantic import computed_field
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "admin")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "db")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")


settings = Settings()
