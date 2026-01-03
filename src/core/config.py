from typing import Final

from dotenv import load_dotenv
from pydantic import AnyUrl
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    IS_DEV_ENV: bool

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(levelname)s: %(asctime)s.%(msecs)03d  %(name)s: %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    DATABASE_URL: AnyUrl
    DEBUG_QUERIES: bool = False


settings: Final[Settings] = Settings()  # type: ignore[call-arg]
