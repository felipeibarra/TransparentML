# 📁 results/ - Resultados

## 📋 Propósito
Almacena todos los outputs del entrenamiento: métricas, visualizaciones y reportes.

---

## 🗂️ Estructura

```
results/
├── figures/          # Visualizaciones PNG
│   ├── residuals.png
│   ├── predictions_vs_actual.png
│   ├── feature_importance.png
│   └── learning_curves.png
├── metrics/          # Métricas JSON/CSV
│   ├── evaluation.json
│   ├── model_comparison.csv
│   └── detailed_metrics.json
└── models/           # Modelos entrenados (deprecated)
    └── *.joblib      # Usar /models/ en raíz
```

---

## 🔄 Flujo de Generación

```
scripts/train.py
    │
    ├─> src/evaluation (métricas)
    │       │
    │       ▼
    │   results/metrics/*.json
    │
    └─> src/visualization (gráficos)
            │
            ▼
        results/figures/*.png
```

---

## 📊 Tipos de Outputs

### 1. Métricas (`metrics/`)

**`evaluation.json`**:
```json
{
  "r2_score": 0.8523,
  "mae": 0.0234,
  "mse": 0.0012,
  "rmse": 0.0346,
  "train_time": 1.23
}
```

**`model_comparison.csv`**:
```csv
model,r2,mae,rmse,train_time
LinearRegression,0.85,0.023,0.034,1.2
Ridge,0.87,0.021,0.032,1.5
Lasso,0.84,0.024,0.035,1.3
```

### 2. Visualizaciones (`figures/`)

- **residuals.png**: Análisis de residuos
- **predictions_vs_actual.png**: Predicciones vs valores reales
- **feature_importance.png**: Importancia de features
- **learning_curves.png**: Curvas de aprendizaje
- **correlation_matrix.png**: Matriz de correlación

---

## 📝 Uso

### Leer métricas
```python
import json

with open('results/metrics/evaluation.json') as f:
    metrics = json.load(f)
    
print(f"R² Score: {metrics['r2_score']}")
```

### Ver visualizaciones
```bash
open results/figures/predictions_vs_actual.png
```

### Comparar modelos
```python
import pandas as pd

df = pd.read_csv('results/metrics/model_comparison.csv')
best_model = df.loc[df['r2'].idxmax()]
print(f"Mejor modelo: {best_model['model']}")
```

---

## 🐳 Acceso en Contenedor

Resultados compartidos entre Mac y contenedor:

```
Mac: ./results/          ↔️  Contenedor: /app/results/
```

Ejecutas entrenamiento en contenedor → resultados aparecen en tu Mac.

---

## 🧹 Limpieza

```bash
# Limpiar resultados
make clean-results

# O manualmente
rm -rf results/figures/* results/metrics/*
```

---

## 📈 Análisis Post-Entrenamiento

1. **Revisar métricas**:
   ```bash
   cat results/metrics/evaluation.json | python3 -m json.tool
   ```

2. **Ver gráficos**:
   ```bash
   open results/figures/
   ```

3. **Comparar modelos**:
   ```bash
   cat results/metrics/model_comparison.csv
   ```

---

## 🔗 Ver También
- `src/evaluation.py` - Genera métricas
- `models/` - Modelos guardados
- `scripts/train.py` - Script de entrenamiento
