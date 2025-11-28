# src/ - Código Fuente del Proyecto

## 📋 Descripción

Esta carpeta contiene todos los módulos Python que implementan la funcionalidad core del análisis PCA. El código está organizado de manera modular para facilitar el mantenimiento y la reutilización.

## 🏗️ Arquitectura de Módulos

```
┌─────────────────────────────────────────────────────────────────┐
│                         PROYECTO PCA                            │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
                ▼               ▼               ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │ data_loader  │ │ pca_manual   │ │visualization │
        │              │ │              │ │              │
        │ • Carga Iris │ │ • PCA Manual │ │ • Gráficos   │
        │ • Estándar.  │ │ • Autovalor  │ │ • Heatmaps   │
        │ • Estadíst.  │ │ • Autovector │ │ • Biplots    │
        └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
               │                │                │
               └────────────────┼────────────────┘
                                │
                                ▼
                        ┌──────────────┐
                        │     api      │
                        │              │
                        │ • FastAPI    │
                        │ • Endpoints  │
                        │ • REST API   │
                        └──────────────┘
```

## 📦 Módulos

### `__init__.py`
Inicializa el paquete Python `src`.

**Función**: Permite importar módulos desde el directorio src como un paquete.

---

### `data_loader.py`
**Propósito**: Gestión de carga y preprocesamiento de datos

```
┌──────────────────────────────────────────┐
│         data_loader.py                   │
├──────────────────────────────────────────┤
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ load_iris_data()                   │ │
│  │ → Carga dataset Iris               │ │
│  │ → Retorna X, y, nombres            │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ standardize_data()                 │ │
│  │ → Normaliza: μ=0, σ=1              │ │
│  │ → Usa StandardScaler               │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ get_correlation_matrix()           │ │
│  │ → Calcula correlaciones            │ │
│  └────────────────────────────────────┘ │
│                                          │
└──────────────────────────────────────────┘
```

**Funciones principales**:
- `load_iris_data()`: Carga el dataset Iris desde sklearn
- `standardize_data()`: Estandariza features (media 0, desviación estándar 1)
- `create_dataframe()`: Convierte arrays NumPy a DataFrame de pandas
- `get_data_statistics()`: Calcula estadísticas descriptivas
- `get_correlation_matrix()`: Genera matriz de correlación

---

### `pca_manual.py`
**Propósito**: Implementación manual de PCA sin sklearn.PCA

```
┌──────────────────────────────────────────┐
│         pca_manual.py                    │
├──────────────────────────────────────────┤
│                                          │
│  Clase: PCAManual                        │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ fit(X)                             │ │
│  │ ├─ Centrar datos                   │ │
│  │ ├─ Calcular matriz covarianza      │ │
│  │ ├─ Calcular autovalores            │ │
│  │ ├─ Calcular autovectores           │ │
│  │ └─ Ordenar por varianza            │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ transform(X)                       │ │
│  │ → Proyecta datos a espacio PCA     │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ inverse_transform()                │ │
│  │ → Reconstruye datos originales     │ │
│  └────────────────────────────────────┘ │
│                                          │
└──────────────────────────────────────────┘
```

**Clase principal**: `PCAManual`

**Métodos clave**:
- `fit()`: Ajusta el modelo calculando autovalores y autovectores
- `transform()`: Proyecta datos al espacio de componentes principales
- `fit_transform()`: Combina fit y transform en una operación
- `inverse_transform()`: Reconstruye datos desde el espacio PCA
- `get_covariance_matrix()`: Retorna la matriz de covarianza
- `get_loadings()`: Calcula correlaciones entre variables y componentes

**Algoritmo**:
1. Centrar datos (restar media)
2. Calcular matriz de covarianza: `Cov(X) = (1/n-1) * X^T * X`
3. Calcular autovalores (λ) y autovectores (v): `Cov(X) * v = λ * v`
4. Ordenar por autovalores descendentes
5. Seleccionar k componentes principales
6. Proyectar datos: `X_pca = X_centered * V_k`

---

### `visualization.py`
**Propósito**: Generación de visualizaciones profesionales

