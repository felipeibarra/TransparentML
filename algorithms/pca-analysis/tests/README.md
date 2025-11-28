# tests/ - Tests Unitarios y de Integración

## 📋 Descripción

Esta carpeta contiene tests automáticos para validar la correctitud de la implementación PCA y garantizar que el código funciona como se espera. Los tests siguen las mejores prácticas de testing en Python usando `pytest`.

## 🎯 Propósito de los Tests

```
┌────────────────────────────────────────────────────┐
│              ¿Por qué hacer tests?                 │
├────────────────────────────────────────────────────┤
│                                                    │
│  ✅ Verificar correctitud de implementación        │
│  ✅ Detectar bugs antes de producción              │
│  ✅ Facilitar refactoring seguro                   │
│  ✅ Documentar comportamiento esperado             │
│  ✅ Garantizar calidad del código                  │
│                                                    │
└────────────────────────────────────────────────────┘
```

## 🗂️ Estructura de Tests

```
tests/
├── README.md                      # Este archivo
├── __init__.py                    # Inicializador del paquete
├── test_data_loader.py            # Tests de carga de datos
├── test_pca_manual.py             # Tests de PCA manual
├── test_visualization.py          # Tests de visualizaciones
├── test_integration.py            # Tests de integración
└── conftest.py                    # Fixtures compartidas
```

## 🧪 Tipos de Tests

### 1. Tests Unitarios
**Objetivo**: Probar funciones/métodos individuales aisladamente

```python
# test_data_loader.py
def test_load_iris_data():
    """Test que load_iris_data retorna datos correctos"""
    X, y, features, targets = load_iris_data()
    
    assert X.shape == (150, 4)
    assert y.shape == (150,)
    assert len(features) == 4
    assert len(targets) == 3
```

### 2. Tests de Integración
**Objetivo**: Probar que los módulos funcionan juntos correctamente

```python
# test_integration.py
def test_full_pca_pipeline():
    """Test del pipeline completo de PCA"""
    # Cargar datos
    X, y, features, targets = load_iris_data()
    
    # Estandarizar
    X_scaled, _ = standardize_data(X)
    
    # Aplicar PCA
    pca = PCAManual(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    # Verificar resultado
    assert X_pca.shape == (150, 2)
    assert pca.explained_variance_ratio_.sum() > 0.9
```

### 3. Tests de Validación
**Objetivo**: Comparar con implementaciones de referencia (sklearn)

```python
# test_pca_manual.py
def test_pca_vs_sklearn():
    """Test que PCA manual coincide con sklearn"""
    from sklearn.decomposition import PCA
    
    X_scaled, _ = standardize_data(X)
    
    # PCA manual
    pca_manual = PCAManual(n_components=2)
    X_manual = pca_manual.fit_transform(X_scaled)
    
    # PCA sklearn
    pca_sklearn = PCA(n_components=2)
    X_sklearn = pca_sklearn.fit_transform(X_scaled)
    
    # Comparar (permitir diferencias por signo)
    diff = np.abs(np.abs(X_manual) - np.abs(X_sklearn))
    assert np.all(diff < 1e-6)
```

## 📊 Diagrama de Testing

```
┌─────────────────────────────────────────────────────┐
│              Pipeline de Testing                    │
└─────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Unit Tests │ │Integration   │ │ Validation   │
│              │ │   Tests      │ │   Tests      │
│ • data_loader│ │ • Pipeline   │ │ • vs sklearn │
│ • pca_manual │ │ • E2E flows  │ │ • Benchmarks │
│ • visualiz.  │ │ • API        │ │ • Edge cases │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
                   ✅ All Passed
                        │
                        ▼
                  Code Ready ✨
```

## 🚀 Ejecutar Tests

### Instalar pytest
```bash
pip install pytest pytest-cov
```

### Ejecutar todos los tests
```bash
# Desde la raíz del proyecto
pytest tests/

# Con verbose
pytest tests/ -v

# Con coverage
pytest tests/ --cov=src --cov-report=html
```

### Ejecutar tests específicos
```bash
# Un archivo
pytest tests/test_pca_manual.py

# Una función específica
pytest tests/test_pca_manual.py::test_pca_fit

# Por marca/tag
pytest tests/ -m unit
```

### Ejecutar con output detallado
```bash
# Mostrar print statements
pytest tests/ -s

# Mostrar locals en fallos
pytest tests/ -l

# Modo interactivo en fallo
pytest tests/ --pdb
```

## 📝 Ejemplo: test_pca_manual.py

