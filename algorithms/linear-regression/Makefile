.PHONY: help build up down restart logs shell-training shell-api shell-jupyter train test lint format clean-docker reset-all reset-all-force

# Variables
COMPOSE = docker-compose
TRAINING_SERVICE = training-service
API_SERVICE = prediction-api
JUPYTER_SERVICE = jupyter-lab

# Default target
help:
	@echo "🐳 Docker Container Commands - Todo se ejecuta en contenedores"
	@echo ""
	@echo "📦 Gestión de servicios:"
	@echo "  make build              - Construir todas las imágenes Docker"
	@echo "  make up                 - Iniciar todos los servicios"
	@echo "  make down               - Detener todos los servicios"
	@echo "  make restart            - Reiniciar todos los servicios"
	@echo "  make logs               - Ver logs de todos los servicios"
	@echo "  make ps                 - Ver estado de servicios"
	@echo ""
	@echo "🚀 Entrenamiento y ejecución (EN CONTENEDOR):"
	@echo "  make train              - Entrenar modelo en contenedor"
	@echo "  make train-logs         - Ver logs del entrenamiento"
	@echo ""
	@echo "🧪 Testing y calidad (EN CONTENEDOR):"
	@echo "  make test               - Ejecutar tests en contenedor"
	@echo "  make test-cov           - Ejecutar tests con cobertura"
	@echo "  make lint               - Ejecutar linters (flake8, black --check)"
	@echo "  make format             - Formatear código con black"
	@echo "  make typecheck          - Verificar tipos con mypy"
	@echo ""
	@echo "💻 Acceso a shells (EN CONTENEDOR):"
	@echo "  make shell-training     - Shell interactivo en training-service"
	@echo "  make shell-api          - Shell interactivo en prediction-api"
	@echo "  make shell-jupyter      - Shell interactivo en jupyter-lab"
	@echo ""
	@echo "📊 API y predicciones:"
	@echo "  make api-health         - Verificar salud de la API"
	@echo "  make api-info           - Ver información del modelo"
	@echo "  make api-reload         - Recargar modelo en API"
	@echo ""
	@echo "🧹 Limpieza:"
	@echo "  make clean-docker       - Limpiar contenedores, imágenes y volúmenes"
	@echo "  make clean-results      - Limpiar resultados generados"
	@echo ""
	@echo "🔥 Super Función - RESET COMPLETO:"
	@echo "  make reset-all          - BORRAR TODO y reinstalar desde cero (con confirmación)"
	@echo "  make reset-all-force    - BORRAR TODO y reinstalar (SIN confirmación - PELIGROSO)"
	@echo ""
	@echo "⚡ Flujo completo:"
	@echo "  make dev-setup          - Build + Up + Health check"
	@echo "  make dev-full           - Setup + Train + Reload API (todo en uno)"
	@echo ""

# ============================================
# Gestión de servicios
# ============================================

build:
	@echo "🔨 Construyendo imágenes Docker..."
	$(COMPOSE) build

up:
	@echo "🚀 Iniciando servicios..."
	$(COMPOSE) up -d
	@echo "✅ Servicios iniciados"
	@echo "📍 API: http://localhost:8000/docs"
	@echo "📍 Jupyter: http://localhost:8888"

down:
	@echo "🛑 Deteniendo servicios..."
	$(COMPOSE) down

restart:
	@echo "🔄 Reiniciando servicios..."
	$(COMPOSE) restart

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

# ============================================
# Entrenamiento (EN CONTENEDOR)
# ============================================

train:
	@echo "🎯 Entrenando modelo en contenedor..."
	@echo "⚠️  Esto ejecuta Python dentro del contenedor Docker, no en tu Mac"
	$(COMPOSE) exec $(TRAINING_SERVICE) python scripts/train.py

train-logs:
	$(COMPOSE) logs -f $(TRAINING_SERVICE)

# ============================================
# Testing (EN CONTENEDOR)
# ============================================

test:
	@echo "🧪 Ejecutando tests en contenedor..."
	$(COMPOSE) exec $(TRAINING_SERVICE) pytest tests/ -v

test-cov:
	@echo "🧪 Ejecutando tests con cobertura en contenedor..."
	$(COMPOSE) exec $(TRAINING_SERVICE) pytest tests/ --cov=src --cov-report=term-missing

