# 🐳 Guía de Arquitectura Docker - Tarea 1 ML

## Como usar

  # 1. Verificar setup
  ./verify-setup.sh

  # 2. Iniciar servicios
  ./docker-start.sh  # Opción 1

  # 3. Acceder a servicios
  # API: http://localhost:8000/docs
  # Jupyter: http://localhost:8888
  # Gateway: http://localhost

## 📋 Arquitectura de Microservicios

Este proyecto implementa una arquitectura de microservicios con Docker Compose que incluye:

### Servicios

#### 1. **prediction-api** (Puerto 8000)
- FastAPI service para predicciones ML
- Endpoints REST para predicciones individuales y batch
- Métricas Prometheus integradas
- Health checks automáticos

#### 2. **training-service**
- Servicio para entrenamiento de modelos
- Procesamiento de datos
- Generación de modelos persistentes

#### 3. **jupyter-lab** (Puerto 8888)
- JupyterLab para análisis exploratorio
- Acceso a datos y modelos compartidos
- Notebooks interactivos

#### 4. **nginx-gateway** (Puerto 80)
- API Gateway con Nginx
- Rate limiting
- Load balancing
- Proxy reverso para servicios

## 🚀 Inicio Rápido

### Prerequisitos
```bash
# Verificar Docker
docker --version
docker-compose --version
```

### Levantar todos los servicios
```bash
# Construir imágenes
docker-compose build

# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### Acceso a servicios

**API de Predicción:**
- Directo: http://localhost:8000
- A través de gateway: http://localhost/api/
- Documentación Swagger: http://localhost:8000/docs

**JupyterLab:**
- Directo: http://localhost:8888
- A través de gateway: http://localhost/jupyter/

**Nginx Gateway:**
- http://localhost
- Health check: http://localhost/health

## 📊 Comandos Útiles

### Gestión de servicios
```bash
# Ver estado
docker-compose ps

# Reiniciar servicio específico
docker-compose restart prediction-api

# Parar todos los servicios
docker-compose down

# Parar y eliminar volúmenes
docker-compose down -v

# Ver logs de un servicio
docker-compose logs -f prediction-api
```

### Entrenamiento de modelo
```bash
# Ejecutar entrenamiento
docker-compose exec training-service python scripts/train.py

# Ver progreso
docker-compose logs -f training-service
```

### Acceso a contenedores
```bash
# Shell en servicio de training
docker-compose exec training-service bash

# Shell en API
docker-compose exec prediction-api bash

# Shell en JupyterLab
docker-compose exec jupyter-lab bash
```

## 🔄 Flujo de Trabajo

### 1. Entrenamiento de Modelo
```bash
# Entrenar modelo
docker-compose exec training-service python scripts/train.py

# El modelo se guarda en ./models/ (compartido entre servicios)
```

### 2. Servir Predicciones
```bash
# La API carga automáticamente el último modelo de ./models/
# Recargar modelo manualmente:
curl -X POST http://localhost:8000/reload_model
```

### 3. Hacer Predicciones

**Predicción individual:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [0, 181, 5450, 0, 0, 0, 0, 0, 0, 0]
  }'
```

**Predicción batch:**
```bash
curl -X POST http://localhost:8000/batch_predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      [0, 181, 5450, 0, 0, 0, 0, 0, 0, 0],
      [0, 239, 486, 0, 0, 0, 0, 0, 0, 0]
    ]
  }'
```

### 4. Monitoreo
```bash
# Health check
curl http://localhost:8000/health

# Métricas Prometheus
curl http://localhost:8000/metrics

# Info del modelo
curl http://localhost:8000/model_info
```

## 📁 Estructura de Volúmenes

```
./data/          → Datos compartidos (training, API)
./models/        → Modelos entrenados (compartido)
./results/       → Resultados y métricas
./scripts/       → Scripts de entrenamiento
./src/           → Código fuente
./notebooks/     → Jupyter notebooks
```

## 🔧 Desarrollo

### Modo desarrollo (con hot-reload)
```bash
# API con auto-reload
docker-compose up prediction-api

# Los cambios en ./src/ se reflejan automáticamente
```

### Tests
```bash
# Ejecutar tests
docker-compose exec training-service pytest tests/

# Con cobertura
docker-compose exec training-service pytest --cov=src tests/
```

### Linting y formateo
```bash
# Black
docker-compose exec training-service black src/

# Flake8
docker-compose exec training-service flake8 src/

# MyPy
docker-compose exec training-service mypy src/
```

## 🐛 Troubleshooting

### API no carga modelo
```bash
# Verificar que existe modelo
ls -lh models/

# Verificar logs
docker-compose logs prediction-api

# Verificar permisos
docker-compose exec prediction-api ls -la /app/models
```

### Puerto ocupado
```bash
# Cambiar puertos en docker-compose.yml
# Por ejemplo, cambiar 8000:8000 a 8001:8000
```

### Reconstruir imagen
```bash
# Sin cache
docker-compose build --no-cache prediction-api

# Reconstruir todo
docker-compose build --no-cache
```

### Limpiar sistema Docker
```bash
# Eliminar contenedores parados
docker container prune

# Eliminar imágenes sin usar
docker image prune -a

# Eliminar volúmenes sin usar
docker volume prune
```

## 📈 Escalabilidad

### Escalar API horizontalmente
```bash
# Ejecutar múltiples instancias
docker-compose up -d --scale prediction-api=3

# Nginx distribuirá la carga automáticamente
```

## 🔒 Seguridad

- API tokens: Configurar en variables de entorno
- Rate limiting: Configurado en Nginx (10 req/s)
- CORS: Configurado en FastAPI
- Health checks: Automáticos cada 30s

## 📝 Variables de Entorno

Crear `.env` en la raíz del proyecto:

```env
# API Configuration
MODEL_PATH=/app/models
LOG_LEVEL=info

# Training Configuration
DATA_PATH=/app/data
RESULTS_PATH=/app/results

# Jupyter Configuration
JUPYTER_TOKEN=
JUPYTER_PASSWORD=
```

## 🎯 Mejores Prácticas

1. **Siempre usar volúmenes nombrados** para datos persistentes
2. **Logs centralizados**: `docker-compose logs -f`
3. **Health checks**: Verificar antes de enviar tráfico
4. **Separación de concerns**: Cada servicio una responsabilidad
5. **Versionado de modelos**: Guardar con timestamps

## 📚 Recursos Adicionales

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Nginx Docs](https://nginx.org/en/docs/)
- [Prometheus Metrics](https://prometheus.io/docs/concepts/metric_types/)
