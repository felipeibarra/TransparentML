# notebooks/ - Análisis Interactivo con Jupyter

## 📋 Descripción

Esta carpeta contiene Jupyter Notebooks para realizar análisis exploratorio y visualización interactiva del proyecto PCA. Los notebooks permiten ejecutar el código paso a paso, modificar parámetros en tiempo real y experimentar con el análisis.

## 📓 Notebooks Disponibles

### `pca_analysis.ipynb`
**Notebook principal de análisis PCA completo e interactivo**

## 🎯 Propósito

Los notebooks son ideales para:
- 📊 **Exploración visual**: Ver resultados inmediatamente
- 🔬 **Experimentación**: Modificar parámetros y observar efectos
- 📚 **Aprendizaje**: Entender PCA paso a paso
- 📝 **Documentación**: Combinar código, gráficos y explicaciones
- 🎓 **Presentaciones**: Mostrar resultados de forma interactiva

## 🏗️ Estructura del Notebook

```
┌─────────────────────────────────────────────────────────────┐
│              pca_analysis.ipynb                             │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Sección 1  │     │  Sección 2  │     │  Sección 3  │
│             │     │             │     │             │
│ Introducción│────▶│ Carga Datos │────▶│Preproceso   │
│ y Setup     │     │ Iris        │     │Estandarizar │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
        ┌──────────────────────────────────────┘
        │
        ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Sección 4  │     │  Sección 5  │     │  Sección 6  │
│             │     │             │     │             │
│   Análisis  │────▶│ PCA Manual  │────▶│Visualizacio │
│ Exploratorio│     │ Completo    │     │    nes      │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
        ┌──────────────────────────────────────┘
        │
        ▼
┌─────────────┐     ┌─────────────┐
│  Sección 7  │     │  Sección 8  │
│             │     │             │
│ Comparación │────▶│Conclusiones │
│ vs Sklearn  │     │             │
└─────────────┘     └─────────────┘
```

## 📋 Contenido del Notebook

### 1. Introducción y Setup
```
┌──────────────────────────────────┐
│ • Importar librerías             │
│ • Configurar matplotlib          │
│ • Definir constantes             │
└──────────────────────────────────┘
```

### 2. Carga de Datos
```
┌──────────────────────────────────┐
│ • load_iris_data()               │
│ • Mostrar dimensiones            │
│ • Preview de datos (head)        │
│ • Estadísticas descriptivas      │
└──────────────────────────────────┘
```

### 3. Preprocesamiento
```
┌──────────────────────────────────┐
│ • standardize_data()             │
│ • Verificar normalización        │
│ • Comparar antes/después         │
└──────────────────────────────────┘
```

### 4. Análisis Exploratorio
```
┌──────────────────────────────────┐
│ • Matriz de correlación          │
│ • Heatmap interactivo            │
│ • Distribuciones por feature     │
│ • Pairplot (opcional)            │
└──────────────────────────────────┘
```

### 5. PCA Manual
```
┌──────────────────────────────────┐
│ • Crear instancia PCAManual      │
│ • fit_transform()                │
│ • Mostrar autovalores            │
│ • Mostrar autovectores           │
│ • Varianza explicada             │
│ • Loadings                       │
└──────────────────────────────────┘
```

### 6. Visualizaciones
```
┌──────────────────────────────────┐
│ • Scatter 2D de proyección       │
│ • Gráfico de varianza explicada  │
│ • Varianza acumulada             │
│ • Biplot con vectores            │
│ • Matriz de covarianza           │
└──────────────────────────────────┘
```

### 7. Comparación con Sklearn
```
┌──────────────────────────────────┐
│ • PCA de sklearn                 │
│ • Comparar varianzas             │
│ • Comparar proyecciones          │
│ • Calcular diferencias           │
│ • Visualización lado a lado      │
└──────────────────────────────────┘
```

### 8. Conclusiones
```
┌──────────────────────────────────┐
│ • Resumen de resultados          │
│ • Interpretación de componentes  │
│ • Separabilidad de clases        │
│ • Recomendaciones                │
└──────────────────────────────────┘
```

## 🚀 Cómo Usar

### 1. Iniciar Jupyter Notebook

```bash
# Activar entorno virtual
source venv/bin/activate  # Windows: venv\Scripts\activate

# Iniciar Jupyter
jupyter notebook

# O Jupyter Lab (recomendado)
jupyter lab
```

El navegador se abrirá automáticamente en `http://localhost:8888`

### 2. Abrir el Notebook

Navega a: `notebooks/pca_analysis.ipynb`

### 3. Ejecutar Celdas

**Opciones**:
- `Shift + Enter`: Ejecutar celda actual y avanzar
- `Ctrl + Enter`: Ejecutar celda actual
- `Cell > Run All`: Ejecutar todas las celdas
- `Kernel > Restart & Run All`: Reiniciar y ejecutar todo