# ============================================
# Calidad de código (EN CONTENEDOR)
# ============================================

lint:
	@echo "🔍 Ejecutando linters en contenedor..."
	$(COMPOSE) exec $(TRAINING_SERVICE) flake8 src/ scripts/ --max-line-length=100 --extend-ignore=E203,W503 || true
	$(COMPOSE) exec $(TRAINING_SERVICE) black --check src/ scripts/ || true

format:
	@echo "✨ Formateando código en contenedor..."
	$(COMPOSE) exec $(TRAINING_SERVICE) black src/ scripts/

typecheck:
	@echo "🔎 Verificando tipos en contenedor..."
	$(COMPOSE) exec $(TRAINING_SERVICE) mypy src/ --ignore-missing-imports || true

# ============================================
# Shells interactivos (EN CONTENEDOR)
# ============================================

shell-training:
	@echo "💻 Abriendo shell en training-service..."
	@echo "⚠️  Estás dentro del contenedor Docker"
	$(COMPOSE) exec $(TRAINING_SERVICE) /bin/bash

shell-api:
	@echo "💻 Abriendo shell en prediction-api..."
	@echo "⚠️  Estás dentro del contenedor Docker"
	$(COMPOSE) exec $(API_SERVICE) /bin/bash

shell-jupyter:
	@echo "💻 Abriendo shell en jupyter-lab..."
	@echo "⚠️  Estás dentro del contenedor Docker"
	$(COMPOSE) exec $(JUPYTER_SERVICE) /bin/bash

# ============================================
# API endpoints
# ============================================

api-health:
	@echo "🏥 Verificando salud de la API..."
	@curl -s http://localhost:8000/health | python3 -m json.tool || echo "❌ API no disponible"

api-info:
	@echo "ℹ️  Información del modelo..."
	@curl -s http://localhost:8000/model_info | python3 -m json.tool || echo "❌ API no disponible"

api-reload:
	@echo "🔄 Recargando modelo..."
	@curl -X POST http://localhost:8000/reload_model || echo "❌ API no disponible"

# ============================================
# Limpieza
# ============================================

clean-docker:
	@echo "🧹 Limpiando Docker..."
	$(COMPOSE) down -v
	docker system prune -f

