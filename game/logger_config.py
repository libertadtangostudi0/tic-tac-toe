from loguru import logger
import os
import sys

logger.remove()

BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "logs"))

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = (
    "<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# console
logger.add(
    sys.stderr,
    level="DEBUG",
    format=LOG_FORMAT,
)

# file
logger.add(
    os.path.join(LOG_DIR, "game.log"),
    level="DEBUG",
    format=LOG_FORMAT,
    rotation="500 KB",
    retention=5,
)

__all__ = ["logger"]
