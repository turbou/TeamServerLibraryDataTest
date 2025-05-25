FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
    libgtk-3-0 \
    libgbm1 \
    libnotify-bin \
    libnss3 \
    libxss1 \
    xdg-utils \
    fonts-liberation \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
RUN playwright install chromium
RUN playwright install-deps
COPY . .