### 4. Experimentar

Modifica parámetros y re-ejecuta celdas:
```python
# Cambiar número de componentes
pca_manual = PCAManual(n_components=3)  # Probar con 3 componentes

# Cambiar dataset
# Cargar tu propio dataset y aplicar PCA
```

## 🎨 Ventajas del Notebook vs Script

| Característica | Notebook | Script |
|----------------|----------|--------|
| Interactividad | ✅ Alta | ❌ Baja |
| Visualización inline | ✅ Sí | ❌ No |
| Experimentación | ✅ Fácil | ⚠️ Requiere re-ejecutar |
| Documentación | ✅ Integrada | ❌ Separada |
| Producción | ❌ No recomendado | ✅ Ideal |
| Versionamiento | ⚠️ Complejo | ✅ Simple |
| Aprendizaje | ✅ Excelente | ⚠️ Menos intuitivo |

## 📦 Dependencias

Las mismas que el resto del proyecto:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

# Módulos propios
from src.pca_manual import PCAManual
from src.data_loader import load_iris_data, standardize_data
from src.visualization import plot_pca_scatter, plot_variance_explained
```

## 🔧 Configuración del Notebook

### Configuración de Matplotlib
```python
# Para gráficos inline
%matplotlib inline

# Para gráficos interactivos (opcional)
%matplotlib widget

# Configurar estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
```

### Auto-reload de módulos
```python
# Recargar módulos automáticamente al cambiarlos
%load_ext autoreload
%autoreload 2
```

### Ancho de salida
```python
# Hacer pandas más legible
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 100)
```

## 💡 Tips y Trucos

### 1. Ver ayuda de función
```python
# Dentro del notebook
?PCAManual
?PCAManual.fit

# O
help(PCAManual)
```

### 2. Timing de celdas
```python
%%time
# Código a cronometrar
pca_manual.fit_transform(X_scaled)
```

### 3. Guardar gráficos desde notebook
```python
fig, ax = plt.subplots(figsize=(10, 8))
# ... código de gráfico
plt.savefig('mi_grafico.png', dpi=300, bbox_inches='tight')
```

### 4. Exportar a otros formatos
```bash
# HTML
jupyter nbconvert --to html pca_analysis.ipynb

# PDF (requiere LaTeX)
jupyter nbconvert --to pdf pca_analysis.ipynb

# Python script
jupyter nbconvert --to script pca_analysis.ipynb
```

## 🎓 Casos de Uso

### Para estudiantes
- Aprender PCA paso a paso
- Experimentar con parámetros
- Visualizar conceptos en tiempo real

### Para investigadores
- Análisis exploratorio rápido
- Prototipar ideas
- Documentar experimentos

### Para presentaciones
- Demostrar resultados interactivamente
- Combinar código, gráficos y narrativa
- Exportar a HTML para compartir

## 🔗 Relaciones

- **Importa desde**: `src/`
- **Alternativa no-interactiva**: `scripts/run_pca_analysis.py`
- **Resultados**: Pueden guardarse en `results/` manualmente

## 📝 Estructura de Celdas Recomendada

```python
# CELDA 1: Imports
import numpy as np
...

# CELDA 2: Configuración
%matplotlib inline
plt.style.use('seaborn-v0_8-darkgrid')

# CELDA 3: Cargar datos
X, y, feature_names, target_names = load_iris_data()

# CELDA 4: Preprocesar
X_scaled, scaler = standardize_data(X)

# CELDA 5: PCA
pca = PCAManual(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# CELDA 6: Visualizar
plot_pca_scatter(X_pca, y, target_names)

# ... más celdas según necesidad
```

## ⚙️ Shortcuts Útiles

- `a`: Insertar celda arriba
- `b`: Insertar celda abajo
- `dd`: Eliminar celda
- `m`: Cambiar a Markdown
- `y`: Cambiar a Código
- `Shift + M`: Fusionar celdas
- `Ctrl + Shift + -`: Dividir celda

## 🐛 Troubleshooting

### Kernel no encuentra módulos de `src/`
```python
import sys
sys.path.insert(0, '..')
```

### Gráficos no aparecen
```python
%matplotlib inline
plt.show()
```

### Notebook muy lento
- Reiniciar kernel: `Kernel > Restart`
- Limpiar outputs: `Cell > All Output > Clear`

## 📚 Recursos Adicionales

- [Jupyter Documentation](https://jupyter.org/documentation)
- [Jupyter Notebook Tips](https://www.dataquest.io/blog/jupyter-notebook-tips-tricks-shortcuts/)
- [Markdown Guide](https://www.markdownguide.org/)
