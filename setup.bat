@echo off
rem GST Calculator Setup Script for Windows

echo 🧮 GST Calculator Pro - Windows Setup
echo ======================================

rem Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed
    pause
    exit /b 1
)

rem Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed
    pause
    exit /b 1
)

echo ✅ Python version: 
python --version
echo ✅ Node.js version:
node --version
echo.

rem Backend Setup
echo 🔧 Setting up Backend...
cd backend

rem Check if .env exists
if not exist ".env" (
    echo ⚠️  .env file not found. Please create one using .env.example
    echo    copy .env.example .env
    echo    Then edit .env with your MongoDB connection details
)

rem Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

echo.

rem Frontend Setup
echo 🎨 Setting up Frontend...
cd ..\frontend

rem Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
npm install

echo.
echo 🚀 Setup Complete!
echo.
echo To start the application:
echo 1. Backend:  cd backend ^&^& python -m uvicorn test_server:app --reload --port 8003
echo 2. Frontend: cd frontend ^&^& npm run dev
echo.
echo Access at: http://localhost:3000
echo Admin Panel: http://localhost:3000/admin

pause
