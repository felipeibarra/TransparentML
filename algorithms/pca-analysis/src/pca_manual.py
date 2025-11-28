"""
Implementación manual de PCA (Principal Component Analysis)
Calcula autovalores y autovectores de la matriz de covarianza sin usar sklearn.PCA
"""

import numpy as np
from typing import Tuple, Optional


class PCAManual:
    """
    Implementación manual de PCA mediante cálculo de autovalores y autovectores
    de la matriz de covarianza.
    """
    
    def __init__(self, n_components: int = 2):
        """
        Args:
            n_components: Número de componentes principales a retener
        """
        self.n_components = n_components
        self.components_ = None
        self.explained_variance_ = None
        self.explained_variance_ratio_ = None
        self.mean_ = None
        self.eigenvalues_ = None
        self.eigenvectors_ = None
        
    def fit(self, X: np.ndarray) -> 'PCAManual':
        """
        Ajusta el modelo PCA a los datos.
        
        Args:
            X: Matriz de datos (n_samples, n_features)
            
        Returns:
            self
        """
        # 1. Centrar los datos (restar la media)
        self.mean_ = np.mean(X, axis=0)
        X_centered = X - self.mean_
        
        # 2. Calcular la matriz de covarianza
        # Cov(X) = (1/n) * X^T * X
        n_samples = X_centered.shape[0]
        cov_matrix = (X_centered.T @ X_centered) / (n_samples - 1)
        
        # 3. Calcular autovalores y autovectores
        # Los autovectores son las direcciones principales (componentes)
        # Los autovalores indican la varianza en cada dirección
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        
        # 4. Ordenar por autovalores descendentes
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # 5. Seleccionar los primeros n_components
        self.eigenvalues_ = eigenvalues
        self.eigenvectors_ = eigenvectors
        self.components_ = eigenvectors[:, :self.n_components].T
        
        # 6. Calcular varianza explicada
        total_variance = np.sum(eigenvalues)
        self.explained_variance_ = eigenvalues[:self.n_components]
        self.explained_variance_ratio_ = self.explained_variance_ / total_variance
        
        return self
    
    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Transforma los datos al espacio de componentes principales.
        
        Args:
            X: Matriz de datos (n_samples, n_features)
            
        Returns:
            X_transformed: Datos transformados (n_samples, n_components)
        """
        if self.components_ is None:
            raise ValueError("Debe llamar a fit() antes de transform()")
        
        # Centrar los datos
        X_centered = X - self.mean_
        
        # Proyectar en el espacio de componentes principales
        # X_transformed = X_centered * components^T
        X_transformed = X_centered @ self.components_.T
        
        return X_transformed
    
    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """
        Ajusta el modelo y transforma los datos en una sola operación.
        
        Args:
            X: Matriz de datos (n_samples, n_features)
            
        Returns:
            X_transformed: Datos transformados
        """
        self.fit(X)
        return self.transform(X)
    
    def inverse_transform(self, X_transformed: np.ndarray) -> np.ndarray:
        """
        Reconstruye los datos originales desde el espacio PCA.
        
        Args:
            X_transformed: Datos en espacio PCA (n_samples, n_components)
            
        Returns:
            X_reconstructed: Datos reconstruidos (n_samples, n_features)
        """
        if self.components_ is None:
            raise ValueError("Debe llamar a fit() antes de inverse_transform()")
        
        # Proyectar de vuelta al espacio original
        X_reconstructed = X_transformed @ self.components_ + self.mean_
        
        return X_reconstructed
    
    def get_covariance_matrix(self, X: np.ndarray) -> np.ndarray:
        """
        Calcula y retorna la matriz de covarianza de los datos.
        
        Args:
            X: Matriz de datos (n_samples, n_features)
            
        Returns:
            Matriz de covarianza
        """
        X_centered = X - np.mean(X, axis=0)
        n_samples = X_centered.shape[0]
        cov_matrix = (X_centered.T @ X_centered) / (n_samples - 1)
        return cov_matrix
    
    def get_cumulative_variance_ratio(self) -> np.ndarray:
        """
        Retorna la varianza acumulada explicada.
        
        Returns:
            Array con varianza acumulada
        """
        if self.explained_variance_ratio_ is None:
            raise ValueError("Debe llamar a fit() primero")
        
        return np.cumsum(self.explained_variance_ratio_)
    
    def get_loadings(self) -> np.ndarray:
        """
        Retorna los loadings (correlaciones entre variables y componentes).
        
        Returns:
            Matriz de loadings
        """
        if self.components_ is None:
            raise ValueError("Debe llamar a fit() primero")
        
        # Loadings = eigenvectors * sqrt(eigenvalues)
        loadings = self.components_.T * np.sqrt(self.explained_variance_)
        return loadings
