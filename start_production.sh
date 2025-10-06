#!/bin/bash

echo "🐪 Starting Camel Rating System - Production Mode"
echo "================================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    print_error "Please run this script from the camel project root directory"
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p backend/uploads
mkdir -p backend/models
mkdir -p ssl

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f "env.production" ]; then
        print_status "Creating .env file from production template..."
        cp env.production .env
        print_warning "Please update .env file with your actual production values!"
    else
        print_warning "No environment file found. Using default values."
    fi
fi

# Create a simple model for testing if none exists
if [ ! -f "backend/models/camel_model.h5" ]; then
    print_status "Creating a simple test model..."
    cat > backend/models/create_test_model.py << 'EOF'
import numpy as np
import tensorflow as tf
from tensorflow import keras

# Create a simple model for testing
model = keras.Sequential([
    keras.layers.Input(shape=(224, 224, 3)),
    keras.layers.Conv2D(32, 3, activation='relu'),
    keras.layers.MaxPooling2D(),
    keras.layers.Conv2D(64, 3, activation='relu'),
    keras.layers.MaxPooling2D(),
    keras.layers.Conv2D(64, 3, activation='relu'),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(6, activation='sigmoid')  # 1 rating + 5 features
])

model.compile(optimizer='adam', loss='mse')
model.save('camel_model.h5')
print("Test model created successfully!")
EOF
    
    cd backend/models
    python3 create_test_model.py
    rm create_test_model.py
    cd ../..
    print_status "Test model created at backend/models/camel_model.h5"
fi

# Build and start services
print_status "Building and starting Docker containers..."
docker-compose down --remove-orphans
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 10

# Check service health
print_status "Checking service health..."

# Check MongoDB
if docker-compose exec -T mongodb mongosh --eval "db.runCommand('ping')" > /dev/null 2>&1; then
    print_status "✅ MongoDB is running"
else
    print_warning "⚠️  MongoDB may not be ready yet"
fi

# Check Backend
if curl -s http://localhost:8000/health > /dev/null; then
    print_status "✅ Backend API is running"
else
    print_warning "⚠️  Backend API may not be ready yet"
fi

# Check Frontend
if curl -s http://localhost:3000 > /dev/null; then
    print_status "✅ Frontend is running"
else
    print_warning "⚠️  Frontend may not be ready yet"
fi

echo ""
echo "🎉 Camel Rating System is starting up!"
echo "======================================"
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend:  http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo "📍 MongoDB:  localhost:27017"
echo ""
echo "📊 To view logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 To stop:"
echo "   docker-compose down"
echo ""
echo "🔄 To restart:"
echo "   docker-compose restart"
echo ""

# Show container status
print_status "Container Status:"
docker-compose ps
