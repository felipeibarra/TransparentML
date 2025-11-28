# 🐳 Inicio Rápido con Docker

## Solución Contenerizada - Arquitectura de Microservicios

### ⚡ Inicio en 3 comandos

```bash
# 1. Hacer ejecutable el script
chmod +x docker-start.sh

# 2. Ejecutar el script interactivo
./docker-start.sh

# 3. Seleccionar opción 1 para construir e iniciar todos los servicios
```

### 📦 Servicios Disponibles

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| **prediction-api** | 8000 | API FastAPI para predicciones ML |
| **training-service** | - | Servicio de entrenamiento de modelos |
| **jupyter-lab** | 8888 | JupyterLab para análisis |
| **nginx-gateway** | 80 | API Gateway y proxy reverso |

### 🚀 Acceso Rápido

Una vez iniciados los servicios:

- **API Swagger UI**: http://localhost:8000/docs
- **JupyterLab**: http://localhost:8888
- **API Gateway**: http://localhost
- **Health Check**: http://localhost:8000/health

### 🔧 Comandos Esenciales

```bash
# Ver estado de servicios
docker-compose ps

# Ver logs
docker-compose logs -f

# Entrenar modelo
docker-compose exec training-service python scripts/train.py

# Parar servicios
docker-compose down

# Reiniciar
docker-compose restart
```

### 🎯 Flujo de Trabajo Típico

1. **Iniciar servicios**:
   ```bash
   ./docker-start.sh
   # Seleccionar opción 1
   ```

2. **Entrenar modelo**:
   ```bash
   docker-compose exec training-service python scripts/train.py
   ```

3. **Hacer predicciones**:
   ```bash
   curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"features": [0, 181, 5450, 0, 0, 0, 0, 0, 0, 0]}'
   ```

4. **Explorar en Jupyter**:
   - Abrir http://localhost:8888
   - Los datos y modelos están en volúmenes compartidos

### 📚 Documentación Completa

Ver [DOCKER_GUIDE.md](DOCKER_GUIDE.md) para:
- Arquitectura detallada
- Troubleshooting
- Configuración avanzada
- Escalabilidad
- Mejores prácticas

### 🔥 Ventajas de esta Arquitectura

✅ **Aislamiento**: Cada servicio en su propio contenedor  
✅ **Reproducibilidad**: Mismo entorno en desarrollo y producción  
✅ **Escalabilidad**: Escala servicios independientemente  
✅ **Portabilidad**: Funciona en cualquier máquina con Docker  
✅ **Monitoring**: Métricas Prometheus integradas  
✅ **Gateway**: Nginx para load balancing y rate limiting  

### ⚠️ Solución al Error de Setup

El error de `setuptools` en el script `setup.sh` se debe a incompatibilidad entre Python 3.13 y numpy 1.24.3.

**Solución aplicada**:
- ✅ Requirements actualizados a versiones compatibles con Python 3.11+
- ✅ Dockerfiles configurados con Python 3.11
- ✅ Arquitectura de microservicios implementada
- ✅ Docker Compose configurado y listo

**Ahora usa Docker** en lugar del setup local para evitar problemas de dependencias.
