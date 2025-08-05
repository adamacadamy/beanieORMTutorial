from app.core import log_cfg

# __name__ = main.py
logger = log_cfg.configure_logger(__name__)


def main() -> None:
    logger.info("Hello")


if __name__ == "__main__":
    main()