```python
"""
Tests para la implementación manual de PCA
"""
import pytest
import numpy as np
from sklearn.decomposition import PCA

from src.pca_manual import PCAManual
from src.data_loader import load_iris_data, standardize_data


class TestPCAManual:
    """Suite de tests para PCAManual"""
    
    @pytest.fixture
    def iris_scaled(self):
        """Fixture: dataset Iris estandarizado"""
        X, y, _, _ = load_iris_data()
        X_scaled, _ = standardize_data(X)
        return X_scaled, y
    
    def test_pca_initialization(self):
        """Test que PCA se inicializa correctamente"""
        pca = PCAManual(n_components=2)
        
        assert pca.n_components == 2
        assert pca.components_ is None
        assert pca.explained_variance_ is None
    
    def test_pca_fit(self, iris_scaled):
        """Test que fit calcula componentes correctamente"""
        X_scaled, _ = iris_scaled
        pca = PCAManual(n_components=2)
        
        pca.fit(X_scaled)
        
        # Verificar que se calcularon los atributos
        assert pca.components_ is not None
        assert pca.explained_variance_ is not None
        assert pca.eigenvalues_ is not None
        
        # Verificar dimensiones
        assert pca.components_.shape == (2, 4)
        assert len(pca.explained_variance_) == 2
    
    def test_pca_transform(self, iris_scaled):
        """Test que transform proyecta datos correctamente"""
        X_scaled, _ = iris_scaled
        pca = PCAManual(n_components=2)
        
        pca.fit(X_scaled)
        X_transformed = pca.transform(X_scaled)
        
        # Verificar dimensiones
        assert X_transformed.shape == (150, 2)
    
    def test_pca_fit_transform(self, iris_scaled):
        """Test que fit_transform funciona"""
        X_scaled, _ = iris_scaled
        pca = PCAManual(n_components=2)
        
        X_transformed = pca.fit_transform(X_scaled)
        
        assert X_transformed.shape == (150, 2)
        assert pca.components_ is not None
    
    def test_variance_explained_sum(self, iris_scaled):
        """Test que varianza explicada suma <= 1"""
        X_scaled, _ = iris_scaled
        pca = PCAManual(n_components=4)
        
        pca.fit(X_scaled)
        
        total_var = np.sum(pca.explained_variance_ratio_)
        assert 0 < total_var <= 1.0
    
    def test_components_orthogonal(self, iris_scaled):
        """Test que componentes son ortogonales"""
        X_scaled, _ = iris_scaled
        pca = PCAManual(n_components=2)
        
        pca.fit(X_scaled)
        
        # Producto punto debe ser ~0
        dot_product = np.dot(pca.components_[0], pca.components_[1])
        assert abs(dot_product) < 1e-10
    
    def test_pca_vs_sklearn(self, iris_scaled):
        """Test que PCA manual coincide con sklearn"""
        X_scaled, _ = iris_scaled
        
        # PCA manual
        pca_manual = PCAManual(n_components=2)
        pca_manual.fit(X_scaled)
        var_manual = pca_manual.explained_variance_ratio_
        
        # PCA sklearn
        pca_sklearn = PCA(n_components=2)
        pca_sklearn.fit(X_scaled)
        var_sklearn = pca_sklearn.explained_variance_ratio_
        
        # Comparar varianzas
        np.testing.assert_array_almost_equal(
            var_manual, var_sklearn, decimal=6
        )
    
    def test_inverse_transform(self, iris_scaled):
        """Test que inverse_transform reconstruye datos"""
        X_scaled, _ = iris_scaled
        pca = PCAManual(n_components=2)
        
        X_pca = pca.fit_transform(X_scaled)
        X_reconstructed = pca.inverse_transform(X_pca)
        
        # Verificar dimensiones
        assert X_reconstructed.shape == X_scaled.shape
        
        # Error de reconstrucción debe ser pequeño
        mse = np.mean((X_scaled - X_reconstructed) ** 2)
        assert mse < 0.5  # Pérdida esperada con 2 componentes


def test_pca_edge_cases():
    """Test casos límite de PCA"""
    # Caso: n_components > n_features
    X = np.random.randn(10, 3)
    pca = PCAManual(n_components=5)
    
    with pytest.raises(Exception):
        pca.fit(X)
```

## 📝 Ejemplo: test_data_loader.py

