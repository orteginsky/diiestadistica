# core/logging_config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:  # Evitar duplicados
        logger.setLevel(logging.INFO)
        handler = RotatingFileHandler("logs/app.log", maxBytes=5_000_000, backupCount=3)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
