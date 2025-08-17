.PHONY: help install dev-install test test-cov lint format clean run docker-build docker-run docker-stop

# Variables
PYTHON = python
PIP = pip
PYTEST = pytest
BLACK = black
FLAKE8 = flake8
ISORT = isort

# Colores para output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Mostrar esta ayuda
	@echo "$(GREEN)Comandos disponibles:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'

install: ## Instalar dependencias básicas
	@echo "$(GREEN)Instalando dependencias...$(NC)"
	$(PIP) install -r requirements.txt

dev-install: ## Instalar dependencias de desarrollo
	@echo "$(GREEN)Instalando dependencias de desarrollo...$(NC)"
	$(PIP) install -r requirements.txt
	$(PIP) install -e ".[dev]"

test: ## Ejecutar tests
	@echo "$(GREEN)Ejecutando tests...$(NC)"
	$(PYTEST) tests/ -v

test-cov: ## Ejecutar tests con cobertura
	@echo "$(GREEN)Ejecutando tests con cobertura...$(NC)"
	$(PYTEST) tests/ -v --cov=app --cov-report=html --cov-report=term

lint: ## Ejecutar linters
	@echo "$(GREEN)Ejecutando linters...$(NC)"
	$(FLAKE8) app/ tests/
	$(ISORT) --check-only app/ tests/

format: ## Formatear código
	@echo "$(GREEN)Formateando código...$(NC)"
	$(BLACK) app/ tests/
	$(ISORT) app/ tests/

clean: ## Limpiar archivos temporales
	@echo "$(GREEN)Limpiando archivos temporales...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

run: ## Ejecutar la aplicación
	@echo "$(GREEN)Iniciando la aplicación...$(NC)"
	$(PYTHON) start.py

docker-build: ## Construir imagen Docker
	@echo "$(GREEN)Construyendo imagen Docker...$(NC)"
	docker build -t expenses-api .

docker-run: ## Ejecutar con Docker Compose
	@echo "$(GREEN)Ejecutando con Docker Compose...$(NC)"
	docker-compose up -d

docker-stop: ## Detener Docker Compose
	@echo "$(GREEN)Deteniendo Docker Compose...$(NC)"
	docker-compose down

setup: ## Configuración inicial del proyecto
	@echo "$(GREEN)Configurando proyecto...$(NC)"
	$(PYTHON) setup.py

demo: ## Ejecutar demostración completa
	@echo "$(GREEN)Ejecutando demostración...$(NC)"
	$(PYTHON) test_api.py

check: ## Verificar calidad del código
	@echo "$(GREEN)Verificando calidad del código...$(NC)"
	$(MAKE) lint
	$(MAKE) test

all: ## Ejecutar todas las verificaciones
	@echo "$(GREEN)Ejecutando todas las verificaciones...$(NC)"
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) test-cov

# Comandos específicos para Windows
ifeq ($(OS),Windows_NT)
install:
	@echo "$(GREEN)Instalando dependencias (Windows)...$(NC)"
	$(PYTHON) -m pip install -r requirements.txt

dev-install:
	@echo "$(GREEN)Instalando dependencias de desarrollo (Windows)...$(NC)"
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -e ".[dev]"

test:
	@echo "$(GREEN)Ejecutando tests (Windows)...$(NC)"
	$(PYTHON) -m pytest tests/ -v

test-cov:
	@echo "$(GREEN)Ejecutando tests con cobertura (Windows)...$(NC)"
	$(PYTHON) -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term

lint:
	@echo "$(GREEN)Ejecutando linters (Windows)...$(NC)"
	$(PYTHON) -m flake8 app/ tests/
	$(PYTHON) -m isort --check-only app/ tests/

format:
	@echo "$(GREEN)Formateando código (Windows)...$(NC)"
	$(PYTHON) -m black app/ tests/
	$(PYTHON) -m isort app/ tests/
endif
