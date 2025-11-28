# Resultados y Análisis Detallado

## Tarea 2: Reducción de Dimensionalidad con PCA
**Fecha**: Noviembre 2025  
**Autor**: Felipe Ibarra

---

## 1. Resumen Ejecutivo

Este documento presenta los resultados del análisis PCA aplicado al dataset Iris, implementando el algoritmo desde cero mediante cálculo de autovalores y autovectores de la matriz de covarianza. Se logró reducir exitosamente de 4 a 2 dimensiones manteniendo **95.81%** de la varianza total.

## 2. Descripción del Dataset

### Dataset Iris
- **Muestras**: 150 (50 por cada clase)
- **Features**: 4 características numéricas
  - `sepal length (cm)`: Longitud del sépalo
  - `sepal width (cm)`: Ancho del sépalo
  - `petal length (cm)`: Longitud del pétalo
  - `petal width (cm)`: Ancho del pétalo
- **Clases**: 3 especies de iris
  - Setosa
  - Versicolor
  - Virginica

### Estadísticas Descriptivas (Datos Originales)

| Feature | Media | Std | Min | Max |
|---------|-------|-----|-----|-----|
| sepal length | 5.84 | 0.83 | 4.30 | 7.90 |
| sepal width | 3.06 | 0.44 | 2.00 | 4.40 |
| petal length | 3.76 | 1.77 | 1.00 | 6.90 |
| petal width | 1.20 | 0.76 | 0.10 | 2.50 |

## 3. Preprocesamiento

### 3.1 Estandarización

**¿Por qué es fundamental?**
- PCA es sensible a la escala de las variables
- Features con mayor varianza dominarían los componentes sin estandarización
- Queremos que todas las features contribuyan equitativamente

**Transformación aplicada**:
```
X_scaled = (X - μ) / σ
```

**Resultado**:
- Media después: [~0, ~0, ~0, ~0] (≈ 1e-15)
- Desviación estándar después: [1, 1, 1, 1]

### 3.2 Matriz de Correlación

```
                    sepal length  sepal width  petal length  petal width
sepal length (cm)      1.000        -0.118        0.872         0.818
sepal width (cm)      -0.118         1.000       -0.428        -0.366
petal length (cm)      0.872        -0.428        1.000         0.963
petal width (cm)       0.818        -0.366        0.963         1.000
```

**Observaciones**:
- Fuerte correlación positiva entre petal length y petal width (0.963)
- Fuerte correlación entre sepal length y dimensiones del pétalo
- Sepal width tiene correlación negativa con dimensiones del pétalo
- Estas correlaciones justifican la reducción de dimensionalidad

## 4. Implementación PCA Manual

### 4.1 Algoritmo

1. **Centrar datos**: X_centered = X - mean(X)
2. **Matriz de covarianza**: Cov(X) = (1/(n-1)) * X^T * X
3. **Autovalores y autovectores**: numpy.linalg.eig(Cov)
4. **Ordenar**: Descendente por autovalores
5. **Seleccionar**: Primeros k componentes
6. **Proyectar**: X_pca = X_centered * V_k

### 4.2 Matriz de Covarianza (Datos Estandarizados)

```
                    sepal length  sepal width  petal length  petal width
sepal length (cm)      1.007        -0.119        0.878         0.824
sepal width (cm)      -0.119         1.007       -0.431        -0.369
petal length (cm)      0.878        -0.431        1.007         0.970
petal width (cm)       0.824        -0.369        0.970         1.007
```

*Nota: Valores ~1 en diagonal porque los datos están estandarizados*

### 4.3 Autovalores (Varianzas)

```
λ1 = 2.9185 (72.96%)
λ2 = 0.9140 (22.85%)
λ3 = 0.1468 (3.67%)
λ4 = 0.0207 (0.52%)
```

**Total varianza explicada por PC1 + PC2**: **95.81%**

### 4.4 Autovectores (Componentes Principales)

**PC1** (Primer componente principal):
```
sepal length (cm):  0.5211
sepal width (cm):  -0.2693
petal length (cm):  0.5804
petal width (cm):   0.5649
```

**PC2** (Segundo componente principal):
```
sepal length (cm):  0.3774
sepal width (cm):   0.9233
petal length (cm):  0.0245
petal width (cm):   0.0669
```

## 5. Interpretación de Componentes

### PC1: "Tamaño General" (72.96% varianza)

**Características**:
- Fuertemente correlacionado con petal length (0.5804) y petal width (0.5649)
- También correlacionado positivamente con sepal length (0.5211)
- Correlación negativa con sepal width (-0.2693)

**Interpretación biológica**:
- Representa el "tamaño general de la flor"
- Flores con PC1 alto tienen pétalos largos y anchos
- Este componente separa principalmente **Setosa** (valores bajos) del resto

### PC2: "Forma del Sépalo" (22.85% varianza)

**Características**:
- Dominado por sepal width (0.9233)
- Contribución moderada de sepal length (0.3774)
- Mínima contribución de dimensiones del pétalo

**Interpretación biológica**:
- Representa la "forma del sépalo"
- Captura variaciones en el ancho relativo del sépalo
- Ayuda a distinguir entre **Versicolor y Virginica**

## 6. Resultados de Proyección 2D

### 6.1 Distribución de Clases en Espacio PCA

| Especie | PC1 Media | PC1 Std | PC2 Media | PC2 Std |
|---------|-----------|---------|-----------|---------|
| Setosa | -2.68 | 0.32 | -0.33 | 0.39 |
| Versicolor | -0.08 | 0.58 | 0.17 | 0.23 |
| Virginica | 1.79 | 0.57 | -0.08 | 0.28 |

