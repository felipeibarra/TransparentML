"""
Módulo principal para la Tarea 1 de Regresión Lineal.

Este paquete contiene implementaciones de carga de datos, preprocesamiento,
modelado y evaluación para análisis de regresión lineal.
"""

__version__ = "1.0.0"
__author__ = "Felipe Ibarra"

from . import data_loader
from . import preprocessing
from . import models
from . import evaluation
from . import utils

__all__ = [
    "data_loader",
    "preprocessing",
    "models",
    "evaluation",
    "utils"
]
