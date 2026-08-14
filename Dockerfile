FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NODE_VERSION=22

# Install Node.js (needed to build the React frontend) + ffmpeg (needed for Whisper voice chat)
RUN apt-get update && apt-get install -y --no-install-recommends curl ffmpeg \
    && curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install and build the React frontend
COPY frontend/package.json frontend/package-lock.json frontend/
RUN cd frontend && npm ci
COPY frontend/ frontend/
RUN cd frontend && npm run build

# Copy the Django backend
COPY backend/ backend/

# Collect Django static files (admin assets, etc.)
RUN cd backend && python manage.py collectstatic --noinput

EXPOSE 10000

WORKDIR /app/backend

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT:-10000}"]
