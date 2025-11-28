"""
Módulo src - Implementación de PCA y análisis
"""

from .pca_manual import PCAManual
from .data_loader import (
    load_iris_data,
    standardize_data,
    create_dataframe,
    get_data_statistics,
    get_correlation_matrix
)
from .visualization import (
    plot_pca_scatter,
    plot_variance_explained,
    plot_biplot,
    plot_correlation_heatmap,
    plot_covariance_matrix,
    plot_comparison_manual_vs_sklearn
)

__all__ = [
    'PCAManual',
    'load_iris_data',
    'standardize_data',
    'create_dataframe',
    'get_data_statistics',
    'get_correlation_matrix',
    'plot_pca_scatter',
    'plot_variance_explained',
    'plot_biplot',
    'plot_correlation_heatmap',
    'plot_covariance_matrix',
    'plot_comparison_manual_vs_sklearn'
]
