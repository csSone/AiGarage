#!/bin/bash
# AiGarage Production Deployment Script

set -e

echo "🚀 Starting AiGarage production deployment..."

# Step 1: Build frontend
echo "📦 Building frontend..."
cd ../web
npm install
npm run build
cd ..

# Step 2: Copy build to nginx directory
echo "📋 Copying frontend build to nginx directory..."
mkdir -p nginx/dist
rm -rf nginx/dist/*
cp -r web/dist/* nginx/dist/

# Step 3: Build and start Docker services
echo "🐳 Building and starting Docker services..."
cd docker
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

echo "✅ Deployment complete!"
echo ""
echo "Services:"
echo "  - Frontend (via nginx): http://localhost"
echo "  - Backend API: http://localhost/api/"
echo "  - Model Server API: http://localhost/model-api/"
echo ""
echo "To view logs:"
echo "  cd docker && docker-compose logs -f"
