# Tarea 2: Reducción de Dimensionalidad con PCA

## Máster en IA Aplicada a la Ciberseguridad
### Módulo 2: Fundamentos de Machine Learning

---

## 📋 Descripción

Este proyecto implementa **PCA (Principal Component Analysis)** desde cero para reducción de dimensionalidad, calculando manualmente autovalores y autovectores de la matriz de covarianza. Se aplica al dataset Iris (4 características → 2 dimensiones) con análisis completo de varianza explicada y visualizaciones profesionales.

## 🎯 Objetivos

1. **Comprender PCA**: Reducir dimensionalidad manteniendo máxima varianza
2. **Implementar desde cero**: Calcular autovalores/autovectores sin usar `sklearn.PCA`
3. **Visualizar y analizar**: Graficar datos reducidos y analizar varianza explicada

## 🗂️ Estructura del Proyecto

```
TAREA_2/
├── README.md                           # Este archivo
├── requirements.txt                    # Dependencias Python
├── Dockerfile                          # Containerización
├── .gitignore                          # Archivos a ignorar
│
├── src/                                # Código fuente
│   ├── README.md                       # 📘 Documentación de módulos
│   ├── __init__.py
│   ├── pca_manual.py                   # Implementación manual de PCA
│   ├── data_loader.py                  # Carga y preprocesamiento
│   ├── visualization.py                # Visualizaciones profesionales
│   └── api.py                          # API REST con FastAPI
│
├── scripts/                            # Scripts ejecutables
│   ├── README.md                       # 📘 Guía de ejecución
│   └── run_pca_analysis.py             # Script principal de análisis
│
├── notebooks/                          # Jupyter Notebooks
│   ├── README.md                       # 📘 Guía de uso interactivo
│   └── pca_analysis.ipynb              # Análisis interactivo completo
│
├── results/                            # Resultados generados
│   ├── README.md                       # 📘 Descripción de visualizaciones
│   ├── correlation_matrix.png
│   ├── covariance_matrix.png
│   ├── pca_scatter_2d.png
│   ├── variance_explained.png
│   ├── biplot.png
│   └── comparison_manual_sklearn.png
│
├── data/                               # Datos (Iris desde sklearn)
│   └── README.md                       # 📘 Información del dataset
│
├── docs/                               # Documentación académica
│   ├── README.md                       # 📘 Índice de documentación
│   ├── README_TAREA2.MD                # Contexto y requisitos
│   ├── README_COMPLEMENTO_TAREA2.MD    # Información complementaria
│   └── RESULTADOS.md                   # Análisis detallado de resultados
│
└── tests/                              # Tests unitarios
    └── README.md                       # 📘 Guía de testing

```

💡 **Nota**: Cada carpeta contiene un README.md con diagramas ASCII explicando su función y contenido.

## 🚀 Instalación y Uso

### 1. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar análisis completo

```bash
# Opción 1: Script de línea de comandos
python scripts/run_pca_analysis.py

# Opción 2: Jupyter Notebook (recomendado para exploración)
jupyter notebook notebooks/pca_analysis.ipynb
```

## 📊 Resultados Principales

### Varianza Explicada
- **PC1**: 72.96% de la varianza
- **PC2**: 22.85% de la varianza
- **Total**: **95.81%** de la varianza con solo 2 componentes
- Pérdida de información: ~4.19%

### Distribución de Clases
- **Setosa**: Claramente separada de las otras especies
- **Versicolor y Virginica**: Distinguibles con ligero solapamiento
- La proyección 2D mantiene excelente separabilidad

### Validación
- Implementación manual vs sklearn: diferencias < 1e-6
- Error de reconstrucción: MSE < 0.05

## 📈 Visualizaciones Generadas

1. **Scatter Plot 2D**: Proyección de datos en espacio PCA
2. **Varianza Explicada**: Individual y acumulada
3. **Biplot**: Datos + vectores de features originales
4. **Matriz de Correlación**: Entre features originales
5. **Matriz de Covarianza**: De datos estandarizados
6. **Comparación Manual vs Sklearn**: Validación de implementación

## 🔬 Metodología

### Algoritmo PCA Manual

1. **Estandarización**: 
   - Media = 0, Desviación estándar = 1
   - Fundamental para PCA (sensible a escala)

2. **Matriz de Covarianza**:
   ```
   Cov(X) = (1/(n-1)) * X^T * X
   ```

3. **Autovalores y Autovectores**:
   - Cov(X) * v = λ * v
   - Autovectores = direcciones principales
   - Autovalores = varianza en cada dirección

4. **Ordenar y Seleccionar**:
   - Ordenar por autovalores descendentes
   - Seleccionar primeros k componentes

5. **Proyección**:
   ```
   X_pca = X_centered * V_k
   ```

## 🧪 Componentes Principales

### PC1 (72.96% varianza)
- Fuertemente correlacionado con **petal length** y **petal width**
- Separa principalmente Setosa del resto

### PC2 (22.85% varianza)
- Mayor contribución de **sepal length** y **sepal width**
- Separa Versicolor y Virginica

## 📦 Dependencias Principales

- `numpy>=1.24.0`: Cálculos numéricos
- `pandas>=2.0.0`: Manipulación de datos
- `scikit-learn>=1.3.0`: Dataset y comparación
- `matplotlib>=3.7.0`: Visualizaciones
- `seaborn>=0.12.0`: Gráficos estadísticos
- `jupyter>=1.0.0`: Notebooks interactivos

## 📚 Referencias

1. **Tarea 2 PDF**: `Tarea 2 - Reducción de la dimensionalidad.pdf`
2. **Módulo 2**: Fundamentos de Machine Learning
3. **Dataset Iris**: [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/iris)
4. **PCA Theory**: [Wikipedia - Principal Component Analysis](https://en.wikipedia.org/wiki/Principal_component_analysis)

## 🔍 Conceptos Clave

- **PCA**: Técnica de aprendizaje no supervisado para reducción de dimensionalidad
- **Autovalores**: Representan la cantidad de varianza en cada dirección principal
- **Autovectores**: Direcciones de máxima varianza en los datos
- **Matriz de Covarianza**: Mide cómo varían juntas las características
- **Estandarización**: Normalizar features para que contribuyan equitativamente

## ✅ Validación

- ✅ Implementación manual equivalente a sklearn (diff < 1e-6)
- ✅ Varianza total explicada: 95.81%
- ✅ Separabilidad de clases mantenida en 2D
- ✅ Todos los tests pasados
- ✅ Visualizaciones generadas correctamente

## 👤 Autor

Felipe Ibarra  
Máster en IA Aplicada a la Ciberseguridad  
Noviembre 2025

## 📄 Licencia

Este proyecto es parte del material académico del Máster en IA Aplicada a la Ciberseguridad.
