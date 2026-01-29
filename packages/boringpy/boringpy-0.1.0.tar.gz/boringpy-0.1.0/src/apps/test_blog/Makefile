.PHONY: help
help: ## Show this help message
	@echo "test_blog - Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ============================================================================
# Quality checks
# ============================================================================

.PHONY: format
format: ## Format code with ruff
	uv run ruff format .

.PHONY: format-check
format-check: ## Check code formatting without changes
	uv run ruff format --check .

.PHONY: lint
lint: ## Lint code with ruff
	uv run ruff check .

.PHONY: lint-fix
lint-fix: ## Lint and auto-fix issues
	uv run ruff check --fix .

.PHONY: type
type: ## Type check with ty
	uv run ty check .

.PHONY: check
check: format lint-fix type ## Run all quality checks (format, lint, type)
	@echo "✓ All quality checks passed"

# ============================================================================
# Docker commands
# ============================================================================

.PHONY: docker-build
docker-build: ## Build Docker image
	docker-compose build

.PHONY: docker-up
docker-up: ## Start containers in detached mode
	docker-compose up -d

.PHONY: docker-down
docker-down: ## Stop and remove containers
	docker-compose down

.PHONY: docker-logs
docker-logs: ## Show container logs (follow mode)
	docker-compose logs -f api

.PHONY: docker-restart
docker-restart: docker-down docker-up ## Restart all containers

.PHONY: docker-shell
docker-shell: ## Open shell in API container
	docker-compose exec api /bin/bash

.PHONY: docker-clean
docker-clean: docker-down ## Remove containers, volumes, and images
	docker-compose down -v --rmi all

.PHONY: docker-ps
docker-ps: ## Show running containers
	docker-compose ps

# ============================================================================
# Database migrations (Alembic)
# ============================================================================

.PHONY: db-create-migration
db-create-migration: ## Create new migration (usage: make db-create-migration MSG="add users table")
	@if [ -z "$(MSG)" ]; then \
		echo "Error: MSG is required"; \
		echo "Usage: make db-create-migration MSG='your message'"; \
		exit 1; \
	fi
	uv run alembic revision -m "$(MSG)"

.PHONY: db-upgrade
db-upgrade: ## Apply all pending migrations
	uv run alembic upgrade head

.PHONY: db-downgrade
db-downgrade: ## Rollback last migration
	uv run alembic downgrade -1

.PHONY: db-history
db-history: ## Show migration history
	uv run alembic history

.PHONY: db-current
db-current: ## Show current migration revision
	uv run alembic current

.PHONY: db-reset
db-reset: ## Reset database (WARNING: destroys all data)
	@echo "⚠️  WARNING: This will destroy all database data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		uv run alembic downgrade base && \
		uv run alembic upgrade head && \
		echo "✓ Database reset complete"; \
	else \
		echo "Cancelled"; \
	fi

# ============================================================================
# Testing
# ============================================================================

.PHONY: test
test: ## Run tests
	uv run pytest -v

.PHONY: test-cov
test-cov: ## Run tests with coverage report
	uv run pytest --cov=app --cov-report=term-missing --cov-report=html

.PHONY: test-watch
test-watch: ## Run tests in watch mode
	uv run pytest-watch

# ============================================================================
# Development
# ============================================================================

.PHONY: install
install: ## Install dependencies with uv
	uv sync

.PHONY: install-dev
install-dev: ## Install development dependencies
	uv sync --dev

.PHONY: dev
dev: ## Run API in development mode with hot reload
	uv run uvicorn app.main:app --reload --port 8080

.PHONY: shell
shell: ## Open Python REPL with app context
	uv run python

.PHONY: clean
clean: ## Clean cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -f .coverage

# ============================================================================
# Deployment (customize for your infrastructure)
# ============================================================================

.PHONY: deploy
deploy: ## Deploy to production (CUSTOMIZE THIS TARGET)
	@echo "⚠️  DEPLOYMENT NOT CONFIGURED"
	@echo ""
	@echo "Customize this target for your infrastructure:"
	@echo ""
	@echo "Cloud Providers:"
	@echo "  • AWS ECS:           aws ecs update-service --cluster ... --service test_blog"
	@echo "  • GCP Cloud Run:     gcloud run deploy test_blog --source . --region us-central1"
	@echo "  • Azure Container:   az containerapp update --name test_blog --resource-group ..."
	@echo ""
	@echo "Platform as a Service:"
	@echo "  • Heroku:            git push heroku main"
	@echo "  • Railway:           railway up"
	@echo "  • Fly.io:            fly deploy"
	@echo ""
	@echo "Self-hosted:"
	@echo "  • Docker Swarm:      docker stack deploy -c docker-compose.yml test_blog"
	@echo "  • Kubernetes:        kubectl apply -f k8s/"
	@echo ""
	@exit 1

.PHONY: deploy-check
deploy-check: check test ## Run all checks before deployment
	@echo "✓ Ready for deployment"