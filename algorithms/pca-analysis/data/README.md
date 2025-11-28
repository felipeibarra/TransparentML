# data/ - Datos del Proyecto

## 📋 Descripción

Esta carpeta está destinada para almacenar datasets. Actualmente, el proyecto utiliza el **dataset Iris** que se carga directamente desde `sklearn.datasets`, por lo que no requiere archivos locales.

## 🌸 Dataset: Iris

### Origen
El dataset Iris es cargado automáticamente mediante:
```python
from sklearn.datasets import load_iris
iris = load_iris()
```

**Fuente original**: [UCI Machine Learning Repository - Iris Dataset](https://archive.ics.uci.edu/ml/datasets/iris)

### Historia
- **Introducido por**: Ronald A. Fisher (1936)
- **Paper original**: "The use of multiple measurements in taxonomic problems"
- **Uno de los datasets más famosos** en machine learning y estadística

## 📊 Características del Dataset

```
┌────────────────────────────────────────────────────────┐
│              Dataset Iris - Estructura                 │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Muestras: 150 (50 por cada especie)                  │
│  Features: 4 (medidas en cm)                           │
│  Clases: 3 (especies de flores)                       │
│  Tipo: Clasificación multiclase                       │
│                                                        │
│  ┌──────────────────────────────────────────┐         │
│  │  Features (X)                            │         │
│  │  ────────────────────────────────────    │         │
│  │  1. Sepal Length (cm)  [4.3 - 7.9]      │         │
│  │  2. Sepal Width  (cm)  [2.0 - 4.4]      │         │
│  │  3. Petal Length (cm)  [1.0 - 6.9]      │         │
│  │  4. Petal Width  (cm)  [0.1 - 2.5]      │         │
│  └──────────────────────────────────────────┘         │
│                                                        │
│  ┌──────────────────────────────────────────┐         │
│  │  Target (y)                              │         │
│  │  ────────────────────────────────────    │         │
│  │  0: Iris Setosa      (50 samples)       │         │
│  │  1: Iris Versicolor  (50 samples)       │         │
│  │  2: Iris Virginica   (50 samples)       │         │
│  └──────────────────────────────────────────┘         │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 🔬 Descripción de Features

### Anatomía de la Flor Iris
```
        ┌──────────┐
        │  Pétalo  │  ← Petal (interior, colorido)
        └──────────┘
    ┌────────────────┐
    │    Sépalo      │  ← Sepal (exterior, verde)
    └────────────────┘

    Petal Length ────►
    Petal Width  ────►
    Sepal Length ────►
    Sepal Width  ────►
```

### 1. Sepal Length (Longitud del Sépalo)
- **Rango**: 4.3 - 7.9 cm
- **Media**: 5.84 cm
- **Desviación**: 0.83 cm
- Parte externa de la flor que protege el pétalo

### 2. Sepal Width (Ancho del Sépalo)
- **Rango**: 2.0 - 4.4 cm
- **Media**: 3.06 cm
- **Desviación**: 0.44 cm
- Importante para distinguir especies

### 3. Petal Length (Longitud del Pétalo)
- **Rango**: 1.0 - 6.9 cm
- **Media**: 3.76 cm
- **Desviación**: 1.77 cm
- **Feature más discriminativa**

### 4. Petal Width (Ancho del Pétalo)
- **Rango**: 0.1 - 2.5 cm
- **Media**: 1.20 cm
- **Desviación**: 0.76 cm
- Alta correlación con Petal Length

## 🌺 Clases (Especies)

### Iris Setosa
```
┌──────────────────────────────┐
│    Iris Setosa               │
│    ──────────────            │
│    • Pétalos pequeños        │
│    • Fácilmente separable    │
│    • 50 muestras             │
│    • Clase: 0                │
└──────────────────────────────┘
```

### Iris Versicolor
```
┌──────────────────────────────┐
│    Iris Versicolor           │
│    ──────────────            │
│    • Tamaño intermedio       │
│    • Solapamiento moderado   │
│    • 50 muestras             │
│    • Clase: 1                │
└──────────────────────────────┘
```

### Iris Virginica
```
┌──────────────────────────────┐
│    Iris Virginica            │
│    ──────────────            │
│    • Pétalos grandes         │
│    • Similar a Versicolor    │
│    • 50 muestras             │
│    • Clase: 2                │
└──────────────────────────────┘
```

## 📈 Estadísticas por Clase

| Feature | Setosa | Versicolor | Virginica |
|---------|--------|------------|-----------|
| Sepal Length | 5.01 ± 0.35 | 5.94 ± 0.52 | 6.59 ± 0.64 |
| Sepal Width  | 3.43 ± 0.38 | 2.77 ± 0.31 | 2.97 ± 0.32 |
| Petal Length | 1.46 ± 0.17 | 4.26 ± 0.47 | 5.55 ± 0.55 |
| Petal Width  | 0.25 ± 0.11 | 1.33 ± 0.20 | 2.03 ± 0.27 |

## 🎯 Uso del Dataset en el Proyecto

### 1. Carga de Datos
```python
from src.data_loader import load_iris_data

X, y, feature_names, target_names = load_iris_data()
```

### 2. Preprocesamiento
```python
from src.data_loader import standardize_data

X_scaled, scaler = standardize_data(X)
```

### 3. Análisis PCA
```python
from src.pca_manual import PCAManual

pca = PCAManual(n_components=2)
X_pca = pca.fit_transform(X_scaled)
```

## 📊 Distribución de Datos

```
┌────────────────────────────────────────────────────┐
│      Distribución de Features                      │
│                                                    │
│  Sepal Length:  ▁▂▅▇█▇▅▃▂▁                         │
│  Sepal Width:   ▁▃▅▇█▇▅▂▁                          │
│  Petal Length:  █▃▁  ▁▃▅▇█                         │
│  Petal Width:   █▂   ▁▂▅▇█                         │
│                                                    │
│  Nota: Distribución bimodal en features de pétalo │
└────────────────────────────────────────────────────┘
```

## 🔗 Correlaciones

```
         sepal_l  sepal_w  petal_l  petal_w
sepal_l    1.00    -0.12     0.87     0.82
sepal_w   -0.12     1.00    -0.43    -0.37
petal_l    0.87    -0.43     1.00     0.96
petal_w    0.82    -0.37     0.96     1.00
```

**Observaciones**:
- Alta correlación entre medidas de pétalos (0.96)
- Baja/negativa correlación de sepal width con otras features
- Sugiere redundancia → ideal para PCA

## 💾 Estructura de Datos

### Formato en memoria
```python
# X: numpy array de shape (150, 4)
X = [[5.1, 3.5, 1.4, 0.2],  # Muestra 1
     [4.9, 3.0, 1.4, 0.2],  # Muestra 2
     ...
     [5.9, 3.0, 5.1, 1.8]]  # Muestra 150

# y: numpy array de shape (150,)
y = [0, 0, ..., 2, 2]  # 50 de cada clase
```

### Como DataFrame
```python
import pandas as pd
from src.data_loader import create_dataframe

df = create_dataframe(X, y, feature_names, target_names)

# Resultado:
#      sepal length  sepal width  petal length  petal width    species  target
# 0             5.1          3.5           1.4          0.2     setosa       0
# 1             4.9          3.0           1.4          0.2     setosa       0
# ...
```

## 🎓 ¿Por qué Iris para PCA?

### Ventajas
✅ **Pequeño**: 150 muestras, fácil de procesar
✅ **Conocido**: Benchmark estándar
✅ **4D → 2D**: Reducción visible y comprensible
✅ **Correlacionado**: Features redundantes, ideal para PCA
✅ **Separable**: Clases distinguibles después de PCA
✅ **Sin valores faltantes**: Limpio y completo

### Características ideales para PCA
- Features correlacionadas (redundancia)
- Diferentes escalas (requiere estandarización)
- Alta varianza en algunas dimensiones
- Resultados visualmente interpretables

## 📚 Referencias

1. **Paper Original**:
   Fisher, R.A. (1936). "The use of multiple measurements in taxonomic problems". 
   Annals of Eugenics, 7(2), 179-188.

2. **UCI ML Repository**:
   https://archive.ics.uci.edu/ml/datasets/iris

3. **Scikit-learn Docs**:
   https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html

## 🔄 Alternativas y Extensiones

### Usar datos propios
Si quieres usar tu propio dataset:

1. Coloca archivo CSV en esta carpeta:
```
data/
└── mi_dataset.csv
```

2. Modifica `src/data_loader.py`:
```python
def load_custom_data():
    df = pd.read_csv('data/mi_dataset.csv')
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    return X, y, feature_names, target_names
```

3. Actualiza scripts y notebooks para usar `load_custom_data()`

### Otros datasets de sklearn
```python
from sklearn.datasets import (
    load_wine,      # 13 features, 3 clases
    load_breast_cancer,  # 30 features, 2 clases
    load_digits,    # 64 features, 10 clases
)
```

## 🗂️ Organización Recomendada

Si agregas datasets propios:
```
data/
├── README.md           # Este archivo
├── raw/               # Datos originales sin procesar
│   └── dataset.csv
├── processed/         # Datos preprocesados
│   └── dataset_clean.csv
└── external/          # Datos de fuentes externas
    └── supplementary.csv
```

## 🔍 Exploración de Datos

Para explorar el dataset Iris:

```python
# En notebook o script
from src.data_loader import (
    load_iris_data, 
    get_data_statistics,
    get_correlation_matrix
)

X, y, features, targets = load_iris_data()

# Estadísticas
stats = get_data_statistics(X, features)
print(stats)

# Correlaciones
corr = get_correlation_matrix(X, features)
print(corr)
```

## 💡 Notas

- **No se requieren archivos locales** para este proyecto
- El dataset se descarga automáticamente con sklearn
- Si sklearn no está instalado, ejecuta: `pip install scikit-learn`
- La carpeta `data/` sirve como punto de expansión futura
