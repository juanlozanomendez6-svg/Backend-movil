# logger.py
import logging
import os
from datetime import datetime

# Crear logger
logger = logging.getLogger("pos_logger")
logger.setLevel(logging.DEBUG if os.getenv("ENV") == "development" else logging.INFO)

# Formato de log
formatter = logging.Formatter("[%(levelname)s] %(asctime)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")

# Consola
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Funciones convenientes
def info(message):
    logger.info(message)

def error(message):
    logger.error(message)

def warn(message):
    logger.warning(message)

def debug(message):
    if os.getenv("ENV") == "development":
        logger.debug(message)

# Exportar
__all__ = ["info", "error", "warn", "debug"]
