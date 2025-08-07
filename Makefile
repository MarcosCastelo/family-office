.PHONY: help build up down logs clean test migrate

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs from all services
	docker-compose logs -f

logs-backend: ## Show backend logs
	docker-compose logs -f backend

logs-frontend: ## Show frontend logs
	docker-compose logs -f frontend

logs-db: ## Show database logs
	docker-compose logs -f db

clean: ## Remove all containers, networks, and volumes
	docker-compose down -v --remove-orphans
	docker system prune -f

test: ## Run tests
	docker-compose exec backend poetry run pytest

migrate: ## Run database migrations
	docker-compose exec backend poetry run flask db upgrade

migrate-create: ## Create new migration
	docker-compose exec backend poetry run flask db migrate -m "$(message)"

shell: ## Open shell in backend container
	docker-compose exec backend bash

db-shell: ## Open shell in database container
	docker-compose exec db psql -U postgres -d family_office

restart: ## Restart all services
	docker-compose restart

restart-backend: ## Restart backend service
	docker-compose restart backend

restart-frontend: ## Restart frontend service
	docker-compose restart frontend 