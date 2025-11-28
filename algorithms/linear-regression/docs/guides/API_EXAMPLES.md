# 📡 Ejemplos de Uso de la API

## Endpoints Disponibles

### 1. Health Check
```bash
curl http://localhost:8000/health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-11-27T20:00:00"
}
```

---

### 2. Información del Modelo
```bash
curl http://localhost:8000/model_info
```

**Respuesta:**
```json
{
  "model_type": "LinearRegression",
  "feature_names": ["duration", "src_bytes", "dst_bytes", ...],
  "has_scaler": true,
  "timestamp": "2024-11-27T20:00:00"
}
```

---

### 3. Predicción Individual

**Request:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [0, 181, 5450, 0, 0, 0, 0, 0, 0, 0]
  }'
```

**Respuesta:**
```json
{
  "prediction": 0.0234,
  "timestamp": "2024-11-27T20:00:00",
  "model_version": "1.0.0"
}
```

---

### 4. Predicción Batch

**Request:**
```bash
curl -X POST http://localhost:8000/batch_predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      [0, 181, 5450, 0, 0, 0, 0, 0, 0, 0],
      [0, 239, 486, 0, 0, 0, 0, 0, 0, 0],
      [0, 235, 1337, 0, 0, 0, 0, 0, 0, 0]
    ]
  }'
```

**Respuesta:**
```json
{
  "predictions": [0.0234, 0.0187, 0.0298],
  "count": 3,
  "timestamp": "2024-11-27T20:00:00"
}
```

---

### 5. Recargar Modelo

```bash
curl -X POST http://localhost:8000/reload_model
```

**Respuesta:**
```json
{
  "status": "success",
  "message": "Model reloaded"
}
```

---

### 6. Métricas Prometheus

```bash
curl http://localhost:8000/metrics
```

**Respuesta (formato Prometheus):**
```
# HELP predictions_total Total number of predictions
# TYPE predictions_total counter
predictions_total 156.0
# HELP prediction_latency_seconds Prediction latency
# TYPE prediction_latency_seconds histogram
prediction_latency_seconds_bucket{le="0.005"} 120.0
prediction_latency_seconds_bucket{le="0.01"} 145.0
...
```

---

## Ejemplos con Python

### Usando requests

```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"

# Health check
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Predicción individual
data = {
    "features": [0, 181, 5450, 0, 0, 0, 0, 0, 0, 0]
}
response = requests.post(f"{BASE_URL}/predict", json=data)
print(f"Predicción: {response.json()['prediction']}")

# Predicción batch
data = {
    "features": [
        [0, 181, 5450, 0, 0, 0, 0, 0, 0, 0],
        [0, 239, 486, 0, 0, 0, 0, 0, 0, 0]
    ]
}
response = requests.post(f"{BASE_URL}/batch_predict", json=data)
predictions = response.json()['predictions']
print(f"Predicciones: {predictions}")
```

### Cliente Python Completo

```python
import requests
from typing import List, Dict, Any

