#!/bin/bash

# Camel Rating System Deployment Script
# This script helps deploy the application to AWS EC2

set -e

echo "🐪 Camel Rating System Deployment Script"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_status "Docker and Docker Compose are installed"
}

# Install Docker on Ubuntu/Debian
install_docker_ubuntu() {
    print_status "Installing Docker on Ubuntu/Debian..."
    
    # Update package index
    sudo apt-get update
    
    # Install required packages
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Set up stable repository
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Install Docker Engine
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io
    
    # Install Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    # Add current user to docker group
    sudo usermod -aG docker $USER
    
    print_status "Docker installation completed. Please log out and log back in for group changes to take effect."
}

# Install Docker on Amazon Linux
install_docker_amazon() {
    print_status "Installing Docker on Amazon Linux..."
    
    # Update package index
    sudo yum update -y
    
    # Install Docker
    sudo yum install -y docker
    
    # Start Docker service
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # Add current user to docker group
    sudo usermod -a -G docker ec2-user
    
    # Install Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    print_status "Docker installation completed. Please log out and log back in for group changes to take effect."
}

# Deploy the application
deploy_app() {
    print_status "Deploying Camel Rating System..."
    
    # Create necessary directories
    mkdir -p backend/uploads
    mkdir -p backend/models
    
    # Build and start services
    docker-compose up --build -d
    
    print_status "Application deployed successfully!"
    print_status "Services are starting up..."
    
    # Wait for services to be ready
    sleep 30
    
    # Check service health
    check_services
}

# Check if services are running
check_services() {
    print_status "Checking service health..."
    
    # Check MongoDB
    if docker-compose exec -T mongodb mongosh --eval "db.runCommand('ping')" > /dev/null 2>&1; then
        print_status "✅ MongoDB is running"
    else
        print_warning "⚠️  MongoDB is not responding"
    fi
    
    # Check Backend
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_status "✅ Backend API is running"
    else
        print_warning "⚠️  Backend API is not responding"
    fi
    
    # Check Frontend
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        print_status "✅ Frontend is running"
    else
        print_warning "⚠️  Frontend is not responding"
    fi
}

# Show deployment information
show_info() {
    echo ""
    echo "🎉 Deployment Complete!"
    echo "======================"
    echo ""
    echo "Your Camel Rating System is now running:"
    echo "• Frontend: http://localhost:3000"
    echo "• Backend API: http://localhost:8000"
    echo "• API Documentation: http://localhost:8000/docs"
    echo ""
    echo "Demo Account:"
    echo "• Email: demo@camelrating.com"
    echo "• Password: demo123"
    echo ""
    echo "Useful Commands:"
    echo "• View logs: docker-compose logs -f"
    echo "• Stop services: docker-compose down"
    echo "• Restart services: docker-compose restart"
    echo "• Update application: docker-compose pull && docker-compose up -d"
    echo ""
}

# Main deployment function
main() {
    case "${1:-deploy}" in
        "install-docker-ubuntu")
            install_docker_ubuntu
            ;;
        "install-docker-amazon")
            install_docker_amazon
            ;;
        "deploy")
            check_docker
            deploy_app
            show_info
            ;;
        "check")
            check_services
            ;;
        *)
            echo "Usage: $0 {deploy|install-docker-ubuntu|install-docker-amazon|check}"
            echo ""
            echo "Commands:"
            echo "  deploy                 - Deploy the application (default)"
            echo "  install-docker-ubuntu  - Install Docker on Ubuntu/Debian"
            echo "  install-docker-amazon  - Install Docker on Amazon Linux"
            echo "  check                  - Check service health"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
