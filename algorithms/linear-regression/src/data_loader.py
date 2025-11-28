"""
Módulo para carga y lectura de datos del KDD Cup 1999.

Este módulo maneja la carga del dataset, definición de columnas,
y validación inicial de los datos.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Definición de columnas del KDD Cup 1999 Dataset
KDD_COLUMNS = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes',
    'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
    'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
    'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
    'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate',
    'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
    'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
    'dst_host_srv_count', 'dst_host_same_srv_rate',
    'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
    'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
    'dst_host_srv_rerror_rate', 'label'
]


def load_kdd_data(
    file_path: str,
    nrows: Optional[int] = None,
    sample_frac: Optional[float] = None
) -> pd.DataFrame:
    """
    Carga el dataset KDD Cup 1999.
    
    Args:
        file_path: Ruta al archivo de datos
        nrows: Número de filas a cargar (None para todas)
        sample_frac: Fracción de datos a samplear (0.0-1.0)
    
    Returns:
        DataFrame con los datos cargados
    
    Example:
        >>> df = load_kdd_data('kddcup.data_10_percent', nrows=10000)
        >>> print(df.shape)
    """
    logger.info(f"Cargando datos desde: {file_path}")
    
    try:
        # Cargar datos sin encabezado
        df = pd.read_csv(
            file_path,
            names=KDD_COLUMNS,
            nrows=nrows,
            low_memory=False
        )
        
        # Samplear si se especifica
        if sample_frac is not None and 0 < sample_frac < 1:
            df = df.sample(frac=sample_frac, random_state=42)
            logger.info(f"Datos sampleados: {len(df)} registros")
        
        logger.info(f"Datos cargados exitosamente: {df.shape}")
        return df
    
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error al cargar datos: {str(e)}")
        raise


def get_data_info(df: pd.DataFrame) -> dict:
    """
    Obtiene información básica del dataset.
    
    Args:
        df: DataFrame a analizar
    
    Returns:
        Diccionario con información del dataset
    """
    info = {
        'n_samples': len(df),
        'n_features': len(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'dtypes': df.dtypes.value_counts().to_dict(),
        'numeric_features': df.select_dtypes(include=[np.number]).columns.tolist(),
        'categorical_features': df.select_dtypes(include=['object']).columns.tolist()
    }
    
    return info


def split_features_target(
    df: pd.DataFrame,
    target_column: str = 'duration'
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Separa features y target del dataset.
    
    Args:
        df: DataFrame original
        target_column: Nombre de la columna objetivo
    
    Returns:
        Tuple (X, y) con features y target
    """
    if target_column not in df.columns:
        raise ValueError(f"Columna objetivo '{target_column}' no encontrada")
    
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    logger.info(f"Features shape: {X.shape}, Target shape: {y.shape}")
    
    return X, y


def save_data(df: pd.DataFrame, file_path: str) -> None:
    """
    Guarda el DataFrame en formato CSV.
    
    Args:
        df: DataFrame a guardar
        file_path: Ruta donde guardar el archivo
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)
    logger.info(f"Datos guardados en: {file_path}")


def load_processed_data(file_path: str) -> pd.DataFrame:
    """
    Carga datos procesados previamente.
    
    Args:
        file_path: Ruta al archivo procesado
    
    Returns:
        DataFrame con los datos procesados
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
    
    df = pd.read_csv(file_path)
    logger.info(f"Datos procesados cargados: {df.shape}")
    
    return df
