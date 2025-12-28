#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")
DOCKER_DIR="${PROJECT_DIR}/docker"

echo "Starting development environment..."

cd "$DOCKER_DIR"

# Stop any running containers
echo "Stopping existing containers..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

# Start development environment
echo "Starting development containers..."
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build

echo "Development environment started!"
echo "Frontend (Vite dev): http://localhost:7016"
echo "Via nginx proxy: http://localhost"
