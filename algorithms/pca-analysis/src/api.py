import os
from pathlib import Path
from datetime import datetime
from typing import Any

os.environ.setdefault("MPLBACKEND", "Agg")

import numpy as np
from fastapi import FastAPI, HTTPException
from sklearn.decomposition import PCA

from src.pca_manual import PCAManual
from src.data_loader import (
    load_iris_data,
    standardize_data,
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

RESULTS_DIR = Path("results")
PLOT_FILES = {
    "correlation_matrix": RESULTS_DIR / "correlation_matrix.png",
    "covariance_matrix": RESULTS_DIR / "covariance_matrix.png",
    "pca_scatter": RESULTS_DIR / "pca_scatter_2d.png",
    "variance_explained": RESULTS_DIR / "variance_explained.png",
    "biplot": RESULTS_DIR / "biplot.png",
    "comparison_manual_sklearn": RESULTS_DIR / "comparison_manual_sklearn.png"
}

analysis_cache: dict[str, Any] | None = None

app = FastAPI(
    title="PCA Service - Tarea 2",
    description="Servicio de análisis PCA que expone métricas, comparaciones y visualizaciones.",
    version="1.0.0"
)


def build_analysis() -> dict[str, Any]:
    """Ejecuta el análisis PCA completo y serializa los resultados."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    X, y, feature_names, target_names = load_iris_data()
    X_scaled, _ = standardize_data(X)
    stats = get_data_statistics(X, feature_names)
    corr_matrix = get_correlation_matrix(X, feature_names)

    pca_manual = PCAManual(n_components=2)
    X_pca_manual = pca_manual.fit_transform(X_scaled)
    cov_matrix = pca_manual.get_covariance_matrix(X_scaled)
    loadings = pca_manual.get_loadings()

    pca_sklearn = PCA(n_components=2)
    X_pca_sklearn = pca_sklearn.fit_transform(X_scaled)

    pca_full = PCAManual(n_components=4)
    pca_full.fit(X_scaled)

    plot_correlation_heatmap(
        corr_matrix,
        save_path=str(PLOT_FILES["correlation_matrix"])
    )
    plot_covariance_matrix(
        cov_matrix,
        feature_names,
        save_path=str(PLOT_FILES["covariance_matrix"])
    )
    plot_pca_scatter(
        X_pca_manual,
        y,
        target_names,
        title="PCA Manual - Proyección 2D del Dataset Iris",
        save_path=str(PLOT_FILES["pca_scatter"])
    )
    plot_variance_explained(
        pca_full.explained_variance_ratio_,
        cumulative=True,
        save_path=str(PLOT_FILES["variance_explained"])
    )
    plot_biplot(
        X_pca_manual,
        y,
        pca_manual.components_,
        feature_names,
        target_names,
        save_path=str(PLOT_FILES["biplot"])
    )
    plot_comparison_manual_vs_sklearn(
        X_pca_manual,
        X_pca_sklearn,
        y,
        target_names,
        save_path=str(PLOT_FILES["comparison_manual_sklearn"])
    )

    component_loadings = []
    for idx in range(loadings.shape[1]):
        component_loadings.append({
            feature_names[j]: float(loadings[j, idx])
            for j in range(len(feature_names))
        })

    variance_manual = pca_manual.explained_variance_ratio_
    variance_sklearn = pca_sklearn.explained_variance_ratio_

    return {
        "dataset": "Iris",
        "created_at": datetime.utcnow().isoformat(),
        "samples": X.shape[0],
        "features": feature_names,
        "target_names": target_names,
        "descriptive_statistics": stats.round(4).to_dict(),
        "correlation_matrix": corr_matrix.round(4).to_dict(),
        "covariance_matrix": cov_matrix.round(4).tolist(),
        "manual_variance_ratio": variance_manual.tolist(),
        "sklearn_variance_ratio": variance_sklearn.tolist(),
        "variance_difference": np.abs(variance_manual - variance_sklearn).round(6).tolist(),
        "cumulative_variance": pca_manual.get_cumulative_variance_ratio().tolist(),
        "component_loadings": component_loadings,
        "plots": {name: str(path) for name, path in PLOT_FILES.items()},
        "scores_preview": X_pca_manual[:5].tolist(),
        "analysis_summary": {
            "pc1_variance": float(variance_manual[0]),
            "pc2_variance": float(variance_manual[1]),
            "total_variance_explained": float(np.sum(variance_manual)),
            "variance_loss_percent": float((1 - np.sum(variance_manual)) * 100)
        }
    }


@app.on_event("startup")
async def init_analysis():
    global analysis_cache
    analysis_cache = build_analysis()


@app.get("/health")
async def health():
    """Endpoint de salud del servicio."""
    status = "ready" if analysis_cache else "initializing"
    return {"status": status, "timestamp": datetime.utcnow().isoformat()}


@app.get("/analysis")
async def get_analysis():
    """Entrega los resultados del análisis PCA."""
    if not analysis_cache:
        raise HTTPException(status_code=503, detail="El análisis aún se está construyendo")
    return analysis_cache


@app.post("/refresh")
async def refresh_analysis():
    """Reconstruye el análisis y sus visualizaciones."""
    global analysis_cache
    analysis_cache = build_analysis()
    return {"status": "refreshed", "timestamp": datetime.utcnow().isoformat()}
