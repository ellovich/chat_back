from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "FATAL"]

    # postgres
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # postgres test db
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str
    
    @property
    def TEST_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    # celery
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    # redis
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    # sentry
    SENTRY_DSN: str

    # cookies
    SECRET_KEY: str
    ALGORITHM: str


settings = Settings()

print(settings.DATABASE_URL)