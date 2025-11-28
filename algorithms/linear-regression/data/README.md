# 📁 data/ - Datasets

## 📋 Propósito
Almacenamiento de datos en diferentes etapas del pipeline ML.

---

## 🗂️ Estructura

```
data/
├── raw/              # Datos originales sin procesar
│   └── kddcup.data_10_percent
├── processed/        # Datos limpiados y transformados
│   ├── cleaned.csv
│   └── encoded.csv
└── splits/           # Train/test splits
    ├── X_train.csv
    ├── X_test.csv
    ├── y_train.csv
    └── y_test.csv
```

---

## 🔄 Flujo de Datos

```
┌──────────────┐
│  raw/        │ Datos originales (inmutables)
└──────┬───────┘
       │ src/data_loader.py
       ▼
┌──────────────┐
│ processed/   │ Datos limpios
└──────┬───────┘
       │ src/preprocessing.py
       ▼
┌──────────────┐
│  splits/     │ Train/Test listos
└──────────────┘
```

---

## 📊 Dataset: KDD Cup 1999

### Descripción
- **Archivo**: `kddcup.data_10_percent` (75 MB)
- **Registros**: ~494,021 conexiones de red
- **Features**: 41 variables
- **Objetivo**: Detección de intrusiones

### Características
- Numéricas: duration, src_bytes, dst_bytes, etc.
- Categóricas: protocol_type, service, flag
- Target: connection_type (normal/attack)

---

## 📝 Uso

### Cargar datos raw
```python
from src.data_loader import load_kdd_data

df = load_kdd_data('data/raw/kddcup.data_10_percent')
```

### Guardar datos procesados
```python
df_clean.to_csv('data/processed/cleaned.csv', index=False)
```

### Cargar splits
```python
import pandas as pd

X_train = pd.read_csv('data/splits/X_train.csv')
y_train = pd.read_csv('data/splits/y_train.csv')
```

---

## 🔒 Buenas Prácticas

- ✅ `raw/` es **inmutable** - nunca modificar
- ✅ `processed/` para datos intermedios
- ✅ `splits/` generado automáticamente
- ✅ Usar `.gitignore` para archivos grandes
- ✅ Documentar transformaciones

---

## 🐳 Acceso en Contenedor

Los datos se comparten entre Mac y contenedor:

```
Mac: ./data/          ↔️  Contenedor: /app/data/
```

Cambios en cualquier lado se reflejan automáticamente.

---

## 🔗 Ver También
- `src/data_loader.py` - Carga de datos
- `src/preprocessing.py` - Procesamiento
