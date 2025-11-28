# 🏗️ Arquitectura del Sistema

## 📐 Diagrama General

```
┌─────────────────────────────────────────────────────────────────┐
│                         TU MAC (HOST)                            │
│                                                                   │
│  📝 Editas código aquí con tu editor favorito                   │
│  ├── src/          (sincronizado con contenedores)              │
│  ├── scripts/      (sincronizado con contenedores)              │
│  └── Makefile      (orquesta todo)                              │
│                                                                   │
│  📂 Resultados guardados aquí automáticamente                   │
│  ├── results/      (compartido desde contenedores)              │
│  ├── models/       (compartido desde contenedores)              │
│  └── data/         (compartido con contenedores)                │
│                                                                   │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        │ Docker Volumes (sincronización bidireccional)
                        │
┌───────────────────────┴─────────────────────────────────────────┐
│                    DOCKER CONTAINERS                             │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  🎯 training-service (ml-training-service)              │   │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│   │
│  │  Python 3.11 + ML Libraries                             │   │
│  │  - numpy, pandas, scikit-learn                          │   │
│  │  - matplotlib, seaborn                                  │   │
│  │  - pytest, black, flake8, mypy                          │   │
│  │                                                          │   │
│  │  ✅ Ejecuta: make train                                 │   │
│  │  ✅ Ejecuta: make test                                  │   │
│  │  ✅ Ejecuta: make format                                │   │
│  │  ✅ Shell: make shell-training                          │   │
│  │                                                          │   │
│  │  📁 /app/src/      ← sincronizado con ./src/           │   │
│  │  📁 /app/scripts/  ← sincronizado con ./scripts/       │   │
│  │  📁 /app/results/  ↔ compartido con ./results/         │   │
│  │  📁 /app/models/   ↔ compartido con ./models/          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  🌐 prediction-api (ml-prediction-api)                  │   │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│   │
│  │  FastAPI + Uvicorn                                      │   │
│  │  Puerto: 8000                                           │   │
│  │                                                          │   │
│  │  Endpoints:                                             │   │
│  │  - GET  /health         (health check)                  │   │
│  │  - GET  /model_info     (info del modelo)               │   │
│  │  - POST /predict        (predicción individual)         │   │
│  │  - POST /batch_predict  (predicciones en batch)         │   │
│  │  - POST /reload_model   (recargar modelo)               │   │
│  │                                                          │   │
│  │  ✅ Acceso: http://localhost:8000/docs                  │   │
│  │  ✅ Test: make api-health                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  📊 jupyter-lab (ml-jupyter-lab)                        │   │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│   │
│  │  JupyterLab + IPython                                   │   │
│  │  Puerto: 8888                                           │   │
│  │                                                          │   │
│  │  ✅ Acceso: http://localhost:8888                       │   │
│  │  📓 Notebooks interactivos                              │   │
│  │  🔬 Análisis exploratorio                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  🔀 nginx-gateway (ml-nginx-gateway)                    │   │
│  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│   │
│  │  Nginx Alpine                                           │   │
│  │  Puerto: 80                                             │   │
│  │                                                          │   │
│  │  Rutas:                                                 │   │
│  │  - /api/      → prediction-api:8000                     │   │
│  │  - /jupyter/  → jupyter-lab:8888                        │   │
│  │                                                          │   │
│  │  Features:                                              │   │
│  │  - Rate limiting                                        │   │
│  │  - Load balancing                                       │   │
│  │  - Reverse proxy                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  🌐 Red: ml-network (172.20.0.0/16)                             │
│  Los contenedores pueden comunicarse entre sí                    │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Datos

### 1. Desarrollo
```
Mac (editar código) 
    ↓
Sincronización automática (volúmenes Docker)
    ↓
Contenedor (código actualizado inmediatamente)
```

### 2. Entrenamiento
```
make train
    ↓
Makefile ejecuta: docker-compose exec training-service python scripts/train.py
    ↓
Contenedor training-service ejecuta Python
    ↓
Lee datos desde /app/data/ (compartido)
    ↓
Procesa y entrena modelo
    ↓
Guarda resultados en /app/results/ y /app/models/ (compartidos)
    ↓
