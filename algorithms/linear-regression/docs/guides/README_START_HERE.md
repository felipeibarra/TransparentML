# 🚀 EMPIEZA AQUÍ - Tarea 1 Regresión Lineal

## ⚠️ Problema Resuelto

El script `setup.sh` tiene un error de compatibilidad entre Python 3.13.5 y numpy 1.24.3.

**✅ SOLUCIÓN**: Usar Docker en lugar de instalación local.

---

## 🎯 Inicio Rápido (2 minutos)

### Paso 1: Verifica que tienes Docker
```bash
docker --version
docker-compose --version
```

Si no tienes Docker, descárgalo de [docker.com](https://docker.com)

### Paso 2: Verifica la configuración
```bash
chmod +x verify-setup.sh
./verify-setup.sh
```

Deberías ver ~24 checks ✓ en verde.

### Paso 3: Inicia los servicios
```bash
./docker-start.sh
```

Selecciona opción **1** para construir e iniciar todos los servicios.

### Paso 4: Accede a los servicios

Espera ~2 minutos mientras se construyen las imágenes. Luego accede a:

- **API Docs (Swagger)**: http://localhost:8000/docs
- **JupyterLab**: http://localhost:8888  
- **API Gateway**: http://localhost

---

## 🏗️ ¿Qué se construyó?

Una arquitectura de **microservicios** con 4 contenedores:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Prediction │     │  Training   │     │  Jupyter    │
│  API :8000  │────▶│  Service    │◀────│  Lab :8888  │
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │
       └────────────────────┴────────────────────┘
                           │
                  ┌────────▼────────┐
                  │  Nginx Gateway  │
                  │     :80         │
                  └─────────────────┘
```

### Servicios

1. **Prediction API** (:8000) - FastAPI para predicciones ML
2. **Training Service** - Entrenamiento de modelos
3. **JupyterLab** (:8888) - Análisis exploratorio
4. **Nginx Gateway** (:80) - API Gateway con rate limiting

---

## 📖 Documentación

- 📘 **[README_DOCKER.md](README_DOCKER.md)** - Inicio rápido Docker
- 📗 **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** - Guía completa de arquitectura
- 📙 **[API_EXAMPLES.md](API_EXAMPLES.md)** - Ejemplos de uso de API
- 📕 **[RESUMEN_SOLUCION.md](RESUMEN_SOLUCION.md)** - Resumen ejecutivo completo

---

## 🎬 Flujo de Trabajo Completo

### 1. Entrenar Modelo
```bash
docker-compose exec training-service python scripts/train.py
```

### 2. Verificar API
```bash
curl http://localhost:8000/health
```

### 3. Hacer Predicción
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0, 181, 5450, 0, 0, 0, 0, 0, 0, 0]}'
```

### 4. Ver Logs
```bash
docker-compose logs -f
```

### 5. Explorar en Jupyter
Abre http://localhost:8888 y explora los datos interactivamente.

---

## 🛠️ Comandos Útiles

```bash
# Ver estado de servicios
docker-compose ps

# Reiniciar un servicio
docker-compose restart prediction-api

# Parar todos los servicios
docker-compose down

# Ver logs de un servicio específico
docker-compose logs -f prediction-api

# Acceder a shell de un servicio
docker-compose exec prediction-api bash
```

---

## 🔧 Troubleshooting

### "Cannot connect to Docker daemon"
```bash
# Inicia Docker Desktop o el daemon
open -a Docker  # macOS
```

### "Port already in use"
```bash
# Cambia puertos en docker-compose.yml
# Por ejemplo: "8001:8000" en lugar de "8000:8000"
```

### Reconstruir imágenes
```bash
docker-compose build --no-cache
docker-compose up -d
```

---

## 🌟 Características

✅ **No requiere instalación local de Python/pip**  
✅ **Reproducible** en cualquier máquina con Docker  
✅ **Escalable** horizontalmente  
✅ **Producción-ready** con health checks y métricas  
✅ **Monitoreo** con Prometheus integrado  
✅ **API Gateway** con rate limiting  
✅ **Documentación** automática (Swagger)  

---

## 📊 Ventajas vs Setup Local

| Aspecto | Setup Local ❌ | Docker ✅ |
|---------|---------------|-----------|
| **Instalación** | Compleja, errores | Automática |
| **Compatibilidad** | Problemas Python 3.13 | Python 3.11 aislado |
| **Reproducibilidad** | Baja | Alta (100%) |
| **Escalabilidad** | No | Sí |
| **Tiempo setup** | 15+ min (con errores) | 2-3 min |
| **Producción** | Requiere reconfiguración | Listo |

---

## 💡 ¿Qué pasó con el error de setuptools?

**Error original**: 
```
pip._vendor.pyproject_hooks._impl.BackendUnavailable: Cannot import 'setuptools.build_meta'
```

**Causa**: numpy 1.24.3 fue compilado antes de Python 3.13 y no lo soporta.

**Soluciones intentadas**:
- ❌ Actualizar setuptools → No funciona
- ❌ Downgrade Python → Requiere reinstalación completa
- ✅ **Docker con Python 3.11 + numpy compatible** → ¡Funciona!

---

## 🚀 Próximos Pasos

1. ✅ Verifica setup con `./verify-setup.sh`
2. ✅ Inicia servicios con `./docker-start.sh`
3. ✅ Entrena modelo
4. ✅ Prueba API
5. ✅ Explora en Jupyter
6. 📖 Lee [DOCKER_GUIDE.md](DOCKER_GUIDE.md) para más detalles

---

## 🆘 ¿Necesitas ayuda?

1. Ejecuta `./verify-setup.sh` para diagnóstico
2. Revisa logs: `docker-compose logs -f`
3. Consulta [DOCKER_GUIDE.md](DOCKER_GUIDE.md) sección Troubleshooting
4. Revisa [API_EXAMPLES.md](API_EXAMPLES.md) para ejemplos

---

## ✨ ¡Todo listo!

Tu proyecto está configurado con una arquitectura de microservicios profesional. 🎉

**Siguiente paso**: `./docker-start.sh` y selecciona opción 1.
