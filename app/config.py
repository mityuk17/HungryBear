from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_PORT: int
    DB_PASSWORD: str
    DB_USER: str
    DB_NAME: str
    DB_HOST: str
    BOT_TOKEN: str
    BOT_USERNAME: str | None = None
    REDIS_HOST: str
    REDIS_USER: str
    REDIS_PASSWORD: str
    REDIS_USER_PASSWORD: str
    REDIS_PORT: int
    YANDEX_API_TOKEN: str
    YANDEX_CATALOG_ID: str
    YANDEX_GPT_MODEL: str

    class Config:
        env_file = "./.env"


settings = Settings()

