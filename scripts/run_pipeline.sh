#!/bin/bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

echo "========================================"
echo "Pipeline started at $(date)"
echo "========================================"

echo "[1/3] Running DVC pipeline..."
"$PROJECT_DIR/.venv/bin/dvc" repro

echo "[2/3] Building Docker services..."
docker compose -f code/deployment/docker-compose.yml build

echo "[3/3] Starting Docker services..."
docker compose -f code/deployment/docker-compose.yml up -d

echo "========================================"
echo "Pipeline completed at $(date)"
echo "========================================"