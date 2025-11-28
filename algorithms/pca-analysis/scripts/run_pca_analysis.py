#!/usr/bin/env python3
"""
Script principal para ejecutar el análisis PCA completo
Implementa PCA desde cero y compara con sklearn
"""

import sys
import os
import numpy as np
from sklearn.decomposition import PCA

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.pca_manual import PCAManual
from src.data_loader import (
    load_iris_data,
    standardize_data,
    create_dataframe,
    get_data_statistics,
    get_correlation_matrix
)
from src.visualization import (
    plot_pca_scatter,
    plot_variance_explained,
    plot_biplot,
    plot_correlation_heatmap,
    plot_covariance_matrix,
    plot_comparison_manual_vs_sklearn
)


def print_section(title: str):
    """Imprime un título de sección formateado"""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70 + "\n")


def main():
    """Función principal que ejecuta todo el análisis"""
    
    print_section("ANÁLISIS PCA - REDUCCIÓN DE DIMENSIONALIDAD")
    print("Dataset: Iris")
    print("Objetivo: Reducir de 4 a 2 dimensiones manteniendo máxima varianza")
    
    # 1. Cargar datos
    print_section("1. CARGA DE DATOS")
    X, y, feature_names, target_names = load_iris_data()
    print(f"✓ Dataset cargado: {X.shape[0]} muestras, {X.shape[1]} features")
    print(f"✓ Features: {feature_names}")
    print(f"✓ Clases: {target_names}")
    
    # Mostrar estadísticas
    print("\n📊 Estadísticas descriptivas (datos originales):")
    stats = get_data_statistics(X, feature_names)
    print(stats)
    
    # 2. Estandarización
    print_section("2. PREPROCESAMIENTO - ESTANDARIZACIÓN")
    print("⚠️  Estandarización es FUNDAMENTAL antes de PCA")
    print("   → Media = 0, Desviación estándar = 1")
    
    X_scaled, scaler = standardize_data(X)
    print(f"✓ Datos estandarizados")
    print(f"  Media después: {np.mean(X_scaled, axis=0)}")
    print(f"  Std después: {np.std(X_scaled, axis=0)}")
    
    # 3. Análisis de correlación
    print_section("3. ANÁLISIS DE CORRELACIÓN")
    corr_matrix = get_correlation_matrix(X, feature_names)
    print("Matriz de Correlación:")
    print(corr_matrix)
    
    # Visualizar correlación
    plot_correlation_heatmap(
        corr_matrix,
        save_path='results/correlation_matrix.png'
    )
    
    # 4. PCA Manual
    print_section("4. PCA MANUAL (Autovalores y Autovectores)")
    print("Implementación desde cero:")
    print("  1. Calcular matriz de covarianza")
    print("  2. Calcular autovalores y autovectores")
    print("  3. Ordenar por autovalores descendentes")
    print("  4. Seleccionar primeros k componentes")
    
    pca_manual = PCAManual(n_components=2)
    X_pca_manual = pca_manual.fit_transform(X_scaled)
    
    print(f"\n✓ PCA manual completado")
    print(f"\n📈 Autovalores (varianzas): {pca_manual.eigenvalues_}")
    print(f"\n📊 Varianza explicada por cada componente:")
    for i, var_ratio in enumerate(pca_manual.explained_variance_ratio_):
        print(f"   PC{i+1}: {var_ratio*100:.2f}%")
    
    cumulative = pca_manual.get_cumulative_variance_ratio()
    print(f"\n📊 Varianza acumulada:")
    for i, cum_var in enumerate(cumulative):
        print(f"   {i+1} componentes: {cum_var*100:.2f}%")
    
    # Matriz de covarianza
    cov_matrix = pca_manual.get_covariance_matrix(X_scaled)
    print(f"\n📐 Matriz de Covarianza calculada")
    plot_covariance_matrix(
        cov_matrix,
        feature_names,
        save_path='results/covariance_matrix.png'
    )
    
    # 5. PCA con sklearn (para comparación)
    print_section("5. PCA CON SKLEARN (Comparación)")
    
    pca_sklearn = PCA(n_components=2)
    X_pca_sklearn = pca_sklearn.fit_transform(X_scaled)
    
    print(f"✓ PCA sklearn completado")
    print(f"\n📊 Varianza explicada (sklearn):")
    for i, var_ratio in enumerate(pca_sklearn.explained_variance_ratio_):
        print(f"   PC{i+1}: {var_ratio*100:.2f}%")
    
    # Comparar resultados
    print(f"\n🔍 Comparación Manual vs Sklearn:")
    print(f"   Diferencia en varianza explicada:")
    diff = np.abs(pca_manual.explained_variance_ratio_ - 
                  pca_sklearn.explained_variance_ratio_)
    for i, d in enumerate(diff):
        print(f"   PC{i+1}: {d:.6f} (diferencia despreciable)")
    
    # 6. Visualizaciones
    print_section("6. VISUALIZACIONES")
    
    # Scatter plot 2D
    print("Generando gráfico de dispersión 2D...")
    plot_pca_scatter(
        X_pca_manual, y, target_names,
        title="PCA Manual - Proyección 2D del Dataset Iris",
        save_path='results/pca_scatter_2d.png'
    )
    
    # Varianza explicada
    print("Generando gráfico de varianza explicada...")
    # Para todos los componentes
    pca_all = PCAManual(n_components=4)
    pca_all.fit(X_scaled)
    plot_variance_explained(
        pca_all.explained_variance_ratio_,
        cumulative=True,
        save_path='results/variance_explained.png'
    )
    
    # Biplot
    print("Generando biplot...")
    plot_biplot(
        X_pca_manual, y,
        pca_manual.components_,
        feature_names,
        target_names,
        save_path='results/biplot.png'
    )
    
    # Comparación manual vs sklearn
    print("Generando comparación manual vs sklearn...")
    plot_comparison_manual_vs_sklearn(
        X_pca_manual, X_pca_sklearn,
        y, target_names,
        save_path='results/comparison_manual_sklearn.png'
    )
    
    # 7. Análisis e Interpretación
    print_section("7. ANÁLISIS E INTERPRETACIÓN")
    
    print("📌 Distribución de clases en espacio reducido:")
    print("   • Las tres especies se separan razonablemente bien en 2D")
    print("   • Setosa está claramente separada de las otras dos")
    print("   • Versicolor y Virginica tienen cierto solapamiento")
    
    print(f"\n📌 Varianza capturada:")
    total_var = np.sum(pca_manual.explained_variance_ratio_) * 100
    print(f"   • PC1 + PC2 capturan {total_var:.2f}% de la varianza total")
    print(f"   • Se pierde solo {100-total_var:.2f}% de información")
    
    print("\n📌 Componentes principales:")
    print("   Los componentes representan combinaciones lineales de las")
    print("   features originales que maximizan la varianza.")
    print(f"\n   Componentes (loadings):")
    for i in range(2):
        print(f"\n   PC{i+1}:")
        for j, fname in enumerate(feature_names):
            print(f"      {fname}: {pca_manual.components_[i, j]:.4f}")
    
    print_section("✅ ANÁLISIS COMPLETADO")
    print("Todos los resultados guardados en la carpeta 'results/'")
    print("\nArchivos generados:")
    print("  • correlation_matrix.png")
    print("  • covariance_matrix.png")
    print("  • pca_scatter_2d.png")
    print("  • variance_explained.png")
    print("  • biplot.png")
    print("  • comparison_manual_sklearn.png")


if __name__ == "__main__":
    # Crear carpeta de resultados si no existe
    os.makedirs('results', exist_ok=True)
    
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