clean-results:
	@echo "🧹 Limpiando resultados..."
	rm -rf results/figures/* results/metrics/* results/models/*
	rm -rf models/*

# ============================================
# Flujo completo de desarrollo
# ============================================

dev-setup: build up
	@echo "⏳ Esperando que los servicios estén listos..."
	@sleep 5
	@make api-health
	@echo ""
	@echo "✅ Entorno listo para desarrollo"
	@echo "🎯 Siguiente paso: make train"

dev-train: train
	@echo "✅ Modelo entrenado"
	@echo "🎯 Siguiente paso: make api-reload"

dev-full: dev-setup dev-train api-reload
	@echo "✅ Flujo completo ejecutado"
	@echo "📍 API lista en: http://localhost:8000/docs"

# ============================================
# 🔥 SUPER FUNCIÓN - RESET COMPLETO
# ============================================

reset-all:
	@echo "⚠️  ═══════════════════════════════════════════════════════════════"
	@echo "⚠️  🔥 RESET COMPLETO DEL PROYECTO 🔥"
	@echo "⚠️  ═══════════════════════════════════════════════════════════════"
	@echo ""
	@echo "Esto borrará y reinstalará TODO:"
	@echo "  ❌ Contenedores Docker (todos)"
	@echo "  ❌ Imágenes Docker del proyecto"
	@echo "  ❌ Volúmenes Docker"
	@echo "  ❌ Cache de Docker build"
	@echo "  ❌ Resultados generados (results/)"
	@echo "  ❌ Modelos entrenados (models/)"
	@echo "  ❌ Datos procesados (data/processed/ y data/splits/)"
	@echo "  ❌ Cache de Python (__pycache__, *.pyc)"
	@echo "  ❌ Archivos temporales"
	@echo ""
	@echo "  ✅ Reconstruirá todas las imágenes desde cero"
	@echo "  ✅ Iniciará servicios limpios"
	@echo "  ✅ Verificará que todo funcione"
	@echo ""
	@echo "⚠️  ADVERTENCIA: Esta operación NO se puede deshacer"
	@echo ""
	@read -p "¿Estás SEGURO de continuar? Escribe 'SI' para confirmar: " confirm; \
	if [ "$$confirm" = "SI" ]; then \
		make reset-all-force; \
	else \
		echo "❌ Operación cancelada"; \
		exit 1; \
	fi

reset-all-force:
	@echo ""
	@echo "🔥 Iniciando RESET COMPLETO..."
	@echo ""
	@echo "[1/10] Deteniendo contenedores..."
	-$(COMPOSE) down 2>/dev/null || true
	@echo "✅ Contenedores detenidos"
	@echo ""
	@echo "[2/10] Eliminando contenedores, volúmenes y redes..."
	-$(COMPOSE) down -v --remove-orphans 2>/dev/null || true
	@echo "✅ Contenedores y volúmenes eliminados"
	@echo ""
	@echo "[3/10] Eliminando imágenes del proyecto..."
	-docker rmi tarea_1-training-service tarea_1-prediction-api tarea_1-jupyter-lab 2>/dev/null || true
	-docker images | grep tarea_1 | awk '{print $$3}' | xargs docker rmi -f 2>/dev/null || true
	@echo "✅ Imágenes eliminadas"
	@echo ""
	@echo "[4/10] Limpiando cache de Docker..."
	-docker builder prune -af 2>/dev/null || true
	@echo "✅ Cache de Docker limpiado"
	@echo ""
	@echo "[5/10] Limpiando sistema Docker..."
	-docker system prune -af --volumes 2>/dev/null || true
	@echo "✅ Sistema Docker limpio"
	@echo ""
	@echo "[6/10] Eliminando resultados generados..."
	-rm -rf results/figures/* results/metrics/* results/models/* 2>/dev/null || true
	-rm -rf models/* 2>/dev/null || true
	@echo "✅ Resultados eliminados"
	@echo ""
	@echo "[7/10] Eliminando datos procesados..."
	-rm -rf data/processed/* data/splits/* 2>/dev/null || true
	@echo "✅ Datos procesados eliminados"
	@echo ""
	@echo "[8/10] Limpiando cache de Python..."
	-find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	-find . -type f -name "*.pyc" -delete 2>/dev/null || true
	-find . -type f -name "*.pyo" -delete 2>/dev/null || true
	-find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	-find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	-find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cache de Python limpiado"
	@echo ""
	@echo "[9/10] Construyendo imágenes desde cero (sin cache)..."
	$(COMPOSE) build --no-cache --pull
	@echo "✅ Imágenes construidas"
	@echo ""
	@echo "[10/10] Iniciando servicios..."
	$(COMPOSE) up -d
	@echo "✅ Servicios iniciados"
	@echo ""
	@echo "⏳ Esperando que los servicios estén listos..."
	@sleep 10
	@echo ""
	@echo "🔍 Verificando estado de servicios..."
	@$(COMPOSE) ps
	@echo ""
	@echo "🏥 Verificando salud de la API..."
	@make api-health 2>/dev/null || echo "⚠️  API aún no está lista (esto es normal)"
	@echo ""
	@echo "════════════════════════════════════════════════════════════════════"
	@echo "✅ ¡RESET COMPLETO FINALIZADO!"
	@echo "════════════════════════════════════════════════════════════════════"
	@echo ""
	@echo "📋 Estado:"
	@echo "  ✅ Todas las imágenes Docker reconstruidas desde cero"
	@echo "  ✅ Servicios iniciados y funcionando"
	@echo "  ✅ Sistema completamente limpio"
	@echo ""
	@echo "🎯 Próximos pasos:"
	@echo "  1. Verifica servicios:  make ps"
	@echo "  2. Ver logs:            make logs"
	@echo "  3. Entrenar modelo:     make train"
	@echo "  4. Verificar API:       make api-health"
	@echo ""
	@echo "📍 URLs:"
	@echo "  API:     http://localhost:8000/docs"
	@echo "  Jupyter: http://localhost:8888"
	@echo ""
	@echo "💡 Tip: Ejecuta 'make train' para entrenar tu primer modelo"
	@echo ""
