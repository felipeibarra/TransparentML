.PHONY: help setup-all build-all up-all down-all restart-all reset-all test-all clean-all

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Project variables
PROJECT_NAME := transparentml
DOCKER_COMPOSE := docker-compose
ALGORITHMS := linear-regression pca-analysis

##@ General Commands

help: ## Show this help message
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  TransparentML - Unified Makefile$(NC)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make $(YELLOW)<target>$(NC)\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  $(YELLOW)%-25s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo ""

##@ Setup & Installation

setup-all: ## Complete project setup (first time)
	@echo "$(GREEN)Setting up TransparentML...$(NC)"
	@chmod +x scripts/*.sh
	@bash scripts/setup-all.sh

setup-dev: ## Setup development environment
	@echo "$(GREEN)Setting up development environment...$(NC)"
	@python3 -m venv venv
	@./venv/bin/pip install -r requirements-dev.txt
	@pre-commit install

install-deps: ## Install Python dependencies locally
	@echo "$(GREEN)Installing dependencies...$(NC)"
	@pip install -r requirements.txt

##@ Docker - Global Operations

build-all: ## Build all Docker images
	@echo "$(GREEN)Building all Docker images...$(NC)"
	@$(DOCKER_COMPOSE) build
	@cd algorithms/linear-regression && $(DOCKER_COMPOSE) build
	@cd algorithms/pca-analysis && $(DOCKER_COMPOSE) build

up-all: ## Start all services
	@echo "$(GREEN)Starting all services...$(NC)"
	@$(DOCKER_COMPOSE) up -d
	@echo "$(BLUE)Services running:$(NC)"
	@echo "  - API Gateway:        http://localhost"
	@echo "  - Linear Regression:  http://localhost:8001"
	@echo "  - PCA Analysis:       http://localhost:8002"
	@echo "  - Jupyter Lab:        http://localhost:8888"

down-all: ## Stop all services
	@echo "$(YELLOW)Stopping all services...$(NC)"
	@$(DOCKER_COMPOSE) down
	@cd algorithms/linear-regression && $(DOCKER_COMPOSE) down
	@cd algorithms/pca-analysis && $(DOCKER_COMPOSE) down

restart-all: down-all up-all ## Restart all services

ps-all: ## Show all running containers
	@echo "$(BLUE)Running containers:$(NC)"
	@$(DOCKER_COMPOSE) ps
	@cd algorithms/linear-regression && $(DOCKER_COMPOSE) ps
	@cd algorithms/pca-analysis && $(DOCKER_COMPOSE) ps

logs-all: ## Show logs from all services
	@$(DOCKER_COMPOSE) logs -f

##@ Algorithm-Specific Commands

up-linear-regression: ## Start Linear Regression service only
	@echo "$(GREEN)Starting Linear Regression service...$(NC)"
	@echo "$(YELLOW)Stopping conflicting gateway if running...$(NC)"
	@docker stop transparentml-gateway 2>/dev/null || true
	@cd algorithms/linear-regression && $(DOCKER_COMPOSE) up -d

down-linear-regression: ## Stop Linear Regression service
	@cd algorithms/linear-regression && $(DOCKER_COMPOSE) down

test-linear-regression: ## Run Linear Regression tests
	@echo "$(GREEN)Running Linear Regression tests...$(NC)"
	@cd algorithms/linear-regression && make test

shell-linear-regression: ## Open shell in Linear Regression container
	@cd algorithms/linear-regression && $(DOCKER_COMPOSE) exec training-service /bin/bash

logs-linear-regression: ## Show Linear Regression logs
	@cd algorithms/linear-regression && $(DOCKER_COMPOSE) logs -f

up-pca: ## Start PCA service only
	@echo "$(GREEN)Starting PCA Analysis service...$(NC)"
	@cd algorithms/pca-analysis && $(DOCKER_COMPOSE) up -d

down-pca: ## Stop PCA service
	@cd algorithms/pca-analysis && $(DOCKER_COMPOSE) down

test-pca: ## Run PCA tests
	@echo "$(GREEN)Running PCA tests...$(NC)"
	@cd algorithms/pca-analysis && make test

shell-pca: ## Open shell in PCA container
	@cd algorithms/pca-analysis && $(DOCKER_COMPOSE) exec pca-analysis /bin/bash

logs-pca: ## Show PCA logs
	@cd algorithms/pca-analysis && $(DOCKER_COMPOSE) logs -f

up-url-diagnostics: ## Start URL Diagnostics service
	@echo "$(GREEN)Starting URL Diagnostics service...$(NC)"
	@cd url-diagnostics && $(DOCKER_COMPOSE) up -d
	@echo "$(BLUE)URL Diagnostics running at: http://localhost:8003$(NC)"
	@echo "$(BLUE)Open: http://localhost:8003/static/index.html$(NC)"

down-url-diagnostics: ## Stop URL Diagnostics service
	@cd url-diagnostics && $(DOCKER_COMPOSE) down

shell-url-diagnostics: ## Open shell in URL Diagnostics container
	@docker exec -it transparentml-url-diagnostics /bin/bash

logs-url-diagnostics: ## Show URL Diagnostics logs
	@cd url-diagnostics && $(DOCKER_COMPOSE) logs -f

##@ Testing & Quality Assurance

test-all: ## Run all tests
	@echo "$(GREEN)Running all tests...$(NC)"
	@bash scripts/test-all.sh

test-unit: ## Run unit tests only
	@echo "$(GREEN)Running unit tests...$(NC)"
	@cd algorithms/linear-regression && make test-unit
	@cd algorithms/pca-analysis && make test-unit

test-integration: ## Run integration tests only
	@echo "$(GREEN)Running integration tests...$(NC)"
	@cd algorithms/linear-regression && make test-integration
	@cd algorithms/pca-analysis && make test-integration

lint-all: ## Run linting on all code
	@echo "$(GREEN)Running linters...$(NC)"
	@cd algorithms/linear-regression && make lint || true
	@cd algorithms/pca-analysis && make lint || true

type-check-all: ## Run type checking
	@echo "$(GREEN)Running type checks...$(NC)"
	@cd algorithms/linear-regression && make type-check || true
	@cd algorithms/pca-analysis && make type-check || true

coverage-all: ## Generate test coverage report
	@echo "$(GREEN)Generating coverage report...$(NC)"
	@bash scripts/coverage.sh

##@ Performance & Benchmarks

benchmark-all: ## Run performance benchmarks
	@echo "$(GREEN)Running benchmarks...$(NC)"
	@bash scripts/benchmark.sh

benchmark-vs-sklearn: ## Compare performance vs scikit-learn
	@echo "$(GREEN)Comparing with scikit-learn...$(NC)"
	@python scripts/benchmark_sklearn.py

metrics-all: ## Show all metrics
	@echo "$(BLUE)Fetching metrics...$(NC)"
	@curl -s http://localhost:8001/api/v1/linear-regression/metrics | jq
	@curl -s http://localhost:8002/api/v1/pca/explained-variance | jq

##@ Data Management

backup-data: ## Backup all datasets
	@echo "$(GREEN)Backing up datasets...$(NC)"
	@bash scripts/backup-data.sh

restore-data: ## Restore datasets from backup
	@echo "$(YELLOW)Restoring datasets...$(NC)"
	@bash scripts/restore-data.sh

clean-results: ## Clean all result files
	@echo "$(YELLOW)Cleaning results...$(NC)"
	@rm -rf algorithms/linear-regression/results/*
	@rm -rf algorithms/pca-analysis/results/*
	@echo "$(GREEN)Results cleaned$(NC)"

clean-models: ## Clean all trained models
	@echo "$(YELLOW)Cleaning models...$(NC)"
	@rm -rf algorithms/linear-regression/models/*
	@rm -rf algorithms/pca-analysis/models/*
	@echo "$(GREEN)Models cleaned$(NC)"

##@ Documentation

generate-docs: ## Generate documentation
	@echo "$(GREEN)Generating documentation...$(NC)"
	@bash scripts/generate-docs.sh

serve-docs: ## Serve documentation locally
	@echo "$(GREEN)Serving documentation at http://localhost:8080$(NC)"
	@cd docs && python3 -m http.server 8080

##@ Nuclear Reset

reset-all: ## Complete reset (WARNING: destructive)
	@echo "$(RED)⚠️  WARNING: This will DELETE everything and rebuild from scratch$(NC)"
	@echo "$(YELLOW)This includes:$(NC)"
	@echo "  - All Docker containers"
	@echo "  - All Docker images"
	@echo "  - All Docker volumes"
	@echo "  - All results and models"
	@echo "  - All processed data"
	@echo ""
	@read -p "Type 'SI' to confirm: " confirm; \
	if [ "$$confirm" = "SI" ]; then \
		$(MAKE) reset-all-force; \
	else \
		echo "$(GREEN)Reset cancelled$(NC)"; \
	fi

reset-all-force: ## Force reset without confirmation (DANGEROUS)
	@echo "$(RED)Executing nuclear reset...$(NC)"
	@echo "$(YELLOW)[1/10] Stopping all containers...$(NC)"
	@$(DOCKER_COMPOSE) down 2>/dev/null || true
	@cd algorithms/linear-regression && $(DOCKER_COMPOSE) down 2>/dev/null || true
	@cd algorithms/pca-analysis && $(DOCKER_COMPOSE) down 2>/dev/null || true
	@echo "$(YELLOW)[2/10] Removing containers...$(NC)"
	@docker ps -aq --filter "name=$(PROJECT_NAME)" | xargs -r docker rm -f 2>/dev/null || true
	@echo "$(YELLOW)[3/10] Removing images...$(NC)"
	@docker images --filter "reference=*$(PROJECT_NAME)*" -q | xargs -r docker rmi -f 2>/dev/null || true
	@echo "$(YELLOW)[4/10] Removing volumes...$(NC)"
	@docker volume ls --filter "name=$(PROJECT_NAME)" -q | xargs -r docker volume rm 2>/dev/null || true
	@echo "$(YELLOW)[5/10] Pruning Docker system...$(NC)"
	@docker system prune -f
	@echo "$(YELLOW)[6/10] Cleaning results...$(NC)"
	@$(MAKE) clean-results
	@echo "$(YELLOW)[7/10] Cleaning models...$(NC)"
	@$(MAKE) clean-models
	@echo "$(YELLOW)[8/10] Cleaning Python cache...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(YELLOW)[9/10] Rebuilding images...$(NC)"
	@$(MAKE) build-all
	@echo "$(YELLOW)[10/10] Starting services...$(NC)"
	@$(MAKE) up-all
	@echo "$(GREEN)✅ Reset complete! All services rebuilt and running.$(NC)"

##@ Utility Commands

clean-all: ## Clean all temporary files
	@echo "$(YELLOW)Cleaning temporary files...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete$(NC)"

health-check-all: ## Check health of all services
	@echo "$(BLUE)Checking service health...$(NC)"
	@bash scripts/health-check.sh

version: ## Show version information
	@echo "$(BLUE)TransparentML$(NC)"
	@echo "Version: 1.0.0"
	@echo "Python: $$(python3 --version)"
	@echo "Docker: $$(docker --version)"
	@echo "Docker Compose: $$(docker-compose --version)"

status: ## Show project status
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  TransparentML - Status$(NC)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)Docker Containers:$(NC)"
	@$(MAKE) ps-all
	@echo ""
	@echo "$(YELLOW)Docker Images:$(NC)"
	@docker images --filter "reference=*$(PROJECT_NAME)*"
	@echo ""
	@echo "$(YELLOW)Docker Volumes:$(NC)"
	@docker volume ls --filter "name=$(PROJECT_NAME)"

##@ Git & Version Control

git-setup: ## Setup git hooks and configuration
	@echo "$(GREEN)Setting up git...$(NC)"
	@pre-commit install
	@git config pull.rebase false

git-clean: ## Clean git ignored files
	@echo "$(YELLOW)Cleaning git ignored files...$(NC)"
	@git clean -fdX

##@ Quick Actions

start-complete: ## 🚀 Start ALL services with URL Diagnostics (recommended)
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  🚀 Starting TransparentML Complete Stack$(NC)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)[1/4] Creating Docker network...$(NC)"
	@docker network create transparentml-network 2>/dev/null || true
	@echo "$(YELLOW)[2/4] Building URL Diagnostics service...$(NC)"
	@cd url-diagnostics && $(DOCKER_COMPOSE) build
	@echo "$(YELLOW)[3/4] Starting URL Diagnostics...$(NC)"
	@cd url-diagnostics && $(DOCKER_COMPOSE) up -d
	@sleep 3
	@echo "$(YELLOW)[4/4] Waiting for service to be ready...$(NC)"
	@sleep 2
	@echo ""
	@echo "$(GREEN)✅ All services started successfully!$(NC)"
	@echo ""
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  📊 AVAILABLE SERVICES$(NC)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)🔍 URL DIAGNOSTICS (Main Interface)$(NC)"
	@echo "   Web Interface:  $(GREEN)http://localhost:8003/static/index.html$(NC)"
	@echo "   API Docs:       http://localhost:8003/docs"
	@echo "   Health Check:   http://localhost:8003/health"
	@echo ""
	@echo "$(YELLOW)📈 MACHINE LEARNING ALGORITHMS$(NC)"
	@echo "   Linear Reg API: http://localhost:8001  $(BLUE)(if started separately)$(NC)"
	@echo "   PCA API:        http://localhost:8002  $(BLUE)(if started separately)$(NC)"
	@echo ""
	@echo "$(YELLOW)🔬 DEVELOPMENT TOOLS$(NC)"
	@echo "   Jupyter Lab:    http://localhost:8888  $(BLUE)(if started separately)$(NC)"
	@echo "   Token:          ml-suite-2024"
	@echo ""
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  🎯 QUICK START GUIDE$(NC)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "1. Open the URL Diagnostics interface:"
	@echo "   $(GREEN)http://localhost:8003/static/index.html$(NC)"
	@echo ""
	@echo "2. Enter a URL to analyze (e.g., https://www.google.com)"
	@echo ""
	@echo "3. Watch real-time logs and get ML-powered insights!"
	@echo ""
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(YELLOW)  💡 USEFUL COMMANDS$(NC)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "  make stop-complete          - Stop all services"
	@echo "  make logs-url-diagnostics   - View logs"
	@echo "  make shell-url-diagnostics  - Enter container"
	@echo "  make status                 - Check service status"
	@echo ""
	@echo "$(GREEN)Ready to analyze URLs! 🚀$(NC)"
	@echo ""

stop-complete: ## Stop all TransparentML services
	@echo "$(YELLOW)Stopping all services...$(NC)"
	@cd url-diagnostics && $(DOCKER_COMPOSE) down 2>/dev/null || true
	@$(DOCKER_COMPOSE) down 2>/dev/null || true
	@cd algorithms/linear-regression && $(DOCKER_COMPOSE) down 2>/dev/null || true
	@cd algorithms/pca-analysis && $(DOCKER_COMPOSE) down 2>/dev/null || true
	@echo "$(GREEN)✅ All services stopped$(NC)"

restart-complete: stop-complete start-complete ## Restart all services

quick-start: setup-all build-all up-all ## Complete quick start (legacy)
	@echo "$(GREEN)✅ Quick start complete!$(NC)"
	@echo "$(BLUE)Access your services:$(NC)"
	@echo "  - Linear Regression: http://localhost:8001"
	@echo "  - PCA Analysis:      http://localhost:8002"
	@echo "  - Jupyter Lab:       http://localhost:8888"

quick-test: ## Quick test of all services
	@echo "$(GREEN)Running quick tests...$(NC)"
	@curl -s http://localhost:8001/health || echo "$(RED)Linear Regression service not available$(NC)"
	@curl -s http://localhost:8002/health || echo "$(RED)PCA service not available$(NC)"
	@echo "$(GREEN)Quick test complete$(NC)"

demo: ## Run demo notebook
	@echo "$(GREEN)Opening demo notebook...$(NC)"
	@echo "$(BLUE)Visit: http://localhost:8888$(NC)"
	@echo "$(YELLOW)Open: examples/quick-predictions.ipynb$(NC)"

##@ Development

dev-setup: setup-all setup-dev ## Complete development setup
	@echo "$(GREEN)✅ Development environment ready!$(NC)"

dev-rebuild: down-all build-all up-all ## Rebuild for development
	@echo "$(GREEN)✅ Development rebuild complete!$(NC)"

dev-logs: ## Tail all logs for development
	@$(DOCKER_COMPOSE) logs -f --tail=100

##@ Production

prod-build: ## Build for production
	@echo "$(GREEN)Building for production...$(NC)"
	@ENVIRONMENT=production $(DOCKER_COMPOSE) -f docker-compose.prod.yml build

prod-up: ## Start production services
	@echo "$(GREEN)Starting production services...$(NC)"
	@$(DOCKER_COMPOSE) -f docker-compose.prod.yml up -d

prod-down: ## Stop production services
	@$(DOCKER_COMPOSE) -f docker-compose.prod.yml down

prod-logs: ## Show production logs
	@$(DOCKER_COMPOSE) -f docker-compose.prod.yml logs -f
