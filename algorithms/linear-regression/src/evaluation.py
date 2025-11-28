"""
Módulo de evaluación de modelos de regresión.

Implementa métricas, validación cruzada y análisis de residuos.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, learning_curve
from typing import Dict, Tuple, Any
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

plt.style.use('seaborn-v0_8-darkgrid')


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calcula métricas de regresión.
    
    Args:
        y_true: Valores reales
        y_pred: Valores predichos
    
    Returns:
        Diccionario con métricas
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    # Adjusted R²
    n = len(y_true)
    p = 1  # Número de predictores (simplificado)
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1) if n > p + 1 else r2
    
    metrics = {
        'mae': float(mae),
        'mse': float(mse),
        'rmse': float(rmse),
        'r2': float(r2),
        'adjusted_r2': float(adj_r2)
    }
    
    return metrics


def evaluate_model(
    model: Any,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> Dict[str, Dict[str, float]]:
    """
    Evalúa modelo en train y test sets.
    
    Args:
        model: Modelo entrenado
        X_train, y_train: Datos de entrenamiento
        X_test, y_test: Datos de prueba
    
    Returns:
        Diccionario con métricas de train y test
    """
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    train_metrics = calculate_metrics(y_train, y_train_pred)
    test_metrics = calculate_metrics(y_test, y_test_pred)
    
    results = {
        'train': train_metrics,
        'test': test_metrics
    }
    
    logger.info(f"Train R²: {train_metrics['r2']:.4f}, Test R²: {test_metrics['r2']:.4f}")
    
    return results


def cross_validate_model(
    model: Any,
    X: pd.DataFrame,
    y: pd.Series,
    cv: int = 5
) -> Dict[str, Any]:
    """
    Realiza validación cruzada.
    
    Args:
        model: Modelo a evaluar
        X: Features
        y: Target
        cv: Número de folds
    
    Returns:
        Diccionario con resultados de CV
    """
    scores = cross_val_score(model, X, y, cv=cv, scoring='r2')
    
    cv_results = {
        'scores': scores.tolist(),
        'mean_score': float(scores.mean()),
        'std_score': float(scores.std()),
        'cv_folds': cv
    }
    
    logger.info(f"CV R² Score: {cv_results['mean_score']:.4f} (+/- {cv_results['std_score']:.4f})")
    
    return cv_results


def plot_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    title: str = "Predicciones vs Valores Reales",
    save_path: str = None
):
    """Visualiza predicciones vs valores reales."""
    plt.figure(figsize=(10, 6))
    plt.scatter(y_true, y_pred, alpha=0.5)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
    plt.xlabel('Valores Reales')
    plt.ylabel('Predicciones')
    plt.title(title)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Gráfico guardado en: {save_path}")
    plt.close()


def plot_residuals(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    save_path: str = None
):
    """Visualiza análisis de residuos."""
    residuals = y_true - y_pred
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Residuos vs Predicciones
    axes[0, 0].scatter(y_pred, residuals, alpha=0.5)
    axes[0, 0].axhline(y=0, color='r', linestyle='--')
    axes[0, 0].set_xlabel('Predicciones')
    axes[0, 0].set_ylabel('Residuos')
    axes[0, 0].set_title('Residuos vs Predicciones')
    
    # Histograma de residuos
    axes[0, 1].hist(residuals, bins=50, edgecolor='black')
    axes[0, 1].set_xlabel('Residuos')
    axes[0, 1].set_ylabel('Frecuencia')
    axes[0, 1].set_title('Distribución de Residuos')
    
    # Q-Q Plot
    from scipy import stats
    stats.probplot(residuals, dist="norm", plot=axes[1, 0])
    axes[1, 0].set_title('Q-Q Plot')
    
    # Residuos vs Índice
    axes[1, 1].scatter(range(len(residuals)), residuals, alpha=0.5)
    axes[1, 1].axhline(y=0, color='r', linestyle='--')
    axes[1, 1].set_xlabel('Índice')
    axes[1, 1].set_ylabel('Residuos')
    axes[1, 1].set_title('Residuos vs Orden')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Análisis de residuos guardado en: {save_path}")
    plt.close()


def save_metrics(metrics: Dict, filepath: str):
    """Guarda métricas en formato JSON."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(metrics, f, indent=4)
    logger.info(f"Métricas guardadas en: {filepath}")


def compare_models(results: Dict[str, Dict]) -> pd.DataFrame:
    """
    Compara resultados de múltiples modelos.
    
    Args:
        results: Diccionario {nombre_modelo: métricas}
    
    Returns:
        DataFrame comparativo
    """
    comparison_data = []
    
    for model_name, metrics in results.items():
        row = {
            'Model': model_name,
            'Train R²': metrics['train']['r2'],
            'Test R²': metrics['test']['r2'],
            'Train RMSE': metrics['train']['rmse'],
            'Test RMSE': metrics['test']['rmse'],
            'Train MAE': metrics['train']['mae'],
            'Test MAE': metrics['test']['mae']
        }
        comparison_data.append(row)
    
    df_comparison = pd.DataFrame(comparison_data)
    df_comparison = df_comparison.sort_values('Test R²', ascending=False)
    
    return df_comparison
