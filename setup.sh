#!/bin/bash
# GST Calculator Setup Script

echo "🧮 GST Calculator Pro - Setup Script"
echo "======================================"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed"
    exit 1
fi

# Check if Node.js is installed  
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    exit 1
fi

echo "✅ Python version: $(python --version)"
echo "✅ Node.js version: $(node --version)"
echo ""

# Backend Setup
echo "🔧 Setting up Backend..."
cd backend

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Please create one using .env.example"
    echo "   cp .env.example .env"
    echo "   Then edit .env with your MongoDB connection details"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo ""

# Frontend Setup
echo "🎨 Setting up Frontend..."
cd ../frontend

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

echo ""
echo "🚀 Setup Complete!"
echo ""
echo "To start the application:"
echo "1. Backend:  cd backend && python -m uvicorn test_server:app --reload --port 8003"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo "Access at: http://localhost:3000"
echo "Admin Panel: http://localhost:3000/admin"
