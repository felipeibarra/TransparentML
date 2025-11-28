# results/ - Visualizaciones y Resultados

## 📋 Descripción

Esta carpeta contiene todas las visualizaciones generadas por el análisis PCA. Los gráficos están en formato PNG de alta resolución (300 DPI) listos para incluir en reportes, presentaciones o publicaciones.

## 📊 Archivos de Visualización

```
results/
├── correlation_matrix.png          # Heatmap de correlaciones
├── covariance_matrix.png           # Heatmap de covarianza
├── pca_scatter_2d.png              # Proyección 2D de datos
├── variance_explained.png          # Gráficos de varianza
├── biplot.png                      # Biplot con vectores
└── comparison_manual_sklearn.png   # Comparación manual vs sklearn
```

## 🎨 Descripción de Visualizaciones

### 1. `correlation_matrix.png`
**Matriz de Correlación entre Features Originales**

```
┌─────────────────────────────────────────┐
│     Correlation Heatmap                 │
│                                         │
│        sepal  sepal  petal  petal       │
│        length width  length width       │
│                                         │
│ sepal   1.0   -0.1    0.9    0.8        │
│ length                                  │
│                                         │
│ sepal  -0.1    1.0   -0.4   -0.4        │
│ width                                   │
│                                         │
│ petal   0.9   -0.4    1.0    1.0        │
│ length                                  │
│                                         │
│ petal   0.8   -0.4    1.0    1.0        │
│ width                                   │
└─────────────────────────────────────────┘
```

**Interpretación**:
- 🔴 Valores cercanos a +1: Correlación positiva fuerte
- 🔵 Valores cercanos a -1: Correlación negativa fuerte
- ⚪ Valores cercanos a 0: Sin correlación

**Insights**:
- Petal length y petal width están altamente correlacionadas (≈0.96)
- Sepal width tiene correlación negativa con otras features
- Esto sugiere que PCA puede reducir dimensionalidad eficientemente

---

### 2. `covariance_matrix.png`
**Matriz de Covarianza de Datos Estandarizados**

```
┌─────────────────────────────────────────┐
│     Covariance Matrix                   │
│                                         │
│     (de datos estandarizados)           │
│                                         │
│   Diagonal = Varianza de cada feature   │
│   Off-diagonal = Covarianza             │
│                                         │
│   Usado para calcular autovalores       │
│   y autovectores en PCA                 │
└─────────────────────────────────────────┘
```

**Propósito**:
- Muestra cómo varían juntas las características
- Base matemática del análisis PCA
- Diagonal = varianza de cada feature (≈1 tras estandarización)

---

### 3. `pca_scatter_2d.png`
**Proyección 2D del Dataset Iris en Espacio PCA**

```
┌─────────────────────────────────────────┐
│                                         │
│         PC2 (22.85%)                    │
│            ▲                            │
│            │                            │
│      ●     │     ■                      │
│    ●●●     │   ■■■                      │
│   ●●●●●    │  ■■■■   ▲▲▲               │
│  ●●●●●●    │ ■■■■■  ▲▲▲▲               │
│   ●●●      │  ■■■■  ▲▲▲▲▲              │
│    ●       │   ■■  ▲▲▲▲▲               │
│            │      ▲▲▲▲                  │
│────────────┼─────────────►             │
│            │         PC1 (72.96%)       │
│                                         │
│  Leyenda:                               │
│  ● Setosa    ■ Versicolor   ▲ Virginica│
└─────────────────────────────────────────┘
```

**Interpretación**:
- **Setosa** (izquierda): Claramente separada
- **Versicolor** (centro): Distinción moderada
- **Virginica** (derecha): Ligero solapamiento con Versicolor
- PC1 captura la mayor separación entre especies
- PC2 refina la separación Versicolor-Virginica

---

### 4. `variance_explained.png`
**Varianza Explicada por Componente Principal**

```
┌─────────────────────────────────────────────────────┐
│  Varianza Individual        Varianza Acumulada      │
│                                                     │
│     72.96%                       100%               │
│      ███                           ●               │
│      ███                         ●                 │
│      ███        22.85%         ●                   │
│      ███         ██          ●                     │
│      ███         ██        ●                       │
│      ███         ██      ●                         │
│      ███         ██    ●  ←── 95.81% con 2 PCs     │
│      ───         ──  ●                             │
│       PC1        PC2                               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Interpretación**:
- **PC1**: Captura 72.96% de varianza
- **PC2**: Captura 22.85% adicional
- **Total**: 95.81% con solo 2 componentes
- **Pérdida**: Solo 4.19% de información

**Conclusión**: 2 componentes son suficientes para representar el dataset

---

### 5. `biplot.png`
**Biplot: Datos + Vectores de Features Originales**

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│            PC2                                      │
│             ▲                                       │
│             │    sepal width                        │
│             │         ↗                             │
│       ●     │     ■         ▲                       │
│     ●●●     │   ■■■      ▲▲▲                        │
│    ●●●●●────┼─■■■■■─▲▲▲▲▲ ───► petal length        │
│   ●●●●●●    │■■■■■■▲▲▲▲▲                            │
│    ●●●      │ ■■■■▲▲▲▲▲                             │
│             │   ■ ▲▲▲     petal width               │
│             │    ▲        ↗                         │
│─────────────┼────────────►                          │
│             │         PC1                           │
│             │   sepal length ↗                      │
│                                                     │
│  Leyenda:                                           │
│  ●■▲ = Observaciones por especie                    │
│  ──► = Vectores de features originales              │
└─────────────────────────────────────────────────────┘
```

