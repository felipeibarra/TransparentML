# 📁 tests/ - Tests Unitarios

## 📋 Propósito
Tests automatizados para garantizar la calidad y correctitud del código.

---

## 🗂️ Estructura

```
tests/
├── __init__.py
├── test_data_loader.py       # Tests de carga de datos
├── test_preprocessing.py     # Tests de preprocesamiento
├── test_models.py            # Tests de modelos
├── test_evaluation.py        # Tests de evaluación
└── test_utils.py             # Tests de utilidades
```

---

## 🔄 Flujo de Testing

```
make test
    │
    ▼
docker-compose exec training-service
    │
    ▼
pytest tests/ -v
    │
    ├─> test_data_loader.py
    ├─> test_preprocessing.py
    ├─> test_models.py
    ├─> test_evaluation.py
    └─> test_utils.py
        │
        ▼
    Reporte de resultados
```

---

## 🧪 Ejecutar Tests

### Todos los tests
```bash
make test  # En contenedor
```

### Tests específicos
```bash
# En contenedor
docker-compose exec training-service pytest tests/test_models.py -v
```

### Con cobertura
```bash
make test-cov
```

### Tests individuales
```bash
docker-compose exec training-service pytest tests/test_models.py::test_linear_regression_fit -v
```

---

## 📝 Estructura de Test

```python
# tests/test_models.py

import pytest
import numpy as np
from src.models import LinearRegressionModel

class TestLinearRegressionModel:
    """Tests para LinearRegressionModel."""
    
    @pytest.fixture
    def sample_data(self):
        """Fixture con datos de ejemplo."""
        X = np.random.rand(100, 10)
        y = np.random.rand(100)
        return X, y
    
    def test_model_initialization(self):
        """Test: modelo se inicializa correctamente."""
        model = LinearRegressionModel()
        assert model is not None
    
    def test_model_fit(self, sample_data):
        """Test: modelo entrena sin errores."""
        X, y = sample_data
        model = LinearRegressionModel()
        model.fit(X, y)
        assert model.is_fitted()
    
    def test_model_predict(self, sample_data):
        """Test: predicciones tienen forma correcta."""
        X, y = sample_data
        model = LinearRegressionModel()
        model.fit(X, y)
        predictions = model.predict(X)
        assert predictions.shape == y.shape
```

---

## 🎯 Tipos de Tests

### 1. Tests Unitarios
Testear funciones/clases individuales

```python
def test_load_kdd_data():
    """Test: cargar dataset KDD."""
    df = load_kdd_data('data/raw/kddcup.data_10_percent')
    assert df is not None
    assert len(df) > 0
```

### 2. Tests de Integración
Testear múltiples componentes juntos

```python
def test_full_pipeline():
    """Test: pipeline completo."""
    # Cargar
    df = load_kdd_data('data/raw/test_sample.csv')
    # Preprocesar
    prep = DataPreprocessor()
    X_train, X_test, y_train, y_test = prep.prepare_data(df)
    # Entrenar
    model = LinearRegressionModel()
    model.fit(X_train, y_train)
    # Predecir
    predictions = model.predict(X_test)
    assert len(predictions) == len(y_test)
```

### 3. Tests de Regresión
Asegurar que cambios no rompan funcionalidad existente

```python
def test_model_output_consistency():
    """Test: modelo produce mismos resultados con mismos datos."""
    np.random.seed(42)
    X = np.random.rand(50, 10)
    y = np.random.rand(50)
    
    model1 = LinearRegressionModel()
    model1.fit(X, y)
    pred1 = model1.predict(X)
    
    model2 = LinearRegressionModel()
    model2.fit(X, y)
    pred2 = model2.predict(X)
    
    np.testing.assert_array_almost_equal(pred1, pred2)
```

---

## 🔧 Fixtures y Utilidades

### Fixtures
```python
@pytest.fixture
def sample_dataset():
    """Dataset de muestra para tests."""
    return pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [2, 4, 6, 8, 10],
        'target': [1.5, 3.5, 5.5, 7.5, 9.5]
    })

@pytest.fixture
def trained_model(sample_dataset):
    """Modelo pre-entrenado."""
    X = sample_dataset[['feature1', 'feature2']]
    y = sample_dataset['target']
    model = LinearRegressionModel()
    model.fit(X, y)
    return model
```

### Parametrización
```python
@pytest.mark.parametrize("alpha,expected_score", [
    (0.1, 0.85),
    (1.0, 0.87),
    (10.0, 0.83)
])
def test_ridge_with_different_alphas(alpha, expected_score):
    """Test Ridge con diferentes valores de alpha."""
    model = RidgeModel(alpha=alpha)
    # ... test logic
```

---

## 📊 Cobertura

### Ver reporte de cobertura
```bash
make test-cov
```

### Generar reporte HTML
```bash
docker-compose exec training-service \
    pytest tests/ --cov=src --cov-report=html

# Ver reporte
open htmlcov/index.html
```

---

## ✅ Buenas Prácticas

- ✅ Un test, una función
- ✅ Tests independientes (no dependen de orden)
- ✅ Usar fixtures para setup
- ✅ Nombres descriptivos: `test_<what>_<condition>_<expected>`
- ✅ Docstrings en cada test
- ✅ Mantener tests simples y legibles
- ✅ Testear edge cases y errores
- ✅ Aim for >80% coverage

---

## 🐛 Debugging Tests

### Ejecutar con output detallado
```bash
docker-compose exec training-service \
    pytest tests/test_models.py -v -s
```

### Detener en primer fallo
```bash
pytest tests/ -x
```

### Ejecutar último test fallido
```bash
pytest --lf
```

### Debugger interactivo
```bash
pytest tests/test_models.py --pdb
```

---

## 🔗 Ver También
- `src/` - Código a testear
- `pytest` docs - https://docs.pytest.org/
- `DOCKER_WORKFLOW.md` - Workflows con contenedores
