"""
Linear Regression API Service
==============================
FastAPI service for Linear Regression predictions and analysis.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
import logging
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import LinearRegressionModel, RidgeRegressionModel, PolynomialRegressionModel
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TransparentML Linear Regression Service",
    description="Linear Regression API for predictions and analysis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global models
linear_model: Optional[LinearRegressionModel] = None
demo_trained = False


class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str
    model_loaded: bool


class TrainRequest(BaseModel):
    X: List[List[float]] = Field(..., description="Training features")
    y: List[float] = Field(..., description="Training targets")
    model_type: str = Field(default="linear", description="linear, ridge, or polynomial")


class PredictRequest(BaseModel):
    X: List[List[float]] = Field(..., description="Features for prediction")


class DemoAnalysisRequest(BaseModel):
    n_samples: int = Field(default=100, ge=50, le=500)
    noise: float = Field(default=10.0, ge=0.0, le=50.0)


def load_demo_model():
    """Load demo model with synthetic data."""
    global linear_model, demo_trained
    
    try:
        # Generate synthetic data
        np.random.seed(42)
        X = np.random.rand(100, 1) * 100
        y = 2.5 * X.squeeze() + 30 + np.random.randn(100) * 10
        
        X_df = pd.DataFrame(X, columns=['feature'])
        y_series = pd.Series(y, name='target')
        
        linear_model = LinearRegressionModel()
        linear_model.fit(X_df, y_series)
        demo_trained = True
        
        logger.info("Demo linear regression model loaded")
        return True
    except Exception as e:
        logger.error(f"Failed to load demo model: {e}")
        return False


@app.on_event("startup")
async def startup_event():
    """Initialize demo model on startup."""
    logger.info("Starting Linear Regression service...")
    load_demo_model()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "TransparentML Linear Regression",
        "version": "1.0.0",
        "algorithms": ["Linear Regression", "Ridge Regression", "Polynomial Regression"],
        "endpoints": {
            "health": "/health",
            "train": "/api/v1/train",
            "predict": "/api/v1/predict",
            "demo_analysis": "/api/v1/demo/analyze",
            "coefficients": "/api/v1/coefficients",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="linear-regression",
        timestamp=datetime.now().isoformat(),
        model_loaded=demo_trained
    )


@app.post("/api/v1/train")
async def train_model(request: TrainRequest):
    """Train a linear regression model."""
    global linear_model
    
    try:
        X = pd.DataFrame(request.X)
        y = pd.Series(request.y)
        
        if request.model_type == "linear":
            linear_model = LinearRegressionModel()
        elif request.model_type == "ridge":
            linear_model = RidgeRegressionModel(alpha=1.0)
        elif request.model_type == "polynomial":
            linear_model = PolynomialRegressionModel(degree=2)
        else:
            raise HTTPException(status_code=400, detail="Invalid model type")
        
        linear_model.fit(X, y)
        
        logger.info(f"Trained {request.model_type} model with {len(X)} samples")
        
        return {
            "status": "success",
            "model_type": request.model_type,
            "n_samples": len(X),
            "n_features": X.shape[1],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/predict")
async def predict(request: PredictRequest):
    """Make predictions."""
    global linear_model
    
    if linear_model is None or not linear_model.is_fitted:
        raise HTTPException(
            status_code=400,
            detail="No model trained. Use /api/v1/train or /api/v1/demo/analyze first"
        )
    
    try:
        X = pd.DataFrame(request.X)
        predictions = linear_model.predict(X).tolist()
        
        return {
            "status": "success",
            "predictions": predictions,
            "n_samples": len(predictions),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/coefficients")
async def get_coefficients():
    """Get model coefficients."""
    global linear_model
    
    if linear_model is None or not linear_model.is_fitted:
        raise HTTPException(status_code=400, detail="No model trained")
    
    try:
        coefs = linear_model.get_coefficients()
        return {
            "status": "success",
            "coefficients": coefs,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/demo/analyze")
async def demo_analysis(request: DemoAnalysisRequest):
    """
    Run demo analysis with synthetic data.
    
    Returns metrics, predictions, and visualization data.
    """
    try:
        from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
        from sklearn.model_selection import train_test_split
        
        # Generate synthetic data
        np.random.seed(42)
        X = np.random.rand(request.n_samples, 1) * 100
        true_slope = 2.5
        true_intercept = 30
        y = true_slope * X.squeeze() + true_intercept + np.random.randn(request.n_samples) * request.noise
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Train model
        X_train_df = pd.DataFrame(X_train, columns=['x'])
        y_train_series = pd.Series(y_train)
        
        model = LinearRegressionModel()
        model.fit(X_train_df, y_train_series)
        
        # Predictions
        X_test_df = pd.DataFrame(X_test, columns=['x'])
        y_pred = model.predict(X_test_df)
        
        # Metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        coefs = model.get_coefficients()
        
        logger.info(f"Demo analysis: R² = {r2:.4f}, RMSE = {rmse:.2f}")
        
        return {
            "status": "success",
            "metrics": {
                "r2_score": float(r2),
                "rmse": float(rmse),
                "mse": float(mse),
                "mae": float(mae),
                "n_train_samples": len(X_train),
                "n_test_samples": len(X_test)
            },
            "model_coefficients": {
                "slope": float(coefs['coefficients'][0]),
                "intercept": float(coefs['intercept']),
                "true_slope": true_slope,
                "true_intercept": true_intercept
            },
            "predictions_sample": {
                "X_test": X_test[:10].tolist(),
                "y_test": y_test[:10].tolist(),
                "y_pred": y_pred[:10].tolist()
            },
            "scatter_data": {
                "X_train": X_train.tolist(),
                "y_train": y_train.tolist(),
                "X_test": X_test.tolist(),
                "y_test": y_test.tolist(),
                "y_pred": y_pred.tolist()
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Demo analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
