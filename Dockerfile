# Dockerfile for telegram_marketsnap_bot
# Optimized for Raspberry Pi (ARM64)

FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies required for building Python packages (especially lxml)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libffi-dev \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app

# Copy and install Python dependencies first (better layer caching)
COPY --chown=botuser:botuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=botuser:botuser . .

# Create necessary directories with correct permissions
RUN mkdir -p logs data && chown -R botuser:botuser logs data

# Switch to non-root user
USER botuser

# Command to run the bot
CMD ["python", "main.py"]
