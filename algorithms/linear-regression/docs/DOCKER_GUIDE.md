# GUÍA DE USO DE DOCKER - TAREA 1

## 📦 Persistencia de Datos con Docker

Esta guía explica cómo usar Docker con persistencia de datos para el proyecto de regresión lineal.

---

## 🏗️ ARQUITECTURA DE VOLÚMENES

### Tipos de Volúmenes Configurados

```
TAREA_1/
├── Bind Mounts (./:/app)       # Código fuente sincronizado
│
├── Named Volumes
│   ├── ml_data                 # Dataset y datos procesados
│   ├── ml_results              # Resultados y métricas
│   ├── ml_models               # Modelos entrenados
│   ├── pip_cache               # Cache de dependencias
│   └── jupyter_data            # Configuración de Jupyter
│
└── Network
    └── ml-network              # Red privada entre contenedores
```

### Ventajas de esta Configuración

✅ **Persistencia:** Los datos sobreviven al ciclo de vida del contenedor  
✅ **Compartición:** Datos accesibles entre múltiples contenedores  
✅ **Performance:** Volúmenes nombrados son más rápidos que bind mounts  
✅ **Portabilidad:** Fácil backup y migración  
✅ **Aislamiento:** Red privada para comunicación entre servicios

---

## 🚀 COMANDOS BÁSICOS

### 1. Construcción de Imágenes

```bash
# Construir imagen por primera vez
docker-compose build

# Reconstruir sin cache (si hay cambios en Dockerfile)
docker-compose build --no-cache

# Construir un servicio específico
docker-compose build ml-task
```

### 2. Gestión de Contenedores

```bash
# Iniciar todos los servicios
docker-compose up -d

# Iniciar servicio específico
docker-compose up -d ml-task

# Ver contenedores en ejecución
docker-compose ps

# Ver logs de un servicio
docker-compose logs -f ml-task

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (¡CUIDADO! Borra datos)
docker-compose down -v
```

### 3. Ejecución de Scripts

```bash
# Ejecutar entrenamiento
docker-compose run --rm ml-task python scripts/train.py

# Ejecutar con variables de entorno
docker-compose run --rm -e SAMPLE_SIZE=10000 ml-task python scripts/train.py

# Modo interactivo (bash)
docker-compose run --rm ml-task bash
```

### 4. Jupyter Notebook

```bash
# Iniciar Jupyter
docker-compose up jupyter

# Acceder en navegador
# URL: http://localhost:8888
# Sin contraseña por configuración

# Detener Jupyter
docker-compose stop jupyter
```

---

## 💾 GESTIÓN DE VOLÚMENES

### Listar Volúmenes

```bash
# Ver todos los volúmenes de Docker
docker volume ls

# Ver volúmenes del proyecto
docker volume ls | grep tarea1
```

### Inspeccionar Volúmenes

```bash
# Ver detalles de un volumen
docker volume inspect tarea1_ml_data

# Ver ubicación física en el host
docker volume inspect tarea1_ml_data | grep Mountpoint
```

### Backup de Volúmenes

```bash
# Backup de datos
docker run --rm -v tarea1_ml_data:/data -v $(pwd)/backup:/backup \
  alpine tar czf /backup/ml_data_backup.tar.gz -C /data .

# Backup de resultados
docker run --rm -v tarea1_ml_results:/data -v $(pwd)/backup:/backup \
  alpine tar czf /backup/ml_results_backup.tar.gz -C /data .

# Backup de modelos
docker run --rm -v tarea1_ml_models:/data -v $(pwd)/backup:/backup \
  alpine tar czf /backup/ml_models_backup.tar.gz -C /data .
```

### Restaurar Volúmenes

```bash
# Restaurar datos
docker run --rm -v tarea1_ml_data:/data -v $(pwd)/backup:/backup \
  alpine sh -c "cd /data && tar xzf /backup/ml_data_backup.tar.gz"

# Restaurar resultados
docker run --rm -v tarea1_ml_results:/data -v $(pwd)/backup:/backup \
  alpine sh -c "cd /data && tar xzf /backup/ml_results_backup.tar.gz"
```

### Limpiar Volúmenes

```bash
# Eliminar volúmenes del proyecto (datos persistentes)
docker-compose down -v

# Eliminar volúmenes huérfanos (no usados)
docker volume prune

# Eliminar volumen específico
docker volume rm tarea1_pip_cache
```

---

## 🔧 USO AVANZADO

### 1. Desarrollo con Hot Reload

El código fuente está montado con bind mount (`./:/app`), por lo que los cambios se reflejan inmediatamente:

```bash
# Iniciar contenedor en modo desarrollo
docker-compose up ml-task

# Editar archivos localmente
# Los cambios se ven dentro del contenedor automáticamente

# Ejecutar script modificado
docker-compose exec ml-task python scripts/train.py
```

### 2. Ejecutar Comandos en Contenedor en Ejecución

```bash
# Bash interactivo
docker-compose exec ml-task bash

# Python REPL
docker-compose exec ml-task python

# Ver estructura de archivos
docker-compose exec ml-task ls -la results/

# Ver métricas
docker-compose exec ml-task cat results/metrics/model_comparison.csv
```

### 3. Copiar Archivos entre Host y Contenedor

```bash
# Copiar del contenedor al host
docker cp tarea1-ml:/app/results/figures ./backup_figures/

# Copiar del host al contenedor
docker cp ./nuevo_dataset.csv tarea1-ml:/app/data/
```

### 4. Optimización de Cache

```bash
# Limpiar cache de pip dentro del contenedor
docker-compose exec ml-task pip cache purge

# Reconstruir imagen sin cache de layers
docker-compose build --no-cache --pull
```

