"""
API de Predicción - Tarea 1 Regresión Lineal
FastAPI service para servir modelos de ML entrenados
"""
import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any
import logging
from datetime import datetime

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
import joblib
import numpy as np
import pandas as pd

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Métricas Prometheus
prediction_counter = Counter('predictions_total', 'Total number of predictions')
prediction_latency = Histogram('prediction_latency_seconds', 'Prediction latency')
error_counter = Counter('prediction_errors_total', 'Total prediction errors')

# Inicializar FastAPI
app = FastAPI(
    title="ML Prediction API - Tarea 1",
    description="API para predicciones de regresión lineal sobre datos de red",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos globales
model = None
scaler = None
feature_names = None

# Schemas de entrada/salida
class PredictionInput(BaseModel):
    """Entrada para predicción"""
    features: List[float] = Field(..., description="Features del modelo")
    
    class Config:
        json_schema_extra = {
            "example": {
                "features": [0, 181, 5450, 0, 0, 0, 0, 0, 0, 0]
            }
        }

class PredictionOutput(BaseModel):
    """Salida de predicción"""
    prediction: float = Field(..., description="Valor predicho")
    timestamp: str = Field(..., description="Timestamp de la predicción")
    model_version: str = Field(..., description="Versión del modelo")

class BatchPredictionInput(BaseModel):
    """Entrada para predicciones batch"""
    features: List[List[float]] = Field(..., description="Lista de features")

class BatchPredictionOutput(BaseModel):
    """Salida de predicciones batch"""
    predictions: List[float] = Field(..., description="Valores predichos")
    count: int = Field(..., description="Número de predicciones")
    timestamp: str = Field(..., description="Timestamp de la predicción")

class HealthResponse(BaseModel):
    """Respuesta de health check"""
    status: str
    model_loaded: bool
    timestamp: str


def load_model():
    """Cargar modelo entrenado"""
    global model, scaler, feature_names
    
    model_path = os.getenv('MODEL_PATH', '/app/results/models')
    Path(model_path).mkdir(parents=True, exist_ok=True)
    
    try:
        # Buscar último modelo
        model_files = list(Path(model_path).glob('*.joblib'))
        if not model_files:
            logger.info("No models found in MODEL_PATH, ejecutando entrenamiento local")
            if not trigger_training():
                logger.error("Entrenamiento de emergencia fallido")
                return False
            model_files = list(Path(model_path).glob('*.joblib'))
            if not model_files:
                logger.error("No se generaron modelos tras el entrenamiento")
                return False
        
        latest_model = max(model_files, key=os.path.getctime)
        logger.info(f"Loading model from {latest_model}")
        
        # Cargar modelo
        model_data = joblib.load(latest_model)
        
        if isinstance(model_data, dict):
            model = model_data.get('model')
            scaler = model_data.get('scaler')
            feature_names = model_data.get('feature_names', [])
        else:
            model = model_data
            
        logger.info("Model loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False


def trigger_training() -> bool:
    """Ejecuta el pipeline de entrenamiento para generar modelos localmente."""
    training_script = Path(__file__).resolve().parents[2] / "scripts" / "train.py"
    if not training_script.exists():
        logger.error(f"Script de entrenamiento no encontrado: {training_script}")
        return False

    logger.info("Iniciando entrenamiento local para preparar modelos")
    try:
        subprocess.run(
            [sys.executable, str(training_script)],
            check=True,
            cwd=str(training_script.parent.parent)
        )
        logger.info("Entrenamiento completo; modelos disponibles")
        return True
    except subprocess.CalledProcessError as exc:
        logger.error(f"Entrenamiento fallido: {exc}")
        return False


@app.on_event("startup")
async def startup_event():
    """Evento de inicio"""
    logger.info("Starting ML Prediction API...")
    load_model()


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "ML Prediction API - Tarea 1",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "batch_predict": "/batch_predict",
            "metrics": "/metrics"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        model_loaded=model is not None,
        timestamp=datetime.now().isoformat()
    )


@app.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
async def predict(input_data: PredictionInput):
    """
    Realizar predicción individual
    """
    if model is None:
        error_counter.inc()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    try:
        with prediction_latency.time():
            # Preparar datos
            features = np.array(input_data.features).reshape(1, -1)
            
            # Escalar si existe scaler
            if scaler is not None:
                features = scaler.transform(features)
            
            # Predicción
            prediction = model.predict(features)[0]
            
            prediction_counter.inc()
            
            return PredictionOutput(
                prediction=float(prediction),
                timestamp=datetime.now().isoformat(),
                model_version="1.0.0"
            )
            
    except Exception as e:
        error_counter.inc()
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/batch_predict", response_model=BatchPredictionOutput, tags=["Prediction"])
async def batch_predict(input_data: BatchPredictionInput):
    """
    Realizar predicciones batch
    """
    if model is None:
        error_counter.inc()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    try:
        with prediction_latency.time():
            # Preparar datos
            features = np.array(input_data.features)
            
            # Escalar si existe scaler
            if scaler is not None:
                features = scaler.transform(features)
            
            # Predicciones
            predictions = model.predict(features)
            
            prediction_counter.inc(len(predictions))
            
            return BatchPredictionOutput(
                predictions=predictions.tolist(),
                count=len(predictions),
                timestamp=datetime.now().isoformat()
            )
            
    except Exception as e:
        error_counter.inc()
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch prediction failed: {str(e)}"
        )


@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """
    Métricas Prometheus
    """
    return Response(content=generate_latest(), media_type="text/plain")


@app.post("/reload_model", tags=["Management"])
async def reload_model():
    """
    Recargar modelo
    """
    success = load_model()
    if success:
        return {"status": "success", "message": "Model reloaded"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reload model"
        )


@app.get("/model_info", tags=["Management"])
async def model_info():
    """
    Información del modelo
    """
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not loaded"
        )
    
    return {
        "model_type": type(model).__name__,
        "feature_names": feature_names if feature_names else "Not available",
        "has_scaler": scaler is not None,
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
