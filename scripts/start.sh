#!/bin/bash
# Start script for MAGUS
# Auto-generates secrets if needed and starts the stack

set -e

echo "🚀 Starting MAGUS"
echo "================="
echo ""

# Generate secrets if .env doesn't exist
if [ ! -f .env ]; then
    echo "🔑 No .env found, generating secrets..."
    ./scripts/generate-secrets.sh
    echo ""
fi

# Create required directories
echo "📁 Creating directories..."
mkdir -p backups
echo ""

# Start services
echo "🐳 Starting Docker services..."
docker compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

echo ""
echo "✅ MAGUS is starting up!"
echo ""
echo "📊 Check status: docker compose ps"
echo "📝 View logs:    docker compose logs -f"
echo ""
echo "🌐 Access points:"
echo "   Frontend:  http://localhost:5173"
echo "   Backend:   http://localhost:8000"
echo "   Admin:     http://localhost:8000/admin/"
echo ""

