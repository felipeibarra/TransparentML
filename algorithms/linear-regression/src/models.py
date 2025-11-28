"""
Módulo de modelos de regresión lineal.

Implementa diferentes tipos de regresión: simple, múltiple, regularizada y polinomial.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from typing import Dict, Any, Optional
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LinearRegressionModel:
    """Modelo de Regresión Lineal simple y múltiple."""
    
    def __init__(self, fit_intercept: bool = True):
        self.model = LinearRegression(fit_intercept=fit_intercept)
        self.is_fitted = False
    
    def fit(self, X: pd.DataFrame, y: pd.Series):
        """Entrena el modelo."""
        self.model.fit(X, y)
        self.is_fitted = True
        logger.info(f"Modelo entrenado. Coeficientes: {len(self.model.coef_)}")
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Realiza predicciones."""
        if not self.is_fitted:
            raise ValueError("Modelo no entrenado. Llama a fit() primero.")
        return self.model.predict(X)
    
    def get_coefficients(self) -> Dict[str, float]:
        """Obtiene coeficientes del modelo."""
        return {
            'intercept': self.model.intercept_,
            'coefficients': self.model.coef_.tolist()
        }


class RidgeRegressionModel:
    """Modelo de Regresión Ridge (L2 regularization)."""
    
    def __init__(self, alpha: float = 1.0):
        self.model = Ridge(alpha=alpha)
        self.is_fitted = False
    
    def fit(self, X: pd.DataFrame, y: pd.Series):
        """Entrena el modelo."""
        self.model.fit(X, y)
        self.is_fitted = True
        logger.info(f"Ridge entrenado. Alpha: {self.model.alpha}")
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Realiza predicciones."""
        return self.model.predict(X)


class LassoRegressionModel:
    """Modelo de Regresión Lasso (L1 regularization)."""
    
    def __init__(self, alpha: float = 1.0):
        self.model = Lasso(alpha=alpha, max_iter=10000)
        self.is_fitted = False
    
    def fit(self, X: pd.DataFrame, y: pd.Series):
        """Entrena el modelo."""
        self.model.fit(X, y)
        self.is_fitted = True
        logger.info(f"Lasso entrenado. Features no-cero: {np.sum(self.model.coef_ != 0)}")
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Realiza predicciones."""
        return self.model.predict(X)


class ElasticNetModel:
    """Modelo de Regresión Elastic Net (L1 + L2 regularization)."""
    
    def __init__(self, alpha: float = 1.0, l1_ratio: float = 0.5):
        self.model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, max_iter=10000)
        self.is_fitted = False
    
    def fit(self, X: pd.DataFrame, y: pd.Series):
        """Entrena el modelo."""
        self.model.fit(X, y)
        self.is_fitted = True
        logger.info(f"ElasticNet entrenado. Alpha: {self.model.alpha}, L1 ratio: {self.model.l1_ratio}")
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Realiza predicciones."""
        return self.model.predict(X)


class PolynomialRegressionModel:
    """Modelo de Regresión Polinomial."""
    
    def __init__(self, degree: int = 2):
        self.degree = degree
        self.pipeline = Pipeline([
            ('poly_features', PolynomialFeatures(degree=degree, include_bias=False)),
            ('linear_regression', LinearRegression())
        ])
        self.is_fitted = False
    
    def fit(self, X: pd.DataFrame, y: pd.Series):
        """Entrena el modelo."""
        self.pipeline.fit(X, y)
        self.is_fitted = True
        logger.info(f"Regresión polinomial entrenada. Grado: {self.degree}")
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Realiza predicciones."""
        return self.pipeline.predict(X)


def save_model(model: Any, filepath: str) -> None:
    """Guarda modelo en disco."""
    joblib.dump(model, filepath)
    logger.info(f"Modelo guardado en: {filepath}")


def load_model(filepath: str) -> Any:
    """Carga modelo desde disco."""
    model = joblib.load(filepath)
    logger.info(f"Modelo cargado desde: {filepath}")
    return model
