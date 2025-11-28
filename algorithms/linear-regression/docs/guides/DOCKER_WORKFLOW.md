# 🐳 Guía de Trabajo con Contenedores Docker

## 📌 Filosofía del Proyecto

**IMPORTANTE:** Todo el código Python se ejecuta dentro de contenedores Docker, NO en tu Mac.

### ✅ Ventajas de esta arquitectura:
- **Aislamiento completo**: Python y dependencias están en el contenedor
- **Reproducibilidad**: Mismo entorno en cualquier máquina
- **Sin conflictos**: No interfiere con tu instalación local de Python
- **Portabilidad**: Funciona igual en Mac, Linux, Windows

### ⚠️ Regla de oro:
> **Nunca ejecutes `python scripts/train.py` directamente en tu Mac**
> **Siempre usa `make train` o `docker-compose exec`**

---

## 🚀 Inicio Rápido

### 1. Primera vez - Setup completo

```bash
# Construir todas las imágenes Docker
make build

# Iniciar todos los servicios
make up

# Verificar que todo está funcionando
make ps
```

### 2. Entrenar modelo (EN CONTENEDOR)

```bash
# Entrenar modelo dentro del contenedor
make train

# Ver logs en tiempo real
make train-logs
```

### 3. Verificar resultados

```bash
# Los resultados se guardan en volúmenes compartidos
ls -lh results/models/
ls -lh results/metrics/
ls -lh results/figures/
```

---

## 📖 Comandos Principales

### Ver todos los comandos disponibles
```bash
make help
```

### Gestión de servicios

```bash
# Construir imágenes
make build

# Iniciar servicios en background
make up

# Ver estado de servicios
make ps

# Ver logs de todos los servicios
make logs

# Detener servicios
make down

# Reiniciar servicios
make restart
```

### Entrenamiento y ejecución

```bash
# Entrenar modelo (EN CONTENEDOR)
make train

# Ver logs del entrenamiento
make train-logs
```

### Testing (EN CONTENEDOR)

```bash
# Ejecutar tests
make test

# Ejecutar tests con cobertura
make test-cov
```

### Calidad de código (EN CONTENEDOR)

```bash
# Ejecutar linters
make lint

# Formatear código
make format

# Verificar tipos
make typecheck
```

### API

```bash
# Verificar salud de la API
make api-health

# Ver información del modelo cargado
make api-info

# Recargar modelo
make api-reload
```

### Acceso a shells interactivos

```bash
# Shell en training-service
make shell-training

# Shell en prediction-api
make shell-api

# Shell en jupyter-lab
make shell-jupyter
```

---

## 🔄 Flujos de Trabajo Comunes

### Flujo 1: Desarrollo completo desde cero

```bash
# 1. Construir e iniciar servicios
make dev-setup

# 2. Entrenar modelo
make train

# 3. Recargar modelo en API
make api-reload

# 4. Probar API
curl http://localhost:8000/health
```

**O en un solo comando:**
```bash
make dev-full
```

### Flujo 2: Re-entrenar modelo

```bash
# 1. Asegurarse que los servicios están corriendo
make ps

# 2. Si no están corriendo, iniciarlos
make up

# 3. Entrenar modelo
make train

# 4. Recargar en API
make api-reload
```

### Flujo 3: Desarrollo y testing

```bash
# 1. Hacer cambios en tu código (en Mac)
# Los cambios se sincronizan automáticamente con el contenedor

# 2. Ejecutar tests
make test

# 3. Ejecutar linters
make lint

# 4. Formatear código
make format

# 5. Re-entrenar si es necesario
make train
```

### Flujo 4: Debugging interactivo

```bash
# 1. Acceder a shell del contenedor
make shell-training

# 2. Dentro del contenedor, ejecutar comandos Python
python scripts/train.py
python -m pytest tests/ -v
python -c "import numpy; print(numpy.__version__)"

# 3. Salir del contenedor
exit
```

---

## 📂 Persistencia de Datos

### Volúmenes compartidos

Los siguientes directorios están compartidos entre tu Mac y los contenedores:

```
./data/          ↔️  /app/data/         (Datasets)
./results/       ↔️  /app/results/      (Métricas, figuras)
./models/        ↔️  /app/models/       (Modelos entrenados)
./src/           ↔️  /app/src/          (Código fuente - sincronizado)
./scripts/       ↔️  /app/scripts/      (Scripts - sincronizados)
```

### Cómo funciona:

1. **Editas código en tu Mac**: Los cambios se reflejan inmediatamente en el contenedor
2. **Ejecutas scripts en contenedor**: Los resultados se guardan en tu Mac
3. **Sin duplicación**: Los archivos son los mismos, solo que accesibles desde ambos lados

---

## 🎯 Ejemplos Prácticos

### Ejemplo 1: Entrenar y hacer predicciones

```bash
# Paso 1: Iniciar servicios
make up

# Paso 2: Entrenar modelo
make train

# Paso 3: Verificar que el modelo fue creado
ls -lh models/

# Paso 4: Recargar modelo en API
make api-reload

# Paso 5: Hacer predicción
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [0, 181, 5450, 0, 0, 0, 0, 0, 0, 0]
  }'
```

### Ejemplo 2: Desarrollo con hot-reload

