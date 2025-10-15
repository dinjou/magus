# Dockerfile for MAGUS
# Note: Frontend is built separately and served by Vite dev server or Nginx in production
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m -u 1000 magus && \
    mkdir -p /app && \
    chown -R magus:magus /app

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn daphne

# Copy application code
COPY --chown=magus:magus krono/ ./krono/

# Create necessary directories
RUN mkdir -p /app/krono/media /app/krono/logs /app/krono/staticfiles && \
    chown -R magus:magus /app

# Switch to non-root user
USER magus

# Collect static files
WORKDIR /app/krono

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/health/', timeout=5)" || exit 1

# Default command (can be overridden in docker-compose)
CMD ["gunicorn", "krono.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]

