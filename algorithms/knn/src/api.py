"""
KNN API Service
===============
FastAPI service for K-Nearest Neighbors classification and regression.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
from datetime import datetime
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.knn_model import KNNClassifier, KNNRegressor
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="TransparentML KNN Service",
    description="K-Nearest Neighbors Classification and Regression API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global models (trained on startup with demo data)
classifier: Optional[KNNClassifier] = None
regressor: Optional[KNNRegressor] = None
demo_data_loaded = False


# Pydantic models
class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str
    models_loaded: bool


class TrainRequest(BaseModel):
    X: List[List[float]] = Field(..., description="Training features")
    y: List[float] = Field(..., description="Training labels")
    n_neighbors: int = Field(default=3, ge=1, le=20)
    metric: Literal["euclidean", "manhattan", "minkowski"] = Field(default="euclidean")
    weights: Literal["uniform", "distance"] = Field(default="uniform")
    task: Literal["classification", "regression"] = Field(default="classification")


class PredictRequest(BaseModel):
    X: List[List[float]] = Field(..., description="Features to predict")
    task: Literal["classification", "regression"] = Field(default="classification")


class DemoAnalysisRequest(BaseModel):
    dataset: Literal["iris", "random"] = Field(default="iris")
    n_neighbors: int = Field(default=5, ge=1, le=20)
    test_size: float = Field(default=0.3, ge=0.1, le=0.5)


# Helper functions
def load_demo_data():
    """Load Iris dataset for demo purposes."""
    try:
        from sklearn.datasets import load_iris
        from sklearn.model_selection import train_test_split
        
        iris = load_iris()
        X_train, X_test, y_train, y_test = train_test_split(
            iris.data, iris.target, test_size=0.3, random_state=42
        )
        
        global classifier, demo_data_loaded
        classifier = KNNClassifier(n_neighbors=5, metric='euclidean', weights='uniform')
        classifier.fit(X_train, y_train)
        
        accuracy = classifier.score(X_test, y_test)
        demo_data_loaded = True
        
        logger.info(f"Demo Iris classifier loaded with {accuracy:.2%} accuracy")
        
        return {
            "X_train_shape": X_train.shape,
            "X_test_shape": X_test.shape,
            "accuracy": accuracy,
            "feature_names": iris.feature_names,
            "target_names": iris.target_names.tolist()
        }
    except Exception as e:
        logger.error(f"Failed to load demo data: {e}")
        return None


# Routes
@app.on_event("startup")
async def startup_event():
    """Load demo data on startup."""
    logger.info("Starting KNN service...")
    demo_info = load_demo_data()
    if demo_info:
        logger.info(f"Demo data loaded: {demo_info}")


@app.get("/", response_model=Dict)
async def root():
    """Root endpoint with service information."""
    return {
        "service": "TransparentML KNN Service",
        "version": "1.0.0",
        "description": "K-Nearest Neighbors for classification and regression",
        "algorithms": ["KNN Classifier", "KNN Regressor"],
        "endpoints": {
            "health": "/health",
            "train": "/api/v1/train",
            "predict": "/api/v1/predict",
            "demo_analysis": "/api/v1/demo/analyze",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="knn-service",
        timestamp=datetime.now().isoformat(),
        models_loaded=demo_data_loaded
    )


@app.post("/api/v1/train")
async def train_model(request: TrainRequest):
    """
    Train a KNN model (classifier or regressor).
    
    Returns training metrics and model info.
    """
    try:
        X = np.array(request.X)
        y = np.array(request.y)
        
        global classifier, regressor
        
        if request.task == "classification":
            classifier = KNNClassifier(
                n_neighbors=request.n_neighbors,
                metric=request.metric,
                weights=request.weights
            )
            classifier.fit(X, y)
            model = classifier
            model_type = "classifier"
        else:
            regressor = KNNRegressor(
                n_neighbors=request.n_neighbors,
                metric=request.metric,
                weights=request.weights
            )
            regressor.fit(X, y)
            model = regressor
            model_type = "regressor"
        
        logger.info(f"Trained {model_type} with {len(X)} samples")
        
        return {
            "status": "success",
            "model_type": model_type,
            "n_samples": len(X),
            "n_features": X.shape[1],
            "n_neighbors": request.n_neighbors,
            "metric": request.metric,
            "weights": request.weights,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/predict")
async def predict(request: PredictRequest):
    """
    Make predictions using trained KNN model.
    """
    global classifier, regressor
    
    try:
        X = np.array(request.X)
        
        if request.task == "classification":
            if classifier is None:
                raise HTTPException(
                    status_code=400,
                    detail="No classifier trained. Train a model first or use /demo/analyze"
                )
            
            predictions = classifier.predict(X).tolist()
            probabilities = classifier.predict_proba(X).tolist()
            
            return {
                "status": "success",
                "task": "classification",
                "predictions": predictions,
                "probabilities": probabilities,
                "n_samples": len(X),
                "timestamp": datetime.now().isoformat()
            }
        else:
            if regressor is None:
                raise HTTPException(
                    status_code=400,
                    detail="No regressor trained. Train a model first."
                )
            
            predictions = regressor.predict(X).tolist()
            
            return {
                "status": "success",
                "task": "regression",
                "predictions": predictions,
                "n_samples": len(X),
                "timestamp": datetime.now().isoformat()
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/demo/analyze")
async def demo_analysis(request: DemoAnalysisRequest):
    """
    Run a complete KNN analysis on demo data (Iris dataset).
    
    Returns training metrics, predictions, and visualizations data.
    """
    try:
        from sklearn.datasets import load_iris, make_classification
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, confusion_matrix
        
        # Load dataset
        if request.dataset == "iris":
            iris = load_iris()
            X, y = iris.data, iris.target
            feature_names = iris.feature_names
            target_names = iris.target_names.tolist()
        else:
            X, y = make_classification(
                n_samples=200, n_features=4, n_informative=3,
                n_redundant=1, n_classes=3, random_state=42
            )
            feature_names = [f"Feature {i+1}" for i in range(4)]
            target_names = ["Class 0", "Class 1", "Class 2"]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=request.test_size, random_state=42
        )
        
        # Train model
        knn = KNNClassifier(
            n_neighbors=request.n_neighbors,
            metric='euclidean',
            weights='uniform'
        )
        knn.fit(X_train, y_train)
        
        # Make predictions
        y_pred = knn.predict(X_test)
        y_proba = knn.predict_proba(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred).tolist()
        
        # Per-class metrics
        class_accuracies = []
        for i, class_name in enumerate(target_names):
            mask = y_test == i
            if mask.sum() > 0:
                class_acc = (y_pred[mask] == i).sum() / mask.sum()
                class_accuracies.append({
                    "class": class_name,
                    "accuracy": float(class_acc),
                    "samples": int(mask.sum())
                })
        
        logger.info(f"Demo analysis completed with {accuracy:.2%} accuracy")
        
        return {
            "status": "success",
            "dataset": request.dataset,
            "metrics": {
                "accuracy": float(accuracy),
                "n_train_samples": len(X_train),
                "n_test_samples": len(X_test),
                "n_neighbors": request.n_neighbors,
                "n_features": X.shape[1],
                "n_classes": len(target_names)
            },
            "confusion_matrix": conf_matrix,
            "class_metrics": class_accuracies,
            "feature_names": feature_names,
            "target_names": target_names,
            "predictions_sample": {
                "true_labels": y_test[:10].tolist(),
                "predicted_labels": y_pred[:10].tolist(),
                "probabilities": y_proba[:10].tolist()
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Demo analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