```
┌──────────────────────────────────────────┐
│         visualization.py                 │
├──────────────────────────────────────────┤
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ plot_pca_scatter()                 │ │
│  │ → Scatter 2D de proyección PCA     │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ plot_variance_explained()          │ │
│  │ → Gráficos de varianza             │ │
│  │ → Individual + Acumulada           │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ plot_biplot()                      │ │
│  │ → Datos + vectores de features     │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ plot_correlation_heatmap()         │ │
│  │ → Heatmap de correlaciones         │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ plot_covariance_matrix()           │ │
│  │ → Heatmap de covarianza            │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ plot_comparison_manual_vs_sklearn()│ │
│  │ → Comparación lado a lado          │ │
│  └────────────────────────────────────┘ │
│                                          │
└──────────────────────────────────────────┘
```

**Funciones de visualización**:
- `plot_pca_scatter()`: Gráfico de dispersión 2D de datos proyectados
- `plot_variance_explained()`: Varianza explicada (individual y acumulada)
- `plot_biplot()`: Biplot con datos y vectores de features
- `plot_correlation_heatmap()`: Heatmap de correlación entre features
- `plot_covariance_matrix()`: Heatmap de matriz de covarianza
- `plot_comparison_manual_vs_sklearn()`: Comparación visual manual vs sklearn

**Características**:
- Estilo profesional con seaborn
- Configuración de colores y markers personalizados
- Exportación a PNG de alta calidad (300 DPI)
- Anotaciones y etiquetas claras

---

### `api.py`
**Propósito**: API REST con FastAPI para exponer análisis PCA

```
┌──────────────────────────────────────────┐
│             api.py                       │
├──────────────────────────────────────────┤
│                                          │
│  FastAPI Application                     │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ GET /health                        │ │
│  │ → Status del servicio              │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ GET /analysis                      │ │
│  │ → Resultados completos PCA         │ │
│  │ → Métricas, varianza, loadings     │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ POST /refresh                      │ │
│  │ → Reconstruye análisis             │ │
│  └────────────────────────────────────┘ │
│                                          │
└──────────────────────────────────────────┘
```

**Endpoints**:
- `GET /health`: Verifica estado del servicio
- `GET /analysis`: Retorna análisis completo en JSON
- `POST /refresh`: Regenera análisis y visualizaciones

**Funcionalidad**:
- Ejecuta análisis PCA al iniciar (startup event)
- Cachea resultados para respuestas rápidas
- Genera todas las visualizaciones
- Expone métricas y comparaciones

**Uso**:
```bash
# Iniciar servidor
uvicorn src.api:app --reload

# Consultar análisis
curl http://localhost:8000/analysis
```

## 🔄 Flujo de Datos

```
┌─────────────┐
│ Dataset Iris│
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  data_loader    │ ─────► Estandarización (μ=0, σ=1)
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│   pca_manual    │ ─────► Cálculo de autovalores/autovectores
└──────┬──────────┘        Proyección a 2D
       │
       ├──────────────────► Métricas: varianza explicada
       │
       ▼
┌─────────────────┐
│  visualization  │ ─────► Gráficos PNG (results/)
└─────────────────┘
       │
       ▼
┌─────────────────┐
│      api        │ ─────► REST API (JSON)
└─────────────────┘
```

## 📚 Dependencias

- **numpy**: Cálculos numéricos y álgebra lineal
- **pandas**: Manipulación de datos
- **scikit-learn**: Dataset Iris y comparación PCA
- **matplotlib**: Visualizaciones base
- **seaborn**: Visualizaciones estadísticas avanzadas
- **fastapi**: Framework API REST
- **typing**: Type hints para mejor documentación

## 🔗 Relaciones

- **Usado por**: `scripts/run_pca_analysis.py`, `notebooks/pca_analysis.ipynb`
- **Genera**: Archivos en `results/`
- **Importa datos**: Dataset Iris (sklearn)

## 💡 Notas de Implementación

### PCA Manual vs Sklearn
La implementación manual en `pca_manual.py` calcula explícitamente:
- Matriz de covarianza: `(X^T @ X) / (n-1)`
- Autovalores/autovectores: `np.linalg.eig()`

Esto difiere de sklearn que puede usar SVD para mayor eficiencia, pero ambos métodos son matemáticamente equivalentes.

### Estandarización
Es **crítico** estandarizar antes de PCA porque PCA es sensible a la escala de las variables. Sin estandarización, variables con mayor varianza dominarían los componentes principales.

### Visualizaciones
Todas las funciones de visualización aceptan parámetro `save_path` opcional para exportar gráficos de alta calidad (300 DPI).
