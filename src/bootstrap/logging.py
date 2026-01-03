import logging

from core.config import Settings

RESET = "\033[0m"
COLORS = {
    "DEBUG": "\033[37m",  # gray
    "INFO": "\033[32m",  # green
    "WARNING": "\033[33m",  # yellow
    "ERROR": "\033[31m",  # red
    "CRITICAL": "\033[41m",  # red background
}


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        if levelname in COLORS:
            record.levelname = f"{COLORS[levelname]}{levelname}{RESET}"
        return super().format(record)


def setup_logging(settings: Settings) -> None:
    handler = logging.StreamHandler()
    formatter = ColorFormatter(settings.LOG_FORMAT, settings.LOG_DATE_FORMAT)
    handler.setFormatter(formatter)
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        handlers=[handler],
    )
