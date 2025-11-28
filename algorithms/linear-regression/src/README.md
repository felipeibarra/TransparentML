# 📁 src/ - Código Fuente

## 📋 Propósito
Módulos Python reutilizables que implementan la lógica de negocio del proyecto de Regresión Lineal sobre el dataset KDD Cup 1999.

---

## 🗂️ Estructura

```
src/
├── __init__.py           # Paquete Python (v1.0.0)
├── data_loader.py        # Carga y validación de datasets
├── preprocessing.py      # Limpieza y transformación
├── models.py             # Modelos de regresión lineal
├── evaluation.py         # Métricas y evaluación
└── utils.py              # Utilidades generales
```

---

## 🏗️ Flujo de Datos

```
┌──────────────┐
│  data/raw/   │ Dataset KDD Cup 1999
└──────┬───────┘
       │ data_loader.py
       ▼
┌──────────────┐
│  DataFrame   │ Pandas DataFrame
└──────┬───────┘
       │ preprocessing.py
       ▼
┌──────────────┐
│ X_train,test │ Features & Target
└──────┬───────┘
       │ models.py
       ▼
┌──────────────┐
│  Trained     │ Modelo entrenado
└──────┬───────┘
       │ evaluation.py
       ▼
┌──────────────┐
│  Metrics     │ → results/
└──────────────┘
```

---

## 📦 Módulos

### `data_loader.py`
Carga y valida el dataset KDD Cup 1999

### `preprocessing.py`
Limpieza, encoding, normalización, split

### `models.py`
Implementación de modelos de regresión lineal

### `evaluation.py`
Cálculo de métricas (R², MAE, RMSE, etc.)

### `utils.py`
Logging, guardado de archivos, utilidades

---

## 📝 Ejemplo de Uso

```python
from src.data_loader import load_kdd_data
from src.preprocessing import DataPreprocessor
from src.models import LinearRegressionModel
from src.evaluation import ModelEvaluator

# Cargar datos
df = load_kdd_data('data/raw/kddcup.data_10_percent')

# Preprocesar
prep = DataPreprocessor()
X_train, X_test, y_train, y_test = prep.prepare_data(df)

# Entrenar
model = LinearRegressionModel()
model.fit(X_train, y_train)

# Evaluar
evaluator = ModelEvaluator()
metrics = evaluator.evaluate(model, X_test, y_test)
```

---

## 🧪 Testing

```bash
make test  # Ejecutar tests EN CONTENEDOR
```

Ver `tests/` para más detalles.

---

## 🔗 Ver También

- **Scripts**: `scripts/train.py` usa estos módulos
- **Tests**: `tests/` para unit tests
- **Docs**: `docs/` para documentación detallada
