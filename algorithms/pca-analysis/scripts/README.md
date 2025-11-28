# scripts/ - Scripts Ejecutables

## 📋 Descripción

Esta carpeta contiene scripts ejecutables para realizar el análisis PCA completo desde la línea de comandos. Son puntos de entrada convenientes que integran todos los módulos del proyecto.

## 📄 Archivos

### `run_pca_analysis.py`
Script principal que ejecuta el análisis PCA completo de principio a fin.

**Propósito**: Automatizar todo el pipeline de análisis PCA y generar resultados.

## 🔄 Flujo de Ejecución

```
┌────────────────────────────────────────────────────────────────┐
│                   run_pca_analysis.py                          │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ╔═════════════════════════════════════════════╗
        ║         1. CARGA DE DATOS                   ║
        ╚═════════════════════════════════════════════╝
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
            load_iris_data()    print estadísticas
            (150 samples)       descriptivas
            (4 features)
                              │
                              ▼
        ╔═════════════════════════════════════════════╗
        ║         2. PREPROCESAMIENTO                 ║
        ╚═════════════════════════════════════════════╝
                              │
                    standardize_data()
                    (μ = 0, σ = 1)
                              │
                              ▼
        ╔═════════════════════════════════════════════╗
        ║         3. ANÁLISIS DE CORRELACIÓN          ║
        ╚═════════════════════════════════════════════╝
                              │
                    get_correlation_matrix()
                              │
                    plot_correlation_heatmap()
                              │
                              ▼
        ╔═════════════════════════════════════════════╗
        ║         4. PCA MANUAL                       ║
        ╚═════════════════════════════════════════════╝
                              │
                    ┌─────────┴─────────┐
                    │                   │
        PCAManual.fit(X_scaled)        │
                    │                   │
        - Calcular matriz covarianza   │
        - Calcular autovalores         │
        - Calcular autovectores        │
        - Ordenar por varianza         │
                    │                   │
        PCAManual.transform()          │
                    │                   │
                    └─────────┬─────────┘
                              │
                    print métricas:
                    - Autovalores
                    - Varianza explicada
                    - Varianza acumulada
                              │
                              ▼
        ╔═════════════════════════════════════════════╗
        ║         5. PCA SKLEARN (Comparación)        ║
        ╚═════════════════════════════════════════════╝
                              │
                    PCA(n_components=2)
                              │
                    fit_transform(X_scaled)
                              │
                    Comparar diferencias
                    (debe ser < 1e-6)
                              │
                              ▼
        ╔═════════════════════════════════════════════╗
        ║         6. VISUALIZACIONES                  ║
        ╚═════════════════════════════════════════════╝
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
    plot_pca_scatter  plot_variance   plot_biplot
                      explained
              │               │               │
              ▼               ▼               ▼
    plot_covariance   plot_comparison
    matrix            manual_vs_sklearn
              │               │
              └───────────────┼───────────────┘
                              │
                              ▼
                    Guardar en results/
                    (6 archivos PNG)
                              │
                              ▼
        ╔═════════════════════════════════════════════╗
        ║         7. ANÁLISIS E INTERPRETACIÓN        ║
        ╚═════════════════════════════════════════════╝
                              │
                    print interpretación:
                    - Distribución de clases
                    - Varianza capturada
                    - Componentes principales
                    - Loadings de features
                              │
                              ▼
                        ✅ COMPLETO
```

## 🚀 Uso

### Ejecución básica

```bash
# Desde la raíz del proyecto
python scripts/run_pca_analysis.py
```

### Con entorno virtual

```bash
# Activar entorno
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Ejecutar
python scripts/run_pca_analysis.py
```

### Desde cualquier directorio

```bash
# Usando ruta absoluta
python /path/to/TAREA_2/scripts/run_pca_analysis.py
```

## 📊 Salida del Script

### Consola
El script imprime a consola:

1. **Carga de datos**
   - Dimensiones del dataset
   - Nombres de features y clases
   - Estadísticas descriptivas

2. **Preprocesamiento**
   - Confirmación de estandarización
   - Media y desviación estándar post-normalización

3. **Matriz de correlación**
   - Correlaciones entre features originales

4. **Resultados PCA Manual**
   - Autovalores completos
   - Varianza explicada por componente
   - Varianza acumulada

5. **Comparación con Sklearn**
   - Diferencias en varianza explicada (debe ser ~0)

6. **Interpretación**
   - Análisis de separabilidad de clases
   - Varianza capturada
   - Loadings de cada componente

