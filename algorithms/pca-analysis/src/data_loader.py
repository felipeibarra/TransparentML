"""
Módulo para carga y preprocesamiento del dataset Iris
"""

import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from typing import Tuple


def load_iris_data() -> Tuple[np.ndarray, np.ndarray, list, list]:
    """
    Carga el dataset Iris desde sklearn.
    
    Returns:
        X: Features (n_samples, n_features)
        y: Labels (n_samples,)
        feature_names: Lista con nombres de features
        target_names: Lista con nombres de clases
    """
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    feature_names = iris.feature_names
    target_names = iris.target_names
    
    return X, y, feature_names, target_names


def standardize_data(X: np.ndarray) -> Tuple[np.ndarray, StandardScaler]:
    """
    Estandariza los datos para que tengan media 0 y varianza 1.
    Esto es fundamental antes de aplicar PCA.
    
    Args:
        X: Matriz de features
        
    Returns:
        X_scaled: Datos estandarizados
        scaler: Objeto StandardScaler ajustado
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, scaler


def create_dataframe(X: np.ndarray, y: np.ndarray, 
                     feature_names: list, target_names: list) -> pd.DataFrame:
    """
    Crea un DataFrame de pandas con los datos.
    
    Args:
        X: Features
        y: Labels
        feature_names: Nombres de features
        target_names: Nombres de clases
        
    Returns:
        DataFrame con los datos
    """
    df = pd.DataFrame(X, columns=feature_names)
    df['species'] = [target_names[i] for i in y]
    df['target'] = y
    
    return df


def get_data_statistics(X: np.ndarray, feature_names: list) -> pd.DataFrame:
    """
    Calcula estadísticas descriptivas de los datos.
    
    Args:
        X: Matriz de features
        feature_names: Nombres de features
        
    Returns:
        DataFrame con estadísticas
    """
    df = pd.DataFrame(X, columns=feature_names)
    stats = df.describe()
    
    return stats


def get_correlation_matrix(X: np.ndarray, feature_names: list) -> pd.DataFrame:
    """
    Calcula la matriz de correlación entre features.
    
    Args:
        X: Matriz de features
        feature_names: Nombres de features
        
    Returns:
        Matriz de correlación
    """
    df = pd.DataFrame(X, columns=feature_names)
    corr_matrix = df.corr()
    
    return corr_matrix
