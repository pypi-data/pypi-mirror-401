# Multi-stage Dockerfile for {{package_name}}
# Stage 1: Builder - Install dependencies
FROM python:3.13-slim AS builder

WORKDIR /app

# Install uv for fast dependency management
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Install dependencies in virtual environment
RUN uv venv && \
    . .venv/bin/activate && \
    uv sync --no-dev

# Stage 2: Runtime - Minimal production image
FROM python:3.13-slim

WORKDIR /app

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy virtual environment from builder
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

# Copy application code
COPY --chown=appuser:appuser app ./app
COPY --chown=appuser:appuser migrations ./migrations
COPY --chown=appuser:appuser alembic.ini ./

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE {{port}}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:{{port}}/api/v1/health')"

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "{{port}}"]
