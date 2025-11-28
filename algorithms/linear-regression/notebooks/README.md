# 📁 notebooks/ - Análisis Interactivo

## 📋 Propósito
Notebooks Jupyter para análisis exploratorio, experimentación y visualización interactiva.

---

## 🗂️ Estructura Sugerida

```
notebooks/
├── 01_exploratory_analysis.ipynb    # EDA del dataset
├── 02_preprocessing.ipynb           # Experimentos de preprocesamiento
├── 03_model_training.ipynb          # Entrenamiento de modelos
├── 04_evaluation.ipynb              # Evaluación y comparación
└── 05_visualizations.ipynb          # Visualizaciones avanzadas
```

---

## 🔄 Workflow

```
JupyterLab (http://localhost:8888)
    │
    ├─> 01_exploratory_analysis.ipynb
    │       │ Cargar datos
    │       │ Estadísticas descriptivas
    │       │ Visualizaciones
    │       ▼
    │   Insights sobre datos
    │
    ├─> 02_preprocessing.ipynb
    │       │ Probar transformaciones
    │       │ Experimentar con encoding
    │       ▼
    │   Pipeline de preprocesamiento
    │
    ├─> 03_model_training.ipynb
    │       │ Entrenar modelos
    │       │ Ajustar hiperparámetros
    │       ▼
    │   Mejor configuración
    │
    └─> 04_evaluation.ipynb
            │ Evaluar modelos
            │ Comparar métricas
            ▼
        Modelo final
```

---

## 🚀 Iniciar JupyterLab

### En contenedor (recomendado)
```bash
# Iniciar servicios
make up

# Acceder a JupyterLab
open http://localhost:8888
```

### Ver logs
```bash
docker-compose logs -f jupyter-lab
```

---

## 📝 Template de Notebook

```python
# ===== SETUP =====
import sys
sys.path.append('/app')  # Para imports de src/

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_loader import load_kdd_data
from src.preprocessing import DataPreprocessor
from src.models import LinearRegressionModel

# Configuración
%matplotlib inline
sns.set_style('whitegrid')
pd.set_option('display.max_columns', None)

# ===== ANÁLISIS =====
# Tu código aquí...
```

---

## 🎯 Notebooks Recomendados

### 1. Exploratory Data Analysis (EDA)
```python
# 01_exploratory_analysis.ipynb

- Cargar dataset KDD Cup 1999
- Dimensiones y tipos de datos
- Valores nulos y duplicados
- Distribuciones de variables
- Correlaciones
- Outliers
```

### 2. Preprocessing
```python
# 02_preprocessing.ipynb

- Probar diferentes encodings
- Comparar métodos de normalización
- Selección de features
- Manejo de outliers
```

### 3. Model Training
```python
# 03_model_training.ipynb

- Entrenar LinearRegression
- Entrenar Ridge con diferentes alphas
- Entrenar Lasso
- Grid search para hiperparámetros
```

### 4. Evaluation
```python
# 04_evaluation.ipynb

- Calcular métricas (R², MAE, RMSE)
- Análisis de residuos
- Curvas de aprendizaje
- Comparación de modelos
```

---

## 💾 Guardar Trabajo

### Guardar notebook
JupyterLab guarda automáticamente, pero también:
- `Ctrl+S` para guardar manual
- `File → Save Notebook`

### Exportar a Python
```bash
# Dentro del contenedor
jupyter nbconvert --to script notebook.ipynb
```

### Exportar a HTML
```bash
jupyter nbconvert --to html notebook.ipynb
```

---

## 🐳 Acceso a Datos

Los notebooks tienen acceso a:

```
/app/data/          # Datasets
/app/src/           # Módulos Python
/app/results/       # Resultados
/app/models/        # Modelos guardados
```

Cambios en archivos se sincronizan con tu Mac.

---

## 🔧 Instalar Paquetes Adicionales

### Temporal (solo en sesión actual)
```python
!pip install package_name
```

### Permanente
1. Editar `requirements.txt` en tu Mac
2. Reconstruir imagen:
```bash
make build
make restart
```

---

## 📊 Visualizaciones

### Matplotlib
```python
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.title('Mi Gráfico')
plt.show()
```

### Seaborn
```python
import seaborn as sns

sns.scatterplot(data=df, x='feature1', y='feature2')
plt.show()
```

### Plotly (interactivo)
```python
import plotly.express as px

fig = px.scatter(df, x='feature1', y='feature2')
fig.show()
```

---

## 🧪 Experimentación

Notebooks son perfectos para:

- ✅ Exploración rápida de datos
- ✅ Prototipado de transformaciones
- ✅ Visualización interactiva
- ✅ Debugging de pipelines
- ✅ Documentación de análisis

**Pero NO para**:
- ❌ Código de producción
- ❌ Scripts automatizados
- ❌ Pipelines reproducibles

**Regla**: Experimenta en notebooks, implementa en `src/`.

---

## 🔗 Ver También
- `src/` - Módulos Python
- `data/` - Datasets
- `DOCKER_WORKFLOW.md` - Workflows con contenedores
