# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system deps required to compile mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    gcc \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose the port Gunicorn will bind to
EXPOSE 5000

# Use gunicorn for production; 3 workers is a sensible default for a small app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "3", "--threads", "2"]
