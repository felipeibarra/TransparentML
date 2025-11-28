"""
Módulo de visualización para análisis PCA
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List
from matplotlib.patches import FancyArrowPatch


# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def plot_pca_scatter(X_pca: np.ndarray, y: np.ndarray, 
                     target_names: list, 
                     title: str = "PCA - Proyección en 2D",
                     save_path: Optional[str] = None) -> None:
    """
    Crea un gráfico de dispersión de los datos proyectados en 2D.
    
    Args:
        X_pca: Datos transformados por PCA (n_samples, 2)
        y: Labels
        target_names: Nombres de las clases
        title: Título del gráfico
        save_path: Ruta para guardar el gráfico
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    markers = ['o', 's', '^']
    
    for i, target_name in enumerate(target_names):
        mask = y == i
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1], 
                  c=colors[i], label=target_name, 
                  marker=markers[i], s=100, alpha=0.7,
                  edgecolors='black', linewidth=0.5)
    
    ax.set_xlabel('Componente Principal 1', fontsize=12, fontweight='bold')
    ax.set_ylabel('Componente Principal 2', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.legend(title='Especies', fontsize=10, title_fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='k', linewidth=0.5, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {save_path}")
    
    plt.show()


def plot_variance_explained(explained_variance_ratio: np.ndarray,
                            cumulative: bool = True,
                            save_path: Optional[str] = None) -> None:
    """
    Visualiza la varianza explicada por cada componente.
    
    Args:
        explained_variance_ratio: Array con ratio de varianza explicada
        cumulative: Si True, muestra también varianza acumulada
        save_path: Ruta para guardar el gráfico
    """
    n_components = len(explained_variance_ratio)
    
    if cumulative:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Varianza individual
        ax1.bar(range(1, n_components + 1), explained_variance_ratio * 100,
               color='#4ECDC4', alpha=0.8, edgecolor='black')
        ax1.set_xlabel('Componente Principal', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Varianza Explicada (%)', fontsize=12, fontweight='bold')
        ax1.set_title('Varianza Explicada por Componente', 
                     fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Añadir valores sobre las barras
        for i, v in enumerate(explained_variance_ratio * 100):
            ax1.text(i + 1, v + 1, f'{v:.2f}%', 
                    ha='center', va='bottom', fontweight='bold')
        
        # Varianza acumulada
        cumsum = np.cumsum(explained_variance_ratio) * 100
        ax2.plot(range(1, n_components + 1), cumsum, 
                marker='o', linewidth=2.5, markersize=8, 
                color='#FF6B6B', markerfacecolor='#FF6B6B',
                markeredgecolor='black', markeredgewidth=1.5)
        ax2.set_xlabel('Número de Componentes', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Varianza Acumulada (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Varianza Explicada Acumulada', 
                     fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=90, color='green', linestyle='--', 
                   label='90% Threshold', alpha=0.5)
        ax2.legend()
        
        # Añadir valores en los puntos
        for i, v in enumerate(cumsum):
            ax2.text(i + 1, v + 2, f'{v:.2f}%', 
                    ha='center', va='bottom', fontsize=9)
        
    else:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(range(1, n_components + 1), explained_variance_ratio * 100,
              color='#4ECDC4', alpha=0.8, edgecolor='black')
        ax.set_xlabel('Componente Principal', fontsize=12, fontweight='bold')
        ax.set_ylabel('Varianza Explicada (%)', fontsize=12, fontweight='bold')
        ax.set_title('Varianza Explicada por Componente', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {save_path}")
    
    plt.show()


def plot_biplot(X_pca: np.ndarray, y: np.ndarray,
                components: np.ndarray, feature_names: list,
                target_names: list,
                save_path: Optional[str] = None) -> None:
    """
    Crea un biplot mostrando datos y vectores de features.
    
    Args:
        X_pca: Datos transformados (n_samples, 2)
        y: Labels
        components: Componentes principales (2, n_features)
        feature_names: Nombres de features
        target_names: Nombres de clases
        save_path: Ruta para guardar
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Scatter de datos
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    for i, target_name in enumerate(target_names):
        mask = y == i
        ax.scatter(X_pca[mask, 0], X_pca[mask, 1],
                  c=colors[i], label=target_name, 
                  s=80, alpha=0.6, edgecolors='black', linewidth=0.5)
    
    # Vectores de features
    scale = 3.5
    for i, feature in enumerate(feature_names):
        ax.arrow(0, 0, 
                components[0, i] * scale, 
                components[1, i] * scale,
                head_width=0.15, head_length=0.15, 
                fc='red', ec='red', linewidth=2, alpha=0.7)
        ax.text(components[0, i] * scale * 1.15, 
               components[1, i] * scale * 1.15,
               feature, fontsize=11, fontweight='bold',
               ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.5', 
                        facecolor='yellow', alpha=0.7))
    
    ax.set_xlabel('PC1', fontsize=12, fontweight='bold')
    ax.set_ylabel('PC2', fontsize=12, fontweight='bold')
    ax.set_title('Biplot PCA - Datos y Vectores de Features', 
                fontsize=14, fontweight='bold', pad=20)
    ax.legend(title='Especies', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.8)
    ax.axvline(x=0, color='k', linewidth=0.8)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Biplot guardado en: {save_path}")
    
    plt.show()


def plot_correlation_heatmap(corr_matrix: pd.DataFrame,
                             save_path: Optional[str] = None) -> None:
    """
    Visualiza la matriz de correlación como heatmap.
    
    Args:
        corr_matrix: Matriz de correlación
        save_path: Ruta para guardar
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(corr_matrix, annot=True, fmt='.3f', 
               cmap='coolwarm', center=0,
               square=True, linewidths=1, 
               cbar_kws={"shrink": 0.8},
               ax=ax)
    
    ax.set_title('Matriz de Correlación - Features del Dataset Iris', 
                fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Heatmap guardado en: {save_path}")
    
    plt.show()


def plot_covariance_matrix(cov_matrix: np.ndarray, 
                          feature_names: list,
                          save_path: Optional[str] = None) -> None:
    """
    Visualiza la matriz de covarianza.
    
    Args:
        cov_matrix: Matriz de covarianza
        feature_names: Nombres de features
        save_path: Ruta para guardar
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    cov_df = pd.DataFrame(cov_matrix, 
                         index=feature_names, 
                         columns=feature_names)
    
    sns.heatmap(cov_df, annot=True, fmt='.3f', 
               cmap='viridis', 
               square=True, linewidths=1,
               cbar_kws={"shrink": 0.8},
               ax=ax)
    
    ax.set_title('Matriz de Covarianza - Datos Estandarizados', 
                fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Matriz de covarianza guardada en: {save_path}")
    
    plt.show()


def plot_comparison_manual_vs_sklearn(X_manual: np.ndarray, 
                                      X_sklearn: np.ndarray,
                                      y: np.ndarray,
                                      target_names: list,
                                      save_path: Optional[str] = None) -> None:
    """
    Compara resultados de PCA manual vs sklearn.
    
    Args:
        X_manual: Datos transformados manualmente
        X_sklearn: Datos transformados con sklearn
        y: Labels
        target_names: Nombres de clases
        save_path: Ruta para guardar
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    # PCA Manual
    for i, target_name in enumerate(target_names):
        mask = y == i
        ax1.scatter(X_manual[mask, 0], X_manual[mask, 1],
                   c=colors[i], label=target_name, s=80, alpha=0.7)
    ax1.set_xlabel('PC1', fontsize=12, fontweight='bold')
    ax1.set_ylabel('PC2', fontsize=12, fontweight='bold')
    ax1.set_title('PCA Manual (Autovalores/Autovectores)', 
                 fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # PCA Sklearn
    for i, target_name in enumerate(target_names):
        mask = y == i
        ax2.scatter(X_sklearn[mask, 0], X_sklearn[mask, 1],
                   c=colors[i], label=target_name, s=80, alpha=0.7)
    ax2.set_xlabel('PC1', fontsize=12, fontweight='bold')
    ax2.set_ylabel('PC2', fontsize=12, fontweight='bold')
    ax2.set_title('PCA Sklearn', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Comparación guardada en: {save_path}")
    
    plt.show()
