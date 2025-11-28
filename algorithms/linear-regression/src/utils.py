"""
Módulo de utilidades generales.
"""

import time
import logging
from functools import wraps
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def timer(func):
    """Decorador para medir tiempo de ejecución."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"{func.__name__} ejecutado en {end - start:.2f}s")
        return result
    return wrapper


def ensure_dir(path: str):
    """Crea directorio si no existe."""
    Path(path).mkdir(parents=True, exist_ok=True)