class MLClient:
    """Cliente para interactuar con la API de ML"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def health_check(self) -> Dict[str, Any]:
        """Verificar estado de la API"""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def predict(self, features: List[float]) -> float:
        """Realizar predicción individual"""
        data = {"features": features}
        response = requests.post(f"{self.base_url}/predict", json=data)
        response.raise_for_status()
        return response.json()['prediction']
    
    def batch_predict(self, features: List[List[float]]) -> List[float]:
        """Realizar predicciones batch"""
        data = {"features": features}
        response = requests.post(f"{self.base_url}/batch_predict", json=data)
        response.raise_for_status()
        return response.json()['predictions']
    
    def model_info(self) -> Dict[str, Any]:
        """Obtener información del modelo"""
        response = requests.get(f"{self.base_url}/model_info")
        response.raise_for_status()
        return response.json()
    
    def reload_model(self) -> Dict[str, str]:
        """Recargar modelo"""
        response = requests.post(f"{self.base_url}/reload_model")
        response.raise_for_status()
        return response.json()

# Uso
client = MLClient()

# Verificar que la API está funcionando
health = client.health_check()
print(f"API Status: {health['status']}")

# Hacer predicción
prediction = client.predict([0, 181, 5450, 0, 0, 0, 0, 0, 0, 0])
print(f"Predicción: {prediction}")

# Predicciones batch
predictions = client.batch_predict([
    [0, 181, 5450, 0, 0, 0, 0, 0, 0, 0],
    [0, 239, 486, 0, 0, 0, 0, 0, 0, 0]
])
print(f"Predicciones batch: {predictions}")
```

---

## Ejemplos con JavaScript/Node.js

```javascript
// Usando fetch (Node.js 18+ o con node-fetch)
const BASE_URL = 'http://localhost:8000';

// Health check
async function healthCheck() {
    const response = await fetch(`${BASE_URL}/health`);
    const data = await response.json();
    console.log(data);
}

// Predicción individual
async function predict(features) {
    const response = await fetch(`${BASE_URL}/predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ features })
    });
    const data = await response.json();
    return data.prediction;
}

// Predicción batch
async function batchPredict(featuresList) {
    const response = await fetch(`${BASE_URL}/batch_predict`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ features: featuresList })
    });
    const data = await response.json();
    return data.predictions;
}

// Uso
(async () => {
    await healthCheck();
    
    const prediction = await predict([0, 181, 5450, 0, 0, 0, 0, 0, 0, 0]);
    console.log('Predicción:', prediction);
    
    const predictions = await batchPredict([
        [0, 181, 5450, 0, 0, 0, 0, 0, 0, 0],
        [0, 239, 486, 0, 0, 0, 0, 0, 0, 0]
    ]);
    console.log('Predicciones batch:', predictions);
})();
```

---

## Testing con pytest

```python
import pytest
import requests

BASE_URL = "http://localhost:8000"

def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data['status'] in ['healthy', 'unhealthy']
    assert 'model_loaded' in data

def test_predict():
    data = {"features": [0, 181, 5450, 0, 0, 0, 0, 0, 0, 0]}
    response = requests.post(f"{BASE_URL}/predict", json=data)
    assert response.status_code == 200
    result = response.json()
    assert 'prediction' in result
    assert isinstance(result['prediction'], (int, float))

def test_batch_predict():
    data = {
        "features": [
            [0, 181, 5450, 0, 0, 0, 0, 0, 0, 0],
            [0, 239, 486, 0, 0, 0, 0, 0, 0, 0]
        ]
    }
    response = requests.post(f"{BASE_URL}/batch_predict", json=data)
    assert response.status_code == 200
    result = response.json()
    assert 'predictions' in result
    assert len(result['predictions']) == 2
    assert result['count'] == 2

def test_model_info():
    response = requests.get(f"{BASE_URL}/model_info")
    assert response.status_code == 200
    data = response.json()
    assert 'model_type' in data
```

---

## Documentación Interactiva

La API incluye documentación interactiva automática:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Estas interfaces permiten:
- Ver todos los endpoints disponibles
- Ver schemas de entrada/salida
- Probar requests directamente desde el navegador
- Ver ejemplos de uso

---

## Monitoreo y Observabilidad

### Métricas disponibles
- `predictions_total`: Total de predicciones realizadas
- `prediction_latency_seconds`: Latencia de predicciones
- `prediction_errors_total`: Total de errores

### Integrar con Prometheus

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'ml-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

---

## Manejo de Errores

### Error 503 - Modelo no cargado
```json
{
  "detail": "Model not loaded"
}
```

### Error 500 - Error en predicción
```json
{
  "detail": "Prediction failed: <error message>"
}
```

### Error 422 - Validación fallida
```json
{
  "detail": [
    {
      "loc": ["body", "features"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```
