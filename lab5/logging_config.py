import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = '[%(asctime)s] %(levelname)-8s | %(name)-15s | %(filename)s:%(lineno)d | %(message)s'
DATE_FORMAT = '%d.%m.%Y %H:%M:%S'

formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

# Console output: INFO, WARNING, ERROR
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Rotating file by size: only WARNING and ERROR (10 MB, 5 backups)
size_rotating_handler = RotatingFileHandler(
    str(LOG_DIR / 'app_warnings.log'),
    maxBytes=10 * 1024 * 1024,
    backupCount=5,
    encoding='utf-8'
)
size_rotating_handler.setLevel(logging.WARNING)
size_rotating_handler.setFormatter(formatter)

# Timed rotating file: INFO and above, rotates at midnight, keeps 7 days
time_rotating_handler = TimedRotatingFileHandler(
    str(LOG_DIR / 'app_main.log'),
    when='midnight',
    interval=1,
    backupCount=7,
    encoding='utf-8'
)
time_rotating_handler.setLevel(logging.INFO)
time_rotating_handler.setFormatter(formatter)
time_rotating_handler.suffix = '%Y-%m-%d'


def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers.clear()

    root_logger.addHandler(console_handler)
    root_logger.addHandler(size_rotating_handler)
    root_logger.addHandler(time_rotating_handler)

    root_logger.info("=== Logging configuration loaded successfully ===")
