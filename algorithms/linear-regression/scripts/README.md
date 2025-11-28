# 📁 scripts/ - Scripts Ejecutables

## 📋 Propósito
Scripts que orquestan los módulos de `src/` para entrenar modelos y servir la API.

---

## 🗂️ Estructura

```
scripts/
├── train.py          # Entrenamiento de modelos
├── backup.sh         # Script de respaldo
└── api/              # API REST
    ├── __init__.py
    └── main.py       # FastAPI application
```

---

## 🔄 Flujo de Ejecución

```
make train
    │
    ▼
docker-compose exec training-service
    │
    ▼
python scripts/train.py
    │
    ├─> src/data_loader
    ├─> src/preprocessing
    ├─> src/models
    ├─> src/evaluation
    │
    ▼
results/ & models/
```

---

## 📜 Scripts

### `train.py` - Entrenamiento
```bash
make train  # Ejecutar EN CONTENEDOR
```

**Flujo**:
1. Cargar datos
2. Preprocesar
3. Entrenar modelos
4. Evaluar
5. Guardar resultados

**Outputs**:
- `models/*.joblib`
- `results/metrics/*.json`
- `results/figures/*.png`

### `api/main.py` - API REST
```bash
make up                  # Iniciar API
make api-health          # Verificar
```

**Endpoints**: http://localhost:8000/docs

### `backup.sh` - Respaldos
```bash
./scripts/backup.sh
```

---

## 🐳 Ejecución

```bash
# ✅ Correcto (en contenedor)
make train

# ❌ Incorrecto (en Mac)
python scripts/train.py
```

---

## 🔗 Ver También
- `src/` - Módulos utilizados
- `DOCKER_WORKFLOW.md` - Guía completa