**Interpretación**:
- **Vectores largos**: Features con mayor contribución a PCs
- **Vectores paralelos**: Features correlacionadas (petal length/width)
- **Vectores perpendiculares**: Features no correlacionadas
- **PC1**: Dominado por petal length y petal width
- **PC2**: Mayor contribución de sepal width

**Uso**: Entender qué features originales definen cada componente principal

---

### 6. `comparison_manual_sklearn.png`
**Comparación: PCA Manual vs Sklearn**

```
┌────────────────────────────────────────────────────┐
│                                                    │
│   PCA Manual              PCA Sklearn              │
│   ┌──────────────┐       ┌──────────────┐         │
│   │              │       │              │         │
│   │    ●   ■  ▲  │       │    ●   ■  ▲  │         │
│   │  ●●● ■■■ ▲▲▲ │       │  ●●● ■■■ ▲▲▲ │         │
│   │ ●●●●■■■■▲▲▲▲ │       │ ●●●●■■■■▲▲▲▲ │         │
│   │  ●●● ■■■ ▲▲▲ │       │  ●●● ■■■ ▲▲▲ │         │
│   │   ●   ■  ▲   │       │   ●   ■  ▲   │         │
│   │              │       │              │         │
│   └──────────────┘       └──────────────┘         │
│                                                    │
│   Diferencia en varianza: < 1e-6 ✓                 │
│   Implementación validada correctamente            │
└────────────────────────────────────────────────────┘
```

**Propósito**: Validar que la implementación manual es correcta

**Validación**:
- ✅ Proyecciones prácticamente idénticas
- ✅ Diferencias < 0.000001 (errores de redondeo)
- ✅ Varianza explicada coincide

---

## 📐 Especificaciones Técnicas

| Propiedad | Valor |
|-----------|-------|
| Formato | PNG |
| Resolución | 300 DPI |
| Calidad | Alta (para publicación) |
| Color | RGB |
| Tamaño típico | 10x8 pulgadas |
| Compresión | Sin pérdida |

## 🔄 Regenerar Visualizaciones

### Opción 1: Script de línea de comandos
```bash
python scripts/run_pca_analysis.py
```

### Opción 2: Jupyter Notebook
```bash
jupyter notebook notebooks/pca_analysis.ipynb
# Ejecutar todas las celdas
```

### Opción 3: API
```bash
# Iniciar servidor
uvicorn src.api:app --reload

# Regenerar
curl -X POST http://localhost:8000/refresh
```

## 📦 Uso de Visualizaciones

### En LaTeX
```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{results/pca_scatter_2d.png}
    \caption{Proyección PCA del dataset Iris}
    \label{fig:pca_scatter}
\end{figure}
```

### En Markdown
```markdown
![PCA Scatter 2D](results/pca_scatter_2d.png)
```

### En Presentaciones
- Arrastra y suelta directamente en PowerPoint/Keynote
- Alta resolución (300 DPI) garantiza calidad en proyección

## 🎯 Interpretación Global

```
┌────────────────────────────────────────────────────┐
│         PIPELINE DE VISUALIZACIONES                │
│                                                    │
│  Datos Raw  →  Correlación  →  Covarianza         │
│     ↓              ↓              ↓                │
│     └──────────────┴──────────────┘                │
│                    │                               │
│                    ▼                               │
│            ┌──────────────┐                        │
│            │   PCA Manual │                        │
│            └──────┬───────┘                        │
│                   │                                │
│         ┌─────────┼─────────┐                      │
│         ▼         ▼         ▼                      │
│     Scatter   Variance  Biplot                     │
│                                                    │
│         └─────────┬─────────┘                      │
│                   │                                │
│                   ▼                               │
│            Validación sklearn                      │
│               (Comparación)                        │
└────────────────────────────────────────────────────┘
```

## 🔗 Relaciones

- **Generado por**: `scripts/run_pca_analysis.py`, `notebooks/pca_analysis.ipynb`, `src/api.py`
- **Usa código de**: `src/visualization.py`
- **Documentado en**: `docs/RESULTADOS.md`

## 💡 Tips

### Personalizar gráficos
Modifica `src/visualization.py` para cambiar:
- Colores
- Tamaños de figura
- Estilos de markers
- Resolución (DPI)

### Exportar otros formatos
```python
# En notebooks o scripts
plt.savefig('grafico.pdf', dpi=300, bbox_inches='tight')  # PDF
plt.savefig('grafico.svg', dpi=300, bbox_inches='tight')  # SVG
```

### Animaciones (avanzado)
```python
# Crear GIF de rotación 3D (requiere 3 PCs)
from matplotlib.animation import FuncAnimation
# ... código de animación
```

## 📊 Análisis Comparativo

| Visualización | Propósito | Audiencia |
|---------------|-----------|-----------|
| Correlation Matrix | Exploración inicial | Técnica |
| Covariance Matrix | Fundamento matemático | Avanzada |
| PCA Scatter | Resultado principal | Todas |
| Variance Explained | Justificar n_components | Técnica |
| Biplot | Interpretar componentes | Técnica/Académica |
| Comparison | Validación | Desarrollo/Revisión |

## 🚀 Próximos Pasos

Después de revisar las visualizaciones:
1. Interpretar resultados en contexto del problema
2. Ajustar número de componentes si es necesario
3. Usar componentes principales para tareas downstream:
   - Clasificación
   - Clustering
   - Visualización
   - Reducción de ruido