```python
"""
Tests para módulo de carga de datos
"""
import pytest
import numpy as np
import pandas as pd

from src.data_loader import (
    load_iris_data,
    standardize_data,
    create_dataframe,
    get_data_statistics,
    get_correlation_matrix
)


def test_load_iris_data():
    """Test carga correcta del dataset Iris"""
    X, y, features, targets = load_iris_data()
    
    # Verificar dimensiones
    assert X.shape == (150, 4)
    assert y.shape == (150,)
    
    # Verificar tipos
    assert isinstance(X, np.ndarray)
    assert isinstance(y, np.ndarray)
    
    # Verificar nombres
    assert len(features) == 4
    assert len(targets) == 3
    assert 'sepal' in features[0].lower()


def test_standardize_data():
    """Test estandarización de datos"""
    X, _, _, _ = load_iris_data()
    X_scaled, scaler = standardize_data(X)
    
    # Verificar forma
    assert X_scaled.shape == X.shape
    
    # Verificar media ~0 y std ~1
    assert np.allclose(np.mean(X_scaled, axis=0), 0, atol=1e-10)
    assert np.allclose(np.std(X_scaled, axis=0), 1, atol=1e-10)


def test_create_dataframe():
    """Test creación de DataFrame"""
    X, y, features, targets = load_iris_data()
    df = create_dataframe(X, y, features, targets)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 150
    assert 'species' in df.columns
    assert 'target' in df.columns


def test_get_data_statistics():
    """Test estadísticas descriptivas"""
    X, _, features, _ = load_iris_data()
    stats = get_data_statistics(X, features)
    
    assert isinstance(stats, pd.DataFrame)
    assert 'mean' in stats.index
    assert 'std' in stats.index
    assert stats.shape[1] == 4


def test_get_correlation_matrix():
    """Test matriz de correlación"""
    X, _, features, _ = load_iris_data()
    corr = get_correlation_matrix(X, features)
    
    assert isinstance(corr, pd.DataFrame)
    assert corr.shape == (4, 4)
    
    # Diagonal debe ser 1
    assert np.allclose(np.diag(corr), 1.0)
    
    # Matriz simétrica
    assert np.allclose(corr, corr.T)
```

## 🔧 Configuración: conftest.py

```python
"""
Fixtures compartidas para todos los tests
"""
import pytest
import numpy as np

from src.data_loader import load_iris_data, standardize_data
from src.pca_manual import PCAManual


@pytest.fixture(scope="session")
def iris_data():
    """Fixture: dataset Iris crudo"""
    return load_iris_data()


@pytest.fixture(scope="session")
def iris_scaled():
    """Fixture: dataset Iris estandarizado"""
    X, y, features, targets = load_iris_data()
    X_scaled, scaler = standardize_data(X)
    return X_scaled, y, features, targets, scaler


@pytest.fixture
def pca_fitted(iris_scaled):
    """Fixture: PCA ya ajustado"""
    X_scaled, _, _, _, _ = iris_scaled
    pca = PCAManual(n_components=2)
    pca.fit(X_scaled)
    return pca


@pytest.fixture
def sample_data():
    """Fixture: datos de ejemplo simples"""
    np.random.seed(42)
    X = np.random.randn(100, 5)
    y = np.random.randint(0, 3, 100)
    return X, y
```

## ✅ Coverage (Cobertura de Tests)

### Generar reporte de coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

Abre `htmlcov/index.html` en el navegador para ver reporte detallado.

### Objetivo de cobertura
- **Target**: > 80% de cobertura
- **Crítico**: 100% en `pca_manual.py`
- **Nice to have**: > 90% global

## 🐛 Debugging Tests

### Test falla
```bash
# Ver traceback completo
pytest tests/ --tb=long

# Entrar en debugger
pytest tests/ --pdb

# Ver variables locales
pytest tests/ -l
```

### Test lento
```bash
# Mostrar duración de tests
pytest tests/ --durations=10
```

## 📋 Best Practices

### 1. Naming
```python
# ✅ Buenos nombres
def test_pca_calculates_eigenvalues():
    ...

def test_standardize_data_returns_zero_mean():
    ...

# ❌ Malos nombres
def test_1():
    ...

def test_thing():
    ...
```

### 2. Assertions
```python
# ✅ Usar numpy testing para arrays
np.testing.assert_array_almost_equal(a, b, decimal=6)

# ✅ Mensajes descriptivos
assert x > 0, f"Expected positive value, got {x}"

# ❌ Comparar floats con ==
assert 0.1 + 0.2 == 0.3  # ¡Puede fallar!
```

### 3. Fixtures
```python
# ✅ Reusar fixtures
@pytest.fixture
def expensive_setup():
    # Setup costoso
    return data

# ✅ Scope apropiado
@pytest.fixture(scope="session")  # Una vez por sesión
@pytest.fixture(scope="function")  # Por defecto, cada test
```

## 🔗 Relaciones

- **Prueba**: Módulos en `src/`
- **Usa**: Fixtures en `conftest.py`
- **Ejecutado por**: CI/CD pipeline (future)

## 📚 Recursos

- [pytest Documentation](https://docs.pytest.org/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Effective Python Testing](https://realpython.com/pytest-python-testing/)

## 💡 Próximos Pasos

- [ ] Implementar tests unitarios completos
- [ ] Agregar tests de visualización (difícil, requiere comparación de imágenes)
- [ ] Configurar CI/CD para ejecutar tests automáticamente
- [ ] Agregar tests de performance/benchmarking
- [ ] Parametrizar tests para múltiples datasets

## 🎯 Ejecutar Tests Ahora

```bash
# Crear un test básico de ejemplo
cd tests/
python -m pytest -v
```
