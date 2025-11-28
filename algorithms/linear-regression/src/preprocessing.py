"""
Módulo de preprocesamiento de datos.

Maneja limpieza, transformación, encoding y scaling de datos
para preparar el dataset para modelado de regresión.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from typing import Tuple, List, Optional, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """
    Clase para preprocesamiento completo de datos.
    
    Attributes:
        scaler: Objeto de scaling (StandardScaler o MinMaxScaler)
        encoders: Diccionario de encoders para variables categóricas
        numeric_features: Lista de features numéricas
        categorical_features: Lista de features categóricas
    """
    
    def __init__(self, scaling_method: str = 'standard'):
        """
        Inicializa el preprocesador.
        
        Args:
            scaling_method: Método de scaling ('standard' o 'minmax')
        """
        self.scaling_method = scaling_method
        self.scaler = StandardScaler() if scaling_method == 'standard' else MinMaxScaler()
        self.encoders: Dict[str, LabelEncoder] = {}
        self.numeric_features: List[str] = []
        self.categorical_features: List[str] = []
    
    def fit(self, X: pd.DataFrame) -> 'DataPreprocessor':
        """
        Ajusta el preprocesador a los datos.
        
        Args:
            X: DataFrame con features
        
        Returns:
            Self para encadenamiento
        """
        # Identificar tipos de features
        self.numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_features = X.select_dtypes(include=['object']).columns.tolist()
        
        logger.info(f"Features numéricas: {len(self.numeric_features)}")
        logger.info(f"Features categóricas: {len(self.categorical_features)}")
        
        # Ajustar scaler a features numéricas
        if self.numeric_features:
            self.scaler.fit(X[self.numeric_features])
        
        # Crear encoders para features categóricas
        for col in self.categorical_features:
            self.encoders[col] = LabelEncoder()
            self.encoders[col].fit(X[col].astype(str))
        
        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma los datos usando los parámetros ajustados.
        
        Args:
            X: DataFrame con features
        
        Returns:
            DataFrame transformado
        """
        X_transformed = X.copy()
        
        # Escalar features numéricas
        if self.numeric_features:
            X_transformed[self.numeric_features] = self.scaler.transform(
                X_transformed[self.numeric_features]
            )
        
        # Codificar features categóricas
        for col in self.categorical_features:
            X_transformed[col] = self.encoders[col].transform(
                X_transformed[col].astype(str)
            )
        
        return X_transformed
    
    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Ajusta y transforma en un solo paso.
        
        Args:
            X: DataFrame con features
        
        Returns:
            DataFrame transformado
        """
        return self.fit(X).transform(X)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia el dataset eliminando valores nulos y duplicados.
    
    Args:
        df: DataFrame original
    
    Returns:
        DataFrame limpio
    """
    df_clean = df.copy()
    
    # Información inicial
    logger.info(f"Tamaño inicial: {df_clean.shape}")
    logger.info(f"Valores nulos: {df_clean.isnull().sum().sum()}")
    logger.info(f"Duplicados: {df_clean.duplicated().sum()}")
    
    # Eliminar duplicados
    df_clean = df_clean.drop_duplicates()
    
    # Manejar valores nulos
    if df_clean.isnull().sum().sum() > 0:
        # Para numéricas: rellenar con mediana
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df_clean[col].isnull().sum() > 0:
                df_clean[col].fillna(df_clean[col].median(), inplace=True)
        
        # Para categóricas: rellenar con moda
        categorical_cols = df_clean.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df_clean[col].isnull().sum() > 0:
                df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
    
    logger.info(f"Tamaño después de limpieza: {df_clean.shape}")
    
    return df_clean


def remove_outliers(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    method: str = 'iqr',
    threshold: float = 3.0
) -> pd.DataFrame:
    """
    Elimina outliers del dataset.
    
    Args:
        df: DataFrame original
        columns: Columnas a revisar (None para todas las numéricas)
        method: Método de detección ('iqr' o 'zscore')
        threshold: Umbral para detección (IQR multiplier o z-score)
    
    Returns:
        DataFrame sin outliers
    """
    df_clean = df.copy()
    
    if columns is None:
        columns = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    
    initial_size = len(df_clean)
    
    for col in columns:
        if method == 'iqr':
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            df_clean = df_clean[
                (df_clean[col] >= lower_bound) & 
                (df_clean[col] <= upper_bound)
            ]
        elif method == 'zscore':
            z_scores = np.abs((df_clean[col] - df_clean[col].mean()) / df_clean[col].std())
            df_clean = df_clean[z_scores < threshold]
    
    removed = initial_size - len(df_clean)
    logger.info(f"Outliers eliminados: {removed} ({removed/initial_size*100:.2f}%)")
    
    return df_clean


def create_train_test_split(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    val_size: float = 0.1,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    """
    Divide los datos en train, validation y test sets.
    
    Args:
        X: Features
        y: Target
        test_size: Proporción del test set
        val_size: Proporción del validation set
        random_state: Semilla aleatoria
    
    Returns:
        Tuple (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    # Split inicial train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Split train/validation
    val_size_adjusted = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=val_size_adjusted, random_state=random_state
    )
    
    logger.info(f"Train set: {X_train.shape}")
    logger.info(f"Validation set: {X_val.shape}")
    logger.info(f"Test set: {X_test.shape}")
    
    return X_train, X_val, X_test, y_train, y_val, y_test


def encode_categorical_features(
    X: pd.DataFrame,
    method: str = 'label',
    columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Codifica variables categóricas.
    
    Args:
        X: DataFrame con features
        method: Método de encoding ('label' o 'onehot')
        columns: Columnas a codificar (None para todas las categóricas)
    
    Returns:
        DataFrame con features codificadas
    """
    X_encoded = X.copy()
    
    if columns is None:
        columns = X_encoded.select_dtypes(include=['object']).columns.tolist()
    
    if method == 'label':
        for col in columns:
            le = LabelEncoder()
            X_encoded[col] = le.fit_transform(X_encoded[col].astype(str))
    
    elif method == 'onehot':
        X_encoded = pd.get_dummies(X_encoded, columns=columns, drop_first=True)
    
    logger.info(f"Features después de encoding: {X_encoded.shape}")
    
    return X_encoded


def scale_features(
    X: pd.DataFrame,
    method: str = 'standard',
    columns: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, object]:
    """
    Escala features numéricas.
    
    Args:
        X: DataFrame con features
        method: Método de scaling ('standard' o 'minmax')
        columns: Columnas a escalar (None para todas las numéricas)
    
    Returns:
        Tuple (DataFrame escalado, scaler object)
    """
    X_scaled = X.copy()
    
    if columns is None:
        columns = X_scaled.select_dtypes(include=[np.number]).columns.tolist()
    
    scaler = StandardScaler() if method == 'standard' else MinMaxScaler()
    X_scaled[columns] = scaler.fit_transform(X_scaled[columns])
    
    logger.info(f"Features escaladas: {len(columns)}")
    
    return X_scaled, scaler
