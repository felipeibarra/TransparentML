# 📁 docs/ - Documentación

## 📋 Propósito
Centro de documentación técnica, metodologías y guías del proyecto.

---

## 🗂️ Estructura

```
docs/
├── README.md               # Este archivo (índice)
├── metodologia.md          # Metodología del proyecto
├── architecture.md         # Arquitectura técnica
└── api.md                  # Documentación de API
```

---

## 📚 Navegación de Documentación

```
                    ┌─────────────────┐
                    │ README.MD (raíz)│
                    │  Punto de entrada
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ QUICK_REFERENCE │ │ DOCKER_WORKFLOW │ │ CONTAINER_SETUP │
│   Comandos      │ │   Workflows     │ │   Setup guía    │
└─────────────────┘ └─────────────────┘ └─────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  ARCHITECTURE   │ │  DOCKER_GUIDE   │ │  API_EXAMPLES   │
│   Diagramas     │ │  Microservicios │ │   API docs      │
└─────────────────┘ └─────────────────┘ └─────────────────┘
         │
         └───────────────> docs/ (Documentación técnica detallada)
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
            ┌──────────────┐ ┌──────────┐ ┌──────────────┐
            │metodologia.md│ │architecture│ │    api.md    │
            └──────────────┘ └──────────┘ └──────────────┘
```

---

## 📖 Documentos Principales

### En la raíz del proyecto

| Documento | Propósito | Audiencia |
|-----------|-----------|-----------|
| **README.MD** | Punto de entrada principal | Todos |
| **QUICK_REFERENCE.md** | Comandos esenciales | Desarrolladores |
| **DOCKER_WORKFLOW.md** | Workflows completos | Desarrolladores |
| **CONTAINER_SETUP.md** | Setup de contenedores | DevOps |
| **ARCHITECTURE.md** | Diagramas del sistema | Arquitectos |
| **DOCKER_GUIDE.md** | Guía de microservicios | DevOps |
| **API_EXAMPLES.md** | Ejemplos de API | API consumers |

### En docs/ (este directorio)

| Documento | Propósito |
|-----------|-----------|
| **metodologia.md** | Metodología ML del proyecto |
| **architecture.md** | Arquitectura técnica detallada |
| **api.md** | Documentación completa de API |

---

## 🎯 Guías por Rol

### Para Principiantes
1. Empezar con: `../README.MD`
2. Leer: `../QUICK_REFERENCE.md`
3. Probar: `make help` y `make train`

### Para Desarrolladores
1. `../DOCKER_WORKFLOW.md` - Workflows diarios
2. `src/README.md` - Estructura del código
3. `tests/README.md` - Cómo testear
4. `metodologia.md` - Enfoque ML

### Para DevOps
1. `../CONTAINER_SETUP.md` - Setup completo
2. `../ARCHITECTURE.md` - Arquitectura
3. `../DOCKER_GUIDE.md` - Microservicios
4. `docker-compose.yml` - Configuración

### Para Data Scientists
1. `notebooks/README.md` - JupyterLab
2. `data/README.md` - Datasets
3. `metodologia.md` - Metodología ML
4. `results/README.md` - Análisis de resultados

---

## 📊 Mapa del Proyecto

```
TAREA_1/
│
├── 📄 Documentación General (raíz)
│   ├── README.MD              ★ EMPEZAR AQUÍ
│   ├── QUICK_REFERENCE.md     ★ Comandos rápidos
│   ├── DOCKER_WORKFLOW.md     ★ Workflows completos
│   ├── CONTAINER_SETUP.md     Resumen setup
│   ├── ARCHITECTURE.md        Diagramas sistema
│   ├── DOCKER_GUIDE.md        Microservicios
│   └── API_EXAMPLES.md        Ejemplos API
│
├── 📁 src/ - Código fuente
│   └── README.md              Estructura módulos
│
├── 📁 scripts/ - Scripts ejecutables
│   └── README.md              Cómo ejecutar
│
├── 📁 data/ - Datasets
│   └── README.md              Estructura datos
│
├── 📁 results/ - Resultados
│   └── README.md              Outputs generados
│
├── 📁 models/ - Modelos ML
│   └── README.md              Modelos guardados
│
├── 📁 notebooks/ - Jupyter
│   └── README.md              Análisis interactivo
│
├── 📁 tests/ - Tests
│   └── README.md              Cómo testear
│
└── 📁 docs/ - Documentación técnica (AQUÍ)
    ├── README.md              Índice (este archivo)
    ├── metodologia.md         Metodología ML
    ├── architecture.md        Arquitectura técnica
    └── api.md                 Documentación API
```

---

## 🚀 Inicio Rápido por Tarea

### Quiero entrenar un modelo
```bash
# 1. Leer: QUICK_REFERENCE.md
# 2. Ejecutar:
make build && make up && make train
# 3. Ver resultados:
ls -lh results/
```

### Quiero entender el código
```bash
# 1. Leer: src/README.md
# 2. Explorar: src/*.py
# 3. Experimentar: notebooks/
```

### Quiero usar la API
```bash
# 1. Leer: API_EXAMPLES.md
# 2. Iniciar: make up
# 3. Docs: http://localhost:8000/docs
```

### Quiero contribuir
```bash
# 1. Leer: DOCKER_WORKFLOW.md
# 2. Leer: tests/README.md
# 3. Desarrollar con: make train, make test
```

---

## 📝 Crear Nueva Documentación

### Para documentos generales
Crear en raíz: `NOMBRE_DESCRIPTIVO.md`

### Para documentos técnicos
Crear en `docs/`: `tema.md`

### Para documentación de carpetas
Crear en carpeta: `carpeta/README.md`

---

## 🔍 Búsqueda Rápida

| Busco... | Ver... |
|----------|--------|
| Comandos Docker | `QUICK_REFERENCE.md` |
| Workflows completos | `DOCKER_WORKFLOW.md` |
| Arquitectura | `ARCHITECTURE.md` |
| Módulos Python | `src/README.md` |
| Entrenar modelo | `scripts/README.md` |
| Datos | `data/README.md` |
| Resultados | `results/README.md` |
| Tests | `tests/README.md` |
| API | `API_EXAMPLES.md` |
| Notebooks | `notebooks/README.md` |

---

## 🔗 Enlaces Útiles

### Documentación Externa
- [Docker Docs](https://docs.docker.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [scikit-learn Docs](https://scikit-learn.org/)
- [pandas Docs](https://pandas.pydata.org/)
- [pytest Docs](https://docs.pytest.org/)

### Dataset
- [KDD Cup 1999](http://kdd.ics.uci.edu/databases/kddcup99/)

---

**Todo documentado | Versión 1.0.0**
