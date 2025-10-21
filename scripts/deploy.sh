#!/bin/bash

# Wahida Production Deployment Script
# This script helps deploy Wahida to production using Railway

set -e

echo "🚀 Starting Wahida Production Deployment"

# Check if required environment variables are set
required_vars=("SUPABASE_URL" "SUPABASE_ANON_KEY" "GOOGLE_GEMINI_API_KEY" "POSTHOG_API_KEY")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Error: $var environment variable is not set"
        exit 1
    fi
done

echo "✅ Environment variables validated"

# Build and test locally first
echo "🔨 Building and testing locally..."

# Build API
echo "Building API..."
cd apps/api
docker build -f Dockerfile.prod -t wahida-api:latest .
cd ../..

# Build Frontend
echo "Building frontend..."
cd apps/frontend
docker build -f Dockerfile.prod -t wahida-web:latest .
cd ../..

echo "✅ Local builds completed"

# Test with production compose
echo "🧪 Testing production setup..."
docker-compose -f docker-compose.prod.yml up -d --build

echo "⏳ Waiting for services to be healthy..."
sleep 30

# Health checks
echo "🏥 Running health checks..."
if curl -f http://localhost:8000/healthz > /dev/null 2>&1; then
    echo "✅ API health check passed"
else
    echo "❌ API health check failed"
    docker-compose -f docker-compose.prod.yml logs api
    exit 1
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Web health check passed"
else
    echo "❌ Web health check failed"
    docker-compose -f docker-compose.prod.yml logs web
    exit 1
fi

echo "✅ All health checks passed"

# Stop local test
docker-compose -f docker-compose.prod.yml down

echo "🎉 Local testing completed successfully!"
echo ""
echo "📋 Next steps for production deployment:"
echo "1. Push this code to GitHub"
echo "2. Connect your GitHub repo to Railway"
echo "3. Set up Railway services:"
echo "   - PostgreSQL database"
echo "   - Redis database"
echo "   - API service (from apps/api)"
echo "   - Web service (from apps/frontend)"
echo "4. Configure environment variables in Railway dashboard"
echo "5. Deploy!"
echo ""
echo "🔗 Useful links:"
echo "- Railway: https://railway.app"
echo "- Wahida GitHub: https://github.com/noah-isme/wahida"
echo "- Supabase: https://supabase.com"
echo ""
echo "🎯 Deployment complete! Wahida is ready for production. 🚀"