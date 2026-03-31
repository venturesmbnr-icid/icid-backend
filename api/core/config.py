# app/core/config.py
# from pydantic import BaseSettings
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://mehdis@localhost:5432/icid"
    TEST_DATABASE_URL: str = "postgresql+asyncpg://mehdis@localhost:5432/icid_test"

    class Config:
        env_file = ".env.test" if os.getenv("PYTEST_CURRENT_TEST") else ".env"



settings = Settings()

DATABASE_URL = settings.DATABASE_URL
TEST_DATABASE_URL = settings.TEST_DATABASE_URL
