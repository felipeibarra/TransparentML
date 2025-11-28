#!/usr/bin/env python3
"""
Script principal de entrenamiento de modelos de regresión.

Este script carga el dataset KDD Cup, realiza preprocesamiento,
entrena múltiples modelos y guarda los resultados.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
import pandas as pd
from datetime import datetime

from src.data_loader import load_kdd_data, split_features_target
from src.preprocessing import (
    clean_data, 
    encode_categorical_features,
    create_train_test_split,
    DataPreprocessor
)
from src.models import (
    LinearRegressionModel,
    RidgeRegressionModel,
    LassoRegressionModel,
    ElasticNetModel,
    PolynomialRegressionModel,
    save_model
)
from src.evaluation import (
    evaluate_model,
    plot_predictions,
    plot_residuals,
    save_metrics,
    compare_models
)
from src.utils import timer, ensure_dir
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@timer
def main():
    """Función principal de entrenamiento."""
    
    logger.info("="*80)
    logger.info("INICIANDO ENTRENAMIENTO DE MODELOS DE REGRESIÓN LINEAL")
    logger.info("="*80)
    
    # Configuración
    DATA_PATH = "kddcup.data_10_percent"
    SAMPLE_SIZE = 50000  # Usar muestra para velocidad
    TARGET_COLUMN = 'duration'
    
    # Directorios
    ensure_dir("results/figures")
    ensure_dir("results/metrics")
    ensure_dir("results/models")
    
    # 1. CARGA DE DATOS
    logger.info("\n[1/6] Cargando datos...")
    df = load_kdd_data(DATA_PATH, nrows=SAMPLE_SIZE)
    logger.info(f"Dataset cargado: {df.shape}")
    
    # 2. LIMPIEZA
    logger.info("\n[2/6] Limpiando datos...")
    df_clean = clean_data(df)
    
    # 3. SEPARAR FEATURES Y TARGET
    logger.info("\n[3/6] Separando features y target...")
    X, y = split_features_target(df_clean, TARGET_COLUMN)
    
    # Codificar variables categóricas
    X_encoded = encode_categorical_features(X, method='label')
    
    # 4. SPLIT TRAIN/TEST
    logger.info("\n[4/6] Dividiendo datos...")
    X_train, X_val, X_test, y_train, y_val, y_test = create_train_test_split(
        X_encoded, y, test_size=0.2, val_size=0.1
    )
    
    # Preprocesar (escalar)
    preprocessor = DataPreprocessor(scaling_method='standard')
    X_train_scaled = preprocessor.fit_transform(X_train)
    X_val_scaled = preprocessor.transform(X_val)
    X_test_scaled = preprocessor.transform(X_test)
    
    # 5. ENTRENAMIENTO DE MODELOS
    logger.info("\n[5/6] Entrenando modelos...")
    
    models = {
        'Linear Regression': LinearRegressionModel(),
        'Ridge (alpha=1.0)': RidgeRegressionModel(alpha=1.0),
        'Lasso (alpha=0.1)': LassoRegressionModel(alpha=0.1),
        'ElasticNet': ElasticNetModel(alpha=0.1, l1_ratio=0.5)
    }
    
    results = {}
    
    for name, model in models.items():
        logger.info(f"\nEntrenando {name}...")
        model.fit(X_train_scaled, y_train)
        
        # Evaluar
        metrics = evaluate_model(
            model, X_train_scaled, y_train, X_test_scaled, y_test
        )
        results[name] = metrics
        
        # Guardar modelo
        model_path = f"results/models/{name.replace(' ', '_').lower()}.joblib"
        save_model(model, model_path)
        
        # Visualizaciones
        y_test_pred = model.predict(X_test_scaled)
        plot_predictions(
            y_test, y_test_pred,
            title=f"{name} - Predicciones vs Reales",
            save_path=f"results/figures/{name.replace(' ', '_').lower()}_predictions.png"
        )
        plot_residuals(
            y_test, y_test_pred,
            save_path=f"results/figures/{name.replace(' ', '_').lower()}_residuals.png"
        )
    
    # 6. COMPARACIÓN Y RESULTADOS
    logger.info("\n[6/6] Generando resultados finales...")
    
    # Comparar modelos
    comparison = compare_models(results)
    logger.info("\n" + "="*80)
    logger.info("COMPARACIÓN DE MODELOS")
    logger.info("="*80)
    print(comparison.to_string(index=False))
    
    # Guardar comparación
    comparison.to_csv("results/metrics/model_comparison.csv", index=False)
    
    # Guardar métricas detalladas
    save_metrics(results, "results/metrics/detailed_metrics.json")
    
    # Mejor modelo
    best_model_name = comparison.iloc[0]['Model']
    best_test_r2 = comparison.iloc[0]['Test R²']
    
    logger.info("\n" + "="*80)
    logger.info(f"MEJOR MODELO: {best_model_name}")
    logger.info(f"Test R² Score: {best_test_r2:.4f}")
    logger.info("="*80)
    
    logger.info("\n✅ Entrenamiento completado exitosamente!")
    logger.info(f"📁 Resultados guardados en: results/")
    logger.info(f"📊 Modelos guardados en: results/models/")
    logger.info(f"📈 Visualizaciones en: results/figures/")


if __name__ == "__main__":
    main()
