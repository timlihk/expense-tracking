# T&E Master Ledger - Development Makefile

.PHONY: dev migrate run lint test install clean

# Development server with auto-reload
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run database migrations
migrate:
	alembic upgrade head

# Production server
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

# Lint code with ruff
lint:
	ruff check app/
	ruff format app/ --check

# Run tests with pytest
test:
	pytest -v

# Install dependencies
install:
	pip install -r requirements.txt

# Clean cache and temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Development setup (install + migrate)
setup: install migrate
	@echo "✅ Development environment ready!"

# Health check
health:
	@curl -s http://localhost:8000/health | python -m json.tool || echo "❌ Server not running"

# Show help
help:
	@echo "Available targets:"
	@echo "  dev      - Start development server with auto-reload"
	@echo "  migrate  - Run database migrations"
	@echo "  run      - Start production server"
	@echo "  lint     - Check code formatting and style"
	@echo "  test     - Run test suite"
	@echo "  install  - Install Python dependencies"
	@echo "  setup    - Full development setup (install + migrate)"
	@echo "  clean    - Remove cache and temporary files"
	@echo "  health   - Check if server is running"
	@echo "  help     - Show this help message"