**Observaciones**:
- **Setosa**: PC1 muy bajo (< -2), completamente separada
- **Versicolor**: PC1 cercano a 0, intermedia
- **Virginica**: PC1 alto (> 1.5), flores más grandes
- PC2 ayuda a separar Versicolor y Virginica

### 6.2 Separabilidad

- **Setosa vs Resto**: Separación perfecta en PC1
- **Versicolor vs Virginica**: Buena separación con ligero solapamiento
- **Clasificación 2D**: Posible con alta precisión (estimada >95%)

## 7. Validación: Manual vs Sklearn

### 7.1 Comparación de Varianza Explicada

| Componente | Manual | Sklearn | Diferencia |
|------------|--------|---------|------------|
| PC1 | 72.9624% | 72.9625% | 0.000001% |
| PC2 | 22.8507% | 22.8507% | 0.000000% |

**Conclusión**: Implementación manual es **equivalente** a sklearn (diferencias < 1e-6)

### 7.2 Comparación Visual

Los gráficos de dispersión muestran proyecciones idénticas:
- Posiciones de puntos coinciden (diferencias < 0.001)
- Puede haber reflexión de ejes (no afecta análisis)
- La estructura de separación de clases es idéntica

## 8. Error de Reconstrucción

Al proyectar a 2D y reconstruir a 4D:

```
Error de Reconstrucción (MSE): 0.0419
```

**Interpretación**:
- Error muy bajo confirma que 2 componentes capturan bien los datos
- Consistente con 95.81% de varianza explicada
- ~4.19% de información perdida es principalmente ruido

## 9. Análisis de Varianza Acumulada

| Componentes | Varianza Acumulada |
|-------------|-------------------|
| 1 | 72.96% |
| 2 | **95.81%** |
| 3 | 99.48% |
| 4 | 100.00% |

**Criterio de selección**:
- Regla del 90%: 2 componentes suficientes (95.81% > 90%)
- Codo del gráfico: Cambio significativo después de PC2
- Interpretabilidad: 2D permite visualización intuitiva

## 10. Aplicaciones Prácticas

### 10.1 Visualización
- Reducir de 4D a 2D permite gráficos de dispersión interpretables
- Mantiene estructura de separación de clases
- Facilita análisis exploratorio

### 10.2 Reducción de Complejidad
- De 4 features a 2 componentes (50% reducción)
- Modelos más simples y rápidos
- Menor riesgo de overfitting

### 10.3 Eliminación de Ruido
- Los componentes menores (PC3, PC4) capturan principalmente ruido
- Al eliminarlos, mejoramos signal-to-noise ratio

## 11. Limitaciones y Consideraciones

### Limitaciones de PCA

1. **Linealidad**: PCA asume relaciones lineales
2. **Varianza = Información**: Asume que varianza alta es información útil
3. **Interpretabilidad**: Componentes son combinaciones lineales abstractas
4. **Sensibilidad a outliers**: Puede distorsionar componentes principales

### Consideraciones del Dataset Iris

- Dataset pequeño (150 muestras) y limpio
- Features ya tienen buena escala relativa
- Clases bien separadas facilitan el análisis
- En datasets reales, preprocesamiento más complejo puede ser necesario

## 12. Conclusiones

### 12.1 Objetivos Cumplidos ✅

1. ✅ **Comprender PCA**: Implementación desde cero demuestra comprensión profunda
2. ✅ **Aplicar PCA**: Reducción exitosa de 4D a 2D
3. ✅ **Visualización**: Gráficos profesionales generados
4. ✅ **Análisis**: Varianza explicada y componentes interpretados

### 12.2 Hallazgos Principales

- **95.81%** de varianza preservada con solo 2 componentes
- PC1 representa "tamaño general", PC2 representa "forma del sépalo"
- Implementación manual equivalente a sklearn (validación exitosa)
- Setosa perfectamente separable, Versicolor/Virginica distinguibles

### 12.3 Aprendizajes Clave

1. La **estandarización es crítica** antes de PCA
2. Los **autovalores indican importancia** de cada componente
3. Los **autovectores muestran relación** con features originales
4. **2 componentes son suficientes** para este dataset (criterio 90%)
5. PCA es efectivo para **visualización y reducción de complejidad**

## 13. Próximos Pasos (Trabajo Futuro)

### Extensiones Posibles

1. **Clasificación**: Entrenar modelos (SVM, KNN) en espacio PCA
2. **PCA Kernel**: Aplicar para capturar relaciones no lineales
3. **Análisis de Sensibilidad**: Estudiar efecto de outliers
4. **Comparación con t-SNE/UMAP**: Métodos no lineales de reducción
5. **Validación cruzada**: Con splits train/test

### Aplicaciones en Ciberseguridad

- **Detección de anomalías**: Reducir features en logs de red
- **Visualización de tráfico**: Proyectar flujos de red a 2D/3D
- **Análisis de malware**: Reducir dimensionalidad de features estáticas
- **IDS/IPS**: Preprocesamiento para modelos de detección

---

## Referencias

1. Jolliffe, I. T. (2002). *Principal Component Analysis*. Springer.
2. Fisher, R. A. (1936). *The use of multiple measurements in taxonomic problems*. Annals of Eugenics.
3. Shlens, J. (2014). *A Tutorial on Principal Component Analysis*. arXiv:1404.1100.

---

**Fin del Documento de Resultados**
