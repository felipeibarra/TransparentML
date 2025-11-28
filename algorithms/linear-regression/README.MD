# 🎓 Tarea 1: Regresión Lineal - Machine Learning

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen)](https://www.docker.com/)

## ⚠️ IMPORTANTE: Arquitectura Container-First

**Este proyecto ejecuta TODO el código Python dentro de contenedores Docker, NO en tu Mac.**

---

## 🚀 Inicio Rápido (3 comandos)

```bash
# 1. Ver comandos disponibles
make help

# 2. Construir e iniciar servicios
make build && make up

# 3. Entrenar modelo (EN CONTENEDOR)
make train
```

**¡Listo!** Los resultados estarán en `results/` y `models/`

---

## 📖 Documentación

### Para empezar
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** ⭐ - Comandos esenciales (EMPIEZA AQUÍ)
- **[PROJECT_ORGANIZATION.md](PROJECT_ORGANIZATION.md)** - Organización completa del proyecto

### Guías detalladas
- **[docs/guides/](docs/guides/)** - Guías de Docker, API y workflows
- **[docs/entrega/](docs/entrega/)** - Documentos de entrega de tarea
- **[docs/README.md](docs/README.md)** - Índice completo de documentación

### Documentación por carpeta
Cada carpeta tiene su propio README con diagramas:
- `src/README.md` - Módulos Python
- `scripts/README.md` - Scripts ejecutables  
- `data/README.md` - Datasets
- `results/README.md` - Outputs generados
- `models/README.md` - Modelos ML
- `notebooks/README.md` - Jupyter notebooks
- `tests/README.md` - Tests unitarios

---

## 📁 Estructura del Proyecto

```
TAREA_1/
├── README.MD ⭐                  # Este archivo
├── QUICK_REFERENCE.md ⭐         # Comandos rápidos
├── PROJECT_ORGANIZATION.md      # Organización del proyecto
├── Makefile ⭐                   # Comandos make
├── docker-compose.yml           # Servicios Docker
├── requirements.txt             # Dependencias Python
│
├── src/                         # Código fuente Python
├── scripts/                     # Scripts ejecutables
├── data/                        # Datasets
├── results/                     # Outputs del entrenamiento
├── models/                      # Modelos ML entrenados
├── notebooks/                   # Jupyter notebooks
├── tests/                       # Tests unitarios
└── docs/                        # Documentación
    ├── guides/                  # Guías de uso
    └── entrega/                 # Documentos de entrega
```

---

## 🎯 Casos de Uso Comunes

### Entrenar un modelo
```bash
make up          # Iniciar servicios si no están corriendo
make train       # Entrenar modelo EN CONTENEDOR
ls results/      # Ver resultados
```

### Usar la API de predicciones
```bash
make up                          # Iniciar servicios
make api-health                  # Verificar API
open http://localhost:8000/docs  # Swagger UI
```

### Análisis con JupyterLab
```bash
make up                   # Iniciar servicios
open http://localhost:8888
```

### Ejecutar tests
```bash
make test         # Tests EN CONTENEDOR
make test-cov     # Con cobertura
```

---

## 🐳 Arquitectura de Contenedores

El proyecto usa 4 servicios Docker:

1. **training-service** - Entrenamiento de modelos ML
2. **prediction-api** (puerto 8000) - API REST con FastAPI
3. **jupyter-lab** (puerto 8888) - Análisis interactivo
4. **nginx-gateway** (puerto 80) - API Gateway

Todos los comandos ejecutan código **dentro de contenedores**, garantizando:
- ✅ Aislamiento del sistema host
- ✅ Reproducibilidad completa
- ✅ Sin conflictos de dependencias
- ✅ Portabilidad entre máquinas

---

## 🛠️ Comandos Principales

```bash
# Gestión
make build        # Construir imágenes Docker
make up           # Iniciar servicios
make down         # Detener servicios
make ps           # Ver estado
make logs         # Ver logs

# Desarrollo
make train        # Entrenar modelo
make test         # Ejecutar tests
make format       # Formatear código
make lint         # Verificar código

# Shell interactivo
make shell-training     # Acceder a contenedor

# API
make api-health   # Verificar API
make api-info     # Info del modelo

# Limpieza
make clean-results      # Limpiar resultados
make clean-docker       # Limpiar Docker
```

Ver todos los comandos: `make help`

---

## 📊 Dataset

**KDD Cup 1999** (10% subset)
- ~494,021 registros de conexiones de red
- 41 variables (numéricas y categóricas)
- Objetivo: Detección de intrusiones
- Ubicación: `data/raw/kddcup.data_10_percent`

---

## 🎓 Sobre el Proyecto

Este proyecto es parte del **Módulo 2 - Machine Learning** del programa de Maestría en Inteligencia Artificial. Implementa un análisis completo de regresión lineal con:

- ✅ Preprocesamiento de datos
- ✅ Múltiples modelos (Linear, Ridge, Lasso)
- ✅ Evaluación con métricas estándar
- ✅ Visualizaciones comprehensivas
- ✅ API REST para predicciones
- ✅ Arquitectura de microservicios
- ✅ Tests automatizados

---

## 📝 Referencias de Documentación

| Necesito... | Ver... |
|-------------|--------|
| **Comandos rápidos** | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| **Workflows Docker** | [docs/guides/DOCKER_WORKFLOW.md](docs/guides/DOCKER_WORKFLOW.md) |
| **Arquitectura** | [docs/guides/ARCHITECTURE.md](docs/guides/ARCHITECTURE.md) |
| **API examples** | [docs/guides/API_EXAMPLES.md](docs/guides/API_EXAMPLES.md) |
| **Setup inicial** | [docs/guides/CONTAINER_SETUP.md](docs/guides/CONTAINER_SETUP.md) |
| **Código fuente** | [src/README.md](src/README.md) |
| **Resultados** | [docs/entrega/RESULTADOS.md](docs/entrega/RESULTADOS.md) |
| **Todo** | [PROJECT_ORGANIZATION.md](PROJECT_ORGANIZATION.md) |

---

## 🤝 Contribuir

1. Leer documentación en `docs/`
2. Seguir estructura existente
3. Ejecutar tests: `make test`
4. Verificar calidad: `make lint`
5. Actualizar documentación si es necesario

---

## 📧 Contacto

**Autor**: Felipe Ibarra  
**Versión**: 1.0.0  
**Fecha**: Enero 2025

---

**⚡ Proyecto completamente dockerizado y documentado**

Para empezar: `make help` o lee [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