```bash
# Paso 1: Iniciar servicios
make up

# Paso 2: Modificar código en src/models/linear_model.py
# (usa tu editor favorito en Mac)

# Paso 3: Los cambios se sincronizan automáticamente

# Paso 4: Re-entrenar con cambios
make train

# Paso 5: Verificar cambios
make test
```

### Ejemplo 3: Debugging dentro del contenedor

```bash
# Paso 1: Acceder a shell
make shell-training

# Paso 2: Dentro del contenedor, instalar herramientas adicionales si es necesario
# pip install ipdb

# Paso 3: Ejecutar script con debugger
# python -m pdb scripts/train.py

# Paso 4: Salir
exit
```

---

## 🔍 Verificación y Troubleshooting

### Verificar que Docker está corriendo

```bash
docker --version
docker-compose --version
docker ps
```

### Ver qué contenedores están corriendo

```bash
make ps
# o
docker-compose ps
```

Deberías ver:
- `ml-training-service` (running)
- `ml-prediction-api` (running)
- `ml-jupyter-lab` (running)
- `ml-nginx-gateway` (running)

### Ver logs de un servicio específico

```bash
# Training service
docker-compose logs -f training-service

# API
docker-compose logs -f prediction-api

# Todos
make logs
```

### Problemas comunes

#### "Cannot connect to Docker daemon"
```bash
# Iniciar Docker Desktop en Mac
open -a Docker
```

#### "Port already in use"
```bash
# Ver qué está usando el puerto
lsof -i :8000

# Detener servicios
make down

# O cambiar puerto en docker-compose.yml
```

#### "Container exits immediately"
```bash
# Ver logs para entender el error
docker-compose logs training-service

# Reconstruir sin cache
docker-compose build --no-cache training-service
```

#### "Changes not reflected"
```bash
# Reiniciar servicio específico
docker-compose restart training-service

# O reconstruir
make build
make restart
```

---

## 🧹 Limpieza

### Limpiar resultados generados

```bash
make clean-results
```

### Limpiar Docker completamente

```bash
# Detener y eliminar contenedores, volúmenes
make clean-docker

# Limpiar todo Docker
docker system prune -a --volumes
```

### Empezar de cero

```bash
# 1. Limpiar todo
make clean-docker
make clean-results

# 2. Reconstruir
make build

# 3. Iniciar
make up

# 4. Entrenar
make train
```

---

## 🎓 Conceptos Clave

### Docker Compose vs Docker Exec

```bash
# ❌ NO HACER: Ejecutar Python en tu Mac
python scripts/train.py

# ✅ CORRECTO: Ejecutar Python en contenedor
docker-compose exec training-service python scripts/train.py

# ✅ AÚN MEJOR: Usar Makefile
make train
```

### Volúmenes vs COPY

Los Dockerfiles usan **COPY** para copiar código en la imagen durante la construcción:
```dockerfile
COPY src/ ./src/
COPY scripts/ ./scripts/
```

El docker-compose.yml usa **volúmenes** para sincronización en tiempo real:
```yaml
volumes:
  - ./src:/app/src
  - ./scripts:/app/scripts
```

Resultado: Puedes editar código en Mac y se refleja inmediatamente en el contenedor.

### Comandos exec vs run

```bash
# exec: Ejecuta comando en contenedor EXISTENTE
docker-compose exec training-service python scripts/train.py

# run: Crea NUEVO contenedor, ejecuta comando, y lo elimina
docker-compose run --rm training-service python scripts/train.py
```

Usa `exec` para servicios que están corriendo (como training-service con `tail -f /dev/null`).

---

## 📊 Cheatsheet

```bash
# ==========================================
# SETUP INICIAL
# ==========================================
make build          # Construir imágenes
make up             # Iniciar servicios
make ps             # Ver estado

# ==========================================
# DESARROLLO DIARIO
# ==========================================
make train          # Entrenar modelo
make test           # Ejecutar tests
make lint           # Verificar código
make format         # Formatear código

# ==========================================
# DEBUGGING
# ==========================================
make shell-training # Acceder a shell
make logs           # Ver logs
make api-health     # Verificar API

# ==========================================
# LIMPIEZA
# ==========================================
make down           # Detener servicios
make clean-results  # Limpiar resultados
make clean-docker   # Limpiar Docker
```

---

## 🎯 Preguntas Frecuentes

**Q: ¿Necesito instalar Python en mi Mac?**
A: No, todo Python corre en Docker. Solo necesitas Docker Desktop.

**Q: ¿Cómo edito el código?**
A: Edita en tu Mac con tu editor favorito. Los cambios se sincronizan automáticamente.

**Q: ¿Dónde están los resultados?**
A: En `./results/`, `./models/` en tu Mac. Son volúmenes compartidos.

**Q: ¿Puedo usar JupyterLab?**
A: Sí, accede a http://localhost:8888. También corre en Docker.

**Q: ¿Cómo instalo una librería nueva?**
A: Agrégala a `requirements.txt`, luego ejecuta `make build`.

**Q: ¿El entrenamiento es lento?**
A: Docker puede ser más lento que nativo. Para producción, considera desplegar sin Docker.

---

## 📚 Recursos Adicionales

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [DOCKER_GUIDE.md](./DOCKER_GUIDE.md) - Arquitectura detallada
- [API_EXAMPLES.md](./API_EXAMPLES.md) - Ejemplos de API
- [README.md](./README.md) - Documentación principal

---

**¿Listo?** Ejecuta: `make help` 🚀
