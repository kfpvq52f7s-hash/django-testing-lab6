import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

# 1. Консольный хендлер - только INFO и выше
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 2. Файловый хендлер с ротацией по размеру - только WARNING и ERROR
rotating_handler = RotatingFileHandler(
    str(LOG_DIR / 'rotating.log'),
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding='utf-8'
)
rotating_handler.setLevel(logging.WARNING)  # ← ТОЛЬКО WARNING и ERROR
rotating_handler.setFormatter(formatter)

# 3. Файловый хендлер с ротацией по времени - только INFO и выше
timed_handler = TimedRotatingFileHandler(
    str(LOG_DIR / 'timed.log'),
    when='midnight',
    interval=1,
    backupCount=7,
    encoding='utf-8'
)
timed_handler.setLevel(logging.INFO)  # ← INFO, WARNING, ERROR (без DEBUG)
timed_handler.setFormatter(formatter)
timed_handler.suffix = '%Y-%m-%d'


def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers.clear()

    root_logger.addHandler(console_handler)
    root_logger.addHandler(rotating_handler)
    root_logger.addHandler(timed_handler)

    root_logger.info("=== Logging system initialized ===")