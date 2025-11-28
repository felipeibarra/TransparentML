# ⚡ GUÍA DE INICIO RÁPIDO

## 🚀 Setup en 1 Comando

```bash
./setup.sh
```

Esto hará automáticamente:
- ✅ Verificar prerequisitos (Python, pip, Docker)
- ✅ Crear entorno virtual
- ✅ Instalar dependencias
- ✅ Configurar directorios
- ✅ Entrenar modelos
- ✅ Generar resultados

## 📋 Opciones del Setup

```bash
# Setup completo (incluye entrenamiento)
./setup.sh

# Setup sin entrenamiento
./setup.sh --skip-training

# Limpieza completa del proyecto
./setup.sh --clean

# Limpieza sin confirmación (CUIDADO!)
./setup.sh --clean --force

# Ayuda
./setup.sh --help
```

## 🧹 Limpieza Completa

El comando `--clean` elimina:
- ❌ Entorno virtual (venv/)
- ❌ Resultados generados (results/)
- ❌ Archivos Python compilados (__pycache__, *.pyc)
- ❌ Archivos temporales (.DS_Store, *.log)
- ❌ Imágenes y volúmenes Docker (opcional)

**Se preserva:**
- ✅ Código fuente (src/, scripts/)
- ✅ Dataset (kddcup.data_10_percent)
- ✅ Documentación (*.md, docs/)
- ✅ Configuración (requirements.txt, Dockerfile)

```bash
# Limpiar y reinstalar
./setup.sh --clean && ./setup.sh
```

## ⚙️ Uso Posterior

### Activación Rápida

```bash
# Opción 1: Script de activación
./activate.sh

# Opción 2: Comando manual
source venv/bin/activate
```

### Ejecutar Entrenamiento

```bash
python scripts/train.py
```

### Ver Resultados

```bash
# Métricas
cat results/metrics/model_comparison.csv

# Visualizaciones
open results/figures/

# Métricas detalladas
cat results/metrics/detailed_metrics.json
```

### Crear Backup

```bash
./scripts/backup.sh
```

## 🐳 Uso con Docker

```bash
# Construir imagen
docker-compose build

# Entrenar modelos
docker-compose run --rm ml-task python scripts/train.py

# Jupyter Notebook
docker-compose up jupyter
# Acceder: http://localhost:8888
```

## 🛠️ Requisitos Previos

### Obligatorios
- macOS
- Python 3.8+
- pip

### Opcionales
- Docker Desktop
- Docker Compose

## 📊 Verificar Instalación

```bash
# Verificar Python
python3 --version

# Verificar pip
pip --version

# Verificar Docker (opcional)
docker --version
docker-compose --version
```

## 🆘 Problemas Comunes

### Python no encontrado
```bash
# Instalar con Homebrew
brew install python3

# O descargar desde
https://www.python.org/downloads/
```

### Permisos denegados
```bash
chmod +x setup.sh
chmod +x scripts/*.sh
```

### Dataset no encontrado
El script preguntará si deseas continuar sin el dataset.
Para descargarlo:
```bash
# Descargar desde
http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html

# Archivo: kddcup.data_10_percent.gz
# Descomprimir:
gunzip kddcup.data_10_percent.gz
```

## 📁 Estructura Generada

```
TAREA_1/
├── venv/                    # Entorno virtual
├── data/                    # Datos
├── results/
│   ├── figures/            # 8 visualizaciones PNG
│   ├── metrics/            # JSON + CSV
│   └── models/             # 4 modelos .joblib
├── src/                     # Código fuente
├── scripts/                 # Scripts ejecutables
├── docs/                    # Documentación
└── activate.sh             # Activación rápida
```

## 🎯 Comandos Útiles

```bash
# Activar entorno
./activate.sh

# Entrenar
python scripts/train.py

# Backup
./scripts/backup.sh

# Limpiar
rm -rf venv results/__pycache__

# Re-setup
./setup.sh
```

## 📚 Documentación Completa

- **README.MD** - Documentación principal
- **RESULTADOS.md** - Análisis detallado
- **ENTREGA_FINAL.md** - Resumen ejecutivo
- **docs/ARQUITECTURA.txt** - Arquitectura
- **docs/DOCKER_GUIDE.md** - Guía Docker

## ⏱️ Tiempo Estimado

- **Setup:** 3-5 minutos
- **Entrenamiento:** 30-60 segundos
- **Total:** 5-10 minutos

---

**¿Listo?** Ejecuta: `./setup.sh` 🚀
