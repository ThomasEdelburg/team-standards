# Makefile - Einheitliche Projekt-Befehle
# Verwendung: make <target>  |  make help

# Stack-Erkennung
STACK := $(shell [ -f package.json ] && echo node || ([ -f pyproject.toml ] || [ -f requirements.txt ] && echo python || echo unknown))

.DEFAULT_GOAL := help

.PHONY: help install start stop test lint format clean backup deploy-test

## help: Zeigt diese Hilfe
help:
	@echo "Verfügbare Befehle:"
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/## /  make /' | column -t -s ':'

## install: Abhängigkeiten installieren + pre-commit setup
install:
ifeq ($(STACK),node)
	npm ci
	npx playwright install --with-deps 2>/dev/null || true
else ifeq ($(STACK),python)
	uv sync --all-extras
endif
	pre-commit install
	@echo "Install abgeschlossen"

## start: Entwicklungsserver starten
start:
ifeq ($(STACK),node)
	npm run dev
else ifeq ($(STACK),python)
	uv run uvicorn app.main:app --reload
endif

## stop: Entwicklungsserver stoppen
stop:
	@pkill -f "npm run dev" 2>/dev/null || true
	@pkill -f "uvicorn" 2>/dev/null || true
	@echo "Server gestoppt"

## test: Alle Tests mit Coverage ausführen
test:
ifeq ($(STACK),node)
	npm run test:coverage
else ifeq ($(STACK),python)
	uv run pytest --cov --cov-fail-under=90 --cov-report=term-missing
endif

## lint: Linting prüfen (ohne Fix)
lint:
ifeq ($(STACK),node)
	npm run lint
else ifeq ($(STACK),python)
	uv run ruff check .
	uv run ruff format --check .
endif

## format: Code automatisch formatieren
format:
ifeq ($(STACK),node)
	npx prettier --write .
	npm run lint -- --fix
else ifeq ($(STACK),python)
	uv run ruff format .
	uv run ruff check --fix .
endif

## backup: Datenbank-Backup erstellen
backup:
	@echo "Backup wird erstellt..."
	@mkdir -p backups
	@./scripts/backup.sh 2>/dev/null || echo "HINWEIS: scripts/backup.sh anpassen"

## deploy-test: Auf Test-System deployen
deploy-test:
	@echo "Deploy auf Test..."
	@./scripts/deploy-test.sh 2>/dev/null || echo "HINWEIS: scripts/deploy-test.sh anpassen"

## clean: Build-Artefakte und Cache löschen
clean:
ifeq ($(STACK),node)
	rm -rf node_modules/.cache dist .next coverage
else ifeq ($(STACK),python)
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov dist
endif
	@echo "Clean abgeschlossen"