### Archivos generados

Todos los archivos se guardan en `results/`:

```
results/
├── correlation_matrix.png          # Heatmap de correlaciones
├── covariance_matrix.png           # Heatmap de covarianza
├── pca_scatter_2d.png              # Proyección 2D de datos
├── variance_explained.png          # Gráficos de varianza
├── biplot.png                      # Biplot con vectores
└── comparison_manual_sklearn.png   # Comparación lado a lado
```

## 📦 Dependencias del Script

El script importa módulos de `src/`:

```python
from src.pca_manual import PCAManual
from src.data_loader import (
    load_iris_data,
    standardize_data,
    create_dataframe,
    get_data_statistics,
    get_correlation_matrix
)
from src.visualization import (
    plot_pca_scatter,
    plot_variance_explained,
    plot_biplot,
    plot_correlation_heatmap,
    plot_covariance_matrix,
    plot_comparison_manual_vs_sklearn
)
```

## ⚙️ Configuración

### Número de componentes

Para cambiar el número de componentes PCA, edita:

```python
pca_manual = PCAManual(n_components=2)  # Cambiar 2 por número deseado
```

### Ruta de resultados

Para cambiar dónde se guardan los gráficos:

```python
plot_pca_scatter(
    X_pca_manual, y, target_names,
    save_path='mi_carpeta/mi_grafico.png'  # Ruta personalizada
)
```

## 🔍 Estructura del Código

```python
def main():
    """Función principal que ejecuta todo el análisis"""
    
    # 1. Cargar datos
    X, y, feature_names, target_names = load_iris_data()
    
    # 2. Estandarizar
    X_scaled, scaler = standardize_data(X)
    
    # 3. Análisis de correlación
    corr_matrix = get_correlation_matrix(X, feature_names)
    plot_correlation_heatmap(corr_matrix, save_path='...')
    
    # 4. PCA Manual
    pca_manual = PCAManual(n_components=2)
    X_pca_manual = pca_manual.fit_transform(X_scaled)
    
    # 5. PCA Sklearn (comparación)
    pca_sklearn = PCA(n_components=2)
    X_pca_sklearn = pca_sklearn.fit_transform(X_scaled)
    
    # 6. Visualizaciones
    plot_pca_scatter(...)
    plot_variance_explained(...)
    plot_biplot(...)
    # ... más gráficos
    
    # 7. Análisis e interpretación
    # Imprimir métricas y conclusiones
```

## 🎯 Casos de Uso

### 1. Análisis rápido
Ejecutar el script tal cual para obtener todos los resultados.

### 2. Validación de implementación
Verificar que PCA manual coincide con sklearn.

### 3. Generación de reportes
Generar todas las visualizaciones para un informe.

### 4. Experimentación
Modificar parámetros y re-ejecutar para ver efectos.

## 🔗 Relaciones

- **Importa desde**: `src/`
- **Genera archivos en**: `results/`
- **Alternativa**: `notebooks/pca_analysis.ipynb` (interactivo)

## 📝 Ejemplo de Salida

```
======================================================================
 ANÁLISIS PCA - REDUCCIÓN DE DIMENSIONALIDAD
======================================================================

Dataset: Iris
Objetivo: Reducir de 4 a 2 dimensiones manteniendo máxima varianza

======================================================================
 1. CARGA DE DATOS
======================================================================

✓ Dataset cargado: 150 muestras, 4 features
✓ Features: ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
✓ Clases: ['setosa', 'versicolor', 'virginica']

📊 Estadísticas descriptivas (datos originales):
       sepal length (cm)  sepal width (cm)  ...
count         150.000000        150.000000  ...
mean            5.843333          3.057333  ...
std             0.828066          0.435866  ...
...

======================================================================
 4. PCA MANUAL (Autovalores y Autovectores)
======================================================================

✓ PCA manual completado

📈 Autovalores (varianzas): [2.91081808 0.92122093 0.14735328 0.02060771]

📊 Varianza explicada por cada componente:
   PC1: 72.96%
   PC2: 22.85%

📊 Varianza acumulada:
   2 componentes: 95.81%

...
```

## 💡 Notas

- El script crea automáticamente la carpeta `results/` si no existe
- Se recomienda ejecutar dentro de un entorno virtual
- La ejecución toma ~5-10 segundos dependiendo del sistema
- Todos los gráficos se exportan a 300 DPI para calidad profesional