Resultados aparecen automáticamente en tu Mac en ./results/ y ./models/
```

### 3. Predicciones
```
Usuario hace request HTTP
    ↓
http://localhost:8000/predict
    ↓
Nginx Gateway (opcional)
    ↓
prediction-api (FastAPI)
    ↓
Carga modelo desde /app/models/ (compartido)
    ↓
Hace predicción
    ↓
Retorna JSON
```

## 📦 Volúmenes Compartidos

| Mac (Host) | Contenedor | Tipo | Descripción |
|-----------|-----------|------|-------------|
| `./src/` | `/app/src/` | bind | Código fuente (sync bidireccional) |
| `./scripts/` | `/app/scripts/` | bind | Scripts (sync bidireccional) |
| `./data/` | `/app/data/` | bind | Datos (compartido) |
| `./results/` | `/app/results/` | bind | Resultados (compartido) |
| `./models/` | `/app/models/` | bind | Modelos entrenados (compartido) |

**Sync bidireccional significa:**
- Cambios en Mac → reflejados instantáneamente en contenedor
- Cambios en contenedor → reflejados instantáneamente en Mac

## 🛠️ Comandos y Ejecución

### Capa 1: Makefile (Tu interfaz)
```bash
make train
```
↓

### Capa 2: Docker Compose (Orquestación)
```bash
docker-compose exec training-service python scripts/train.py
```
↓

### Capa 3: Contenedor (Ejecución)
```bash
# Dentro del contenedor
python scripts/train.py
```

## 🔐 Principios de Diseño

### 1. **Separación de Concerns**
- Cada contenedor tiene una responsabilidad única
- training-service: ML y procesamiento
- prediction-api: Servir predicciones
- jupyter-lab: Exploración interactiva
- nginx-gateway: Routing y seguridad

### 2. **Inmutabilidad**
- Código editado en Mac
- Contenedores son inmutables (reconstruir para cambios estructurales)
- Volúmenes para persistencia de datos

### 3. **Portabilidad**
- Funciona igual en Mac, Linux, Windows
- Solo requiere Docker
- Sin dependencias del sistema host

### 4. **Reproducibilidad**
- Mismo entorno en todas las máquinas
- Versiones fijas en requirements.txt
- Dockerfile define entorno exacto

## 🚦 Estados de los Servicios

```
make build    →  Imágenes construidas (pero no corriendo)
make up       →  Servicios corriendo
make down     →  Servicios detenidos
make restart  →  Servicios reiniciados (sin reconstruir)
```

### Ciclo de vida típico:

```
1. Build:    Dockerfile → Imagen Docker
2. Up:       Imagen → Contenedor corriendo
3. Exec:     make train → Ejecuta comando en contenedor
4. Results:  Resultados guardados en volúmenes
5. Down:     Contenedor se detiene (volúmenes persisten)
```

## 🔍 Debugging

### Ver qué está pasando:
```bash
# Estado de contenedores
make ps

# Logs en tiempo real
make logs

# Logs de servicio específico
docker-compose logs -f training-service

# Entrar a shell del contenedor
make shell-training
```

### Dentro del contenedor:
```bash
# Ver versiones
python --version
pip list

# Ver estructura
ls -la /app

# Ejecutar manualmente
python scripts/train.py
pytest tests/ -v
```

## 🎯 Ventajas de esta Arquitectura

✅ **Sin conflictos**: Python del contenedor ≠ Python de tu Mac
✅ **Portabilidad**: Funciona igual en cualquier máquina
✅ **Reproducibilidad**: Mismo entorno siempre
✅ **Aislamiento**: No contamina tu sistema
✅ **Escalabilidad**: Fácil escalar servicios
✅ **Hot-reload**: Cambios en código se aplican inmediatamente
✅ **Microservicios**: Cada servicio independiente

## 📚 Referencias

- **docker-compose.yml**: Define servicios, volúmenes y red
- **Dockerfile.training**: Define imagen de entrenamiento
- **Dockerfile.api**: Define imagen de API
- **Dockerfile.jupyter**: Define imagen de Jupyter
- **Makefile**: Comandos simplificados
