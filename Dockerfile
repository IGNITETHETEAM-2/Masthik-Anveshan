# ============================================================================
# Masthik Anveshan - Production Dockerfile for Cloud & VPS Deployment
# Compatible with Render, Railway, Fly.io, AWS EC2, and Linux VPS
# ============================================================================

FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    FLASK_ENV=production

WORKDIR /app

# Install minimal OS dependencies required for OpenCV, PyTorch, and image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy repository application source code
COPY . /app/

# Expose server port
EXPOSE 5000

# Health check to ensure service vitality
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Launch application via Gunicorn with production worker and timeout settings
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 1 --threads 4 --timeout 120 app:app"]
