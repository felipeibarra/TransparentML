# 🎓 Tarea 2: PCA - Reducción de Dimensionalidad

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

# 3. Ejecutar análisis PCA (EN CONTENEDOR)
make run-pca
```

**¡Listo!** Los resultados estarán en `results/`

---

## 📖 Documentación

### Para empezar
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** ⭐ - Comandos esenciales (EMPIEZA AQUÍ)
- **[PROJECT_ORGANIZATION.md](PROJECT_ORGANIZATION.md)** - Organización completa del proyecto

### Guías detalladas
- **[docs/guides/](docs/guides/)** - Guías de Docker y workflows
- **[docs/README.md](docs/README.md)** - Índice completo de documentación

### Documentación por carpeta
Cada carpeta tiene su propio README con diagramas:
- `src/README.md` - Módulos Python (PCA manual, visualización, API)
- `scripts/README.md` - Scripts ejecutables
- `data/README.md` - Dataset Iris
- `results/README.md` - Visualizaciones generadas
- `notebooks/README.md` - Jupyter notebooks
- `tests/README.md` - Tests unitarios

---

## 📁 Estructura del Proyecto

```
TAREA_2/
├── README.md ⭐                  # Este archivo
├── QUICK_REFERENCE.md ⭐         # Comandos rápidos
├── PROJECT_ORGANIZATION.md      # Organización del proyecto
├── Makefile ⭐                   # Comandos make
├── docker-compose.yml           # Servicios Docker
├── requirements.txt             # Dependencias Python
│
├── src/                         # Código fuente Python
│   ├── pca_manual.py           # PCA implementado manualmente
│   ├── data_loader.py          # Carga dataset Iris
│   ├── visualization.py        # Visualizaciones
│   └── api.py                  # API FastAPI
│
├── scripts/                     # Scripts ejecutables
│   └── run_pca_analysis.py     # Script principal de análisis
│
├── data/                        # Dataset Iris
├── results/                     # Visualizaciones generadas
├── notebooks/                   # Jupyter notebooks
├── tests/                       # Tests unitarios
└── docs/                        # Documentación
    ├── guides/                  # Guías de uso
    └── entrega/                 # Documentos de entrega
```

---

## 🎯 Casos de Uso Comunes

### Ejecutar análisis PCA
```bash
make up                  # Iniciar servicios si no están corriendo
make run-pca             # Ejecutar análisis PCA EN CONTENEDOR
ls results/              # Ver visualizaciones generadas
```

### Usar JupyterLab
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

El proyecto usa servicios Docker:

1. **pca-analysis** - Análisis PCA y generación de visualizaciones
2. **pca-api** (puerto 8000) - API REST con FastAPI
3. **jupyter-lab** (puerto 8888) - Análisis interactivo

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

# Análisis
make run-pca      # Ejecutar análisis PCA
make test         # Ejecutar tests

# Shell interactivo
make shell-pca    # Acceder a contenedor

# Reset
make reset-all    # 🔥 Borrar TODO y reinstalar

# Limpieza
make clean-results      # Limpiar resultados
make clean-docker       # Limpiar Docker
```

Ver todos los comandos: `make help`

---

## 📊 Dataset

**Iris Dataset**
- 150 registros de flores Iris
- 4 features: sepal length, sepal width, petal length, petal width
- 3 especies: setosa, versicolor, virginica
- Objetivo: Reducción de dimensionalidad con PCA

---

## 🎓 Sobre el Proyecto

Este proyecto es parte del **Módulo 2 - Machine Learning** del programa de Maestría en Inteligencia Artificial. Implementa:

- ✅ PCA implementado manualmente (sin sklearn)
- ✅ Comparación con sklearn PCA
- ✅ Visualizaciones 2D y 3D
- ✅ Análisis de varianza explicada
- ✅ API REST para transformaciones PCA
- ✅ Tests automatizados
- ✅ Arquitectura dockerizada

---

## 📝 Referencias de Documentación

| Necesito... | Ver... |
|-------------|--------|
| **Comandos rápidos** | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| **Workflows Docker** | [docs/guides/DOCKER_WORKFLOW.md](docs/guides/DOCKER_WORKFLOW.md) |
| **Arquitectura** | [docs/guides/ARCHITECTURE.md](docs/guides/ARCHITECTURE.md) |
| **Reset completo** | [docs/guides/RESET_GUIDE.md](docs/guides/RESET_GUIDE.md) |
| **Código fuente** | [src/README.md](src/README.md) |
| **Todo** | [PROJECT_ORGANIZATION.md](PROJECT_ORGANIZATION.md) |

---

## 🤝 Contribuir

1. Leer documentación en `docs/`
2. Seguir estructura existente
3. Ejecutar tests: `make test`
4. Actualizar documentación si es necesario

---

## 📧 Contacto

**Autor**: Felipe Ibarra  
**Versión**: 1.0.0  
**Fecha**: Enero 2025

---

**⚡ Proyecto completamente dockerizado y documentado**

Para empezar: `make help` o lee [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