---

## 📊 MONITOREO Y DEBUG

### Ver Uso de Recursos

```bash
# Estadísticas en tiempo real
docker stats tarea1-ml

# Uso de disco por volúmenes
docker system df -v
```

### Logs y Debugging

```bash
# Ver todos los logs
docker-compose logs

# Logs de un servicio con timestamps
docker-compose logs -f --timestamps ml-task

# Últimas 100 líneas
docker-compose logs --tail=100 ml-task

# Guardar logs en archivo
docker-compose logs ml-task > logs/docker_ml_task.log
```

### Inspeccionar Contenedor

```bash
# Información completa del contenedor
docker inspect tarea1-ml

# Variables de entorno
docker inspect tarea1-ml | grep -A 20 "Env"

# Volúmenes montados
docker inspect tarea1-ml | grep -A 10 "Mounts"
```

---

## 🔐 SEGURIDAD Y MEJORES PRÁCTICAS

### 1. Variables de Entorno Sensibles

Crear archivo `.env` (no versionado):

```bash
# .env
DB_PASSWORD=secret123
API_KEY=abc123xyz
AWS_ACCESS_KEY=AKIA...
```

Usar en docker-compose.yml:

```yaml
services:
  ml-task:
    env_file:
      - .env
```

### 2. Limitar Recursos

```yaml
services:
  ml-task:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
        reservations:
          cpus: '1.0'
          memory: 2G
```

### 3. Usuario No-Root

```dockerfile
# En Dockerfile
RUN adduser --disabled-password --gecos '' mluser
USER mluser
```

### 4. Read-Only Filesystem

```yaml
services:
  ml-task:
    read_only: true
    tmpfs:
      - /tmp
    volumes:
      - ml_results:/app/results  # Escribible
```

---

## 🛠️ TROUBLESHOOTING

### Problema: Contenedor no inicia

```bash
# Ver logs de error
docker-compose logs ml-task

# Verificar estado
docker-compose ps

# Reiniciar servicio
docker-compose restart ml-task
```

### Problema: Volúmenes vacíos

```bash
# Verificar permisos
ls -la data/ results/

# Recrear volúmenes
docker-compose down -v
docker-compose up -d
```

### Problema: Cambios en código no se reflejan

```bash
# Verificar bind mount
docker-compose exec ml-task ls -la /app/src/

# Reiniciar contenedor
docker-compose restart ml-task

# Reconstruir imagen
docker-compose up --build
```

### Problema: Puerto 8888 ocupado

```bash
# Ver qué proceso usa el puerto
lsof -i :8888

# Cambiar puerto en docker-compose.yml
ports:
  - "8889:8888"  # Host:Container
```

### Problema: Espacio en disco lleno

```bash
# Ver uso de espacio
docker system df

# Limpiar todo lo no usado
docker system prune -a --volumes

# Limpiar solo imágenes
docker image prune -a

# Limpiar solo volúmenes
docker volume prune
```

---

## 📋 COMANDOS DE MANTENIMIENTO

### Limpieza Regular

```bash
# Script de limpieza semanal
#!/bin/bash

echo "🧹 Limpiando Docker..."

# Detener contenedores
docker-compose down

# Eliminar imágenes no usadas
docker image prune -a -f

# Eliminar contenedores detenidos
docker container prune -f

# Eliminar redes no usadas
docker network prune -f

# NO eliminar volúmenes (datos persistentes)
# docker volume prune -f

echo "✅ Limpieza completada"
```

### Backup Automático

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="$HOME/backups/ml_project"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup de datos
docker run --rm -v tarea1_ml_data:/data -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/data_$DATE.tar.gz -C /data .

# Backup de resultados
docker run --rm -v tarea1_ml_results:/data -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/results_$DATE.tar.gz -C /data .

# Backup de modelos
docker run --rm -v tarea1_ml_models:/data -v $BACKUP_DIR:/backup \
  alpine tar czf /backup/models_$DATE.tar.gz -C /data .

echo "✅ Backup completado en $BACKUP_DIR"
```

---

## 🌐 CONFIGURACIÓN DE RED

### Red Personalizada

La configuración actual crea una red `ml-network` que permite:

- Comunicación entre servicios por nombre
- Aislamiento del resto de contenedores
- DNS interno automático

```bash
# Ver redes
docker network ls

# Inspeccionar red
docker network inspect tarea1_ml-network

# Contenedores conectados
docker network inspect tarea1_ml-network | grep -A 5 "Containers"
```

### Conectar Servicios Externos

```bash
# Conectar contenedor a la red
docker network connect tarea1_ml-network otro_contenedor

# Desconectar
docker network disconnect tarea1_ml-network otro_contenedor
```

---

## ✅ CHECKLIST PRE-PRODUCCIÓN

Antes de usar en producción:

- [ ] Cambiar credenciales por defecto de Jupyter
- [ ] Agregar HTTPS/SSL
- [ ] Configurar límites de recursos
- [ ] Implementar health checks
- [ ] Configurar logging centralizado
- [ ] Agregar monitoring (Prometheus/Grafana)
- [ ] Documentar disaster recovery
- [ ] Configurar backups automáticos
- [ ] Implementar secretos con Docker Secrets
- [ ] Revisar permisos de volúmenes

---

## 📚 RECURSOS ADICIONALES

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Volumes Guide](https://docs.docker.com/storage/volumes/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)

---

**Autor:** Felipe Ibarra  
**Fecha:** 27 de Noviembre, 2025  
**Proyecto:** Tarea 1 - Regresión Lineal
