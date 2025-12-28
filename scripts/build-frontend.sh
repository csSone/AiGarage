#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
WEB_DIR="${PROJECT_DIR}/web"
DIST_DIR="${PROJECT_DIR}/nginx/dist"

echo "Building Vue.js frontend..."

cd "$WEB_DIR"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Build for production
echo "Running build..."
npm run build

# Create target directory if it doesn't exist
mkdir -p "$DIST_DIR"

# Copy built files to nginx directory
echo "Copying built files to $DIST_DIR..."
rm -rf "$DIST_DIR"/*
cp -r dist/* "$DIST_DIR/"

echo "Build complete! Files copied to $DIST_DIR"
ls -la "$DIST_DIR"
