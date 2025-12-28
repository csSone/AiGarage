#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DOCKER_DIR="${PROJECT_DIR}/docker"

echo "Building and deploying production environment..."

cd "$DOCKER_DIR"

# Stop any running containers
echo "Stopping existing containers..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

# Build frontend
echo "Building frontend..."
docker-compose -f docker-compose.prod.yml run --rm frontend-builder

# Start production environment
echo "Starting production containers..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

echo "Production environment deployed!"
echo "Frontend: http://localhost"
