FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install LawMode
RUN pip install -e .

# Create artifact directories
RUN mkdir -p .lawmode/history .lawmode/reviews

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LAWMODE_ARTIFACT_DIR=/app/.lawmode

# Default command
CMD ["lawmode", "scan", "--help"]

