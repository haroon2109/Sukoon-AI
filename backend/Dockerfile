# Use Python 3.11 slim image for minimal footprint
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Create final image
FROM python:3.11-slim

WORKDIR /app

# Optimize memory allocation and thread limits for constrained environments (e.g., Render Free Tier 512MB)
ENV MALLOC_ARENA_MAX=2
ENV MAX_CONCURRENCY=1
ENV OMP_NUM_THREADS=1
ENV OPENBLAS_NUM_THREADS=1
ENV MKL_NUM_THREADS=1


# Install runtime dependencies required by OpenCV and PaddleOCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . /app

# Expose port
EXPOSE 8000

# Run FastAPI using Uvicorn
# Limit workers to 1 or 2 for free-tier constraints (e.g., 512MB RAM)
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"
