import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn


class Base(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)

    PROJ_ENV: str = Field(..., env="PROJ_ENV")  # type: ignore
    # Application
    DEBUG: bool
    TITLE: str = "TOKEN AUTH APP"
    GLOBAL_PREFIX_URL: str
    LOG_DIR: str = "logs"

    # CORS
    # TODO сделать мидлваре и корс

    # Celery
    # TODO если будет селери то добавить его

    # DataBase
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB_NUMBER: int

    # TODO ДОДЕЛАТЬ ВСЕ property
    @property
    def DATABASE_ASYNC_URL(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.DB_USER,
                password=self.DB_PASSWORD,
                host=self.DB_HOST,
                port=int(self.DB_PORT),  # Явное преобразование строки в число
                path=self.DB_NAME,
            )
        )

    # @property
    # def DATABASE_ASYNC_URL(self):
    #     return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def BASE_DIR(self) -> Path:
        return Path().resolve()


class Local(Base):
    """
    Attributes:
        GLOBAL_PREFIX_URL (str): Глобальный префикс перед всеми эндпоинтами. По умолчанию /api.
        DEBUG (bool): Режим дебага. По умолчанию True.
        REDIS_HOST (str): Хост redis. По умолчанию localhost.
        REDIS_PORT (int): Порт redis. По умолчанию 6379.
        REDIS_DB_NUMBER (int): Номер базы redis. По умолчанию 1.
        DB_HOST (str): Хост БД. По умолчанию localhost.
        DB_PORT (str): Порт БД. По умолчанию 5432.
    """  # noqa: E501

    GLOBAL_PREFIX_URL: str = "/api"
    DEBUG: bool = True

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB_NUMBER: int = 1

    model_config = SettingsConfigDict(env_file="local.env")


class Test(Base):
    GLOBAL_PREFIX_URL: str = "/api/test"
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file="test.env")


class Production(Base):
    GLOBAL_PREFIX_URL: str = "/api"
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file="prod.env")


config_map = {
    "local": Local,
    "test": Test,
    "prod": Production,
}

env_variable = os.environ.get("PROJ_ENV")

if env_variable is None:
    raise ValueError("Not found 'PROJ_ENV' enviroment variable")

env_variable = env_variable.lower()
if env_variable not in config_map:
    raise ValueError(
        f"Incorrect 'PROJ_ENV' enviroment variable, must be in {list(config_map.keys())}"
    )

try:
    settings: Base = config_map[env_variable]()
except ValueError as e:
    print(f"Error on validate configuration from *.env: {e}")
    raise
