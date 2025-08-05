import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from pydantic_settings import BaseSettings


class LoggingSettings(BaseSettings):
    level: str = "INFO"
    fmt: str = "%(asctime)s %(levelname)s [%(filename)s] %(message)s"
    # 2025-08-05 18:47:31 INFO [main.py] Hello
    # asctime = current time during logging
    # levelname = log level [DEBUG=10, INFO=20,  WARNING=30, ERROR=40 OR CRITICAL=50]
    # filename = the python where the log is generated from
    # message = the log message
    datefmt: str = "%Y-%m-%d %H:%M:%S"
    # ISO FORMAT "2015-02-01 12:35:03" # DEU DATE FORMAT %d.%m.%Y %H:%M:%S"
    log_file: str = "app.log"
    max_bytes: int = 1_000_000
    backup_count: int = 3

    class Config:
        env_prefix = "LOG_"
        env_file = Path(__file__).parent.parent.parent / ".env"
        case_sensitive = (False,)
        extra = "allow"

    def configure_logger(self, name: str = None) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(self.level)

        formatter = logging.Formatter(fmt=self.fmt, datefmt=self.datefmt)
        # logger.info(Hello) #2015-02-01 12:35:03, main.py
        # [2015-02-01 12:35:03][INFO][main.py]: Hello

        # setting logger for console/Terminal
        ch = logging.StreamHandler()
        ch.setLevel(self.level)
        ch.setFormatter(formatter)

        # setting logger for file
        fh = RotatingFileHandler(
            filename=self.log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
        )

        fh.setLevel(self.level)
        fh.setFormatter(formatter)

        logger.handlers.clear()

        logger.addHandler(ch)
        logger.addHandler(fh)

        return logger


log_cfg = LoggingSettings()
