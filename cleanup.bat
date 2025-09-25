@echo off
echo ========================================
echo GST Calculator - Pre-Share Cleanup
echo ========================================
echo.

echo 🔥 CRITICAL: Removing sensitive files...
if exist "backend\.env" (
    del "backend\.env"
    echo ✅ Deleted backend\.env (contained MongoDB credentials)
) else (
    echo ❌ backend\.env not found
)

echo.
echo 🧹 Removing development/test files...
for %%f in (
    "backend\check_horses.py"
    "backend\clear_database.py" 
    "backend\fix_corrupt_data.py"
    "backend\fix_live_horses.py"
    "backend\search_horses.py"
    "backend\test_improved_update_logic.py"
    "backend\test_parser_logic.py"
    "backend\test_server.py"
    "backend\test_update_logic.py"
    "backend\main_simple.py"
    "backend\cleanup_analysis.py"
) do (
    if exist %%f (
        del %%f
        echo ✅ Deleted %%f
    )
)

echo.
echo 🧹 Removing cache directories...
if exist "backend\__pycache__" (
    rmdir /s /q "backend\__pycache__"
    echo ✅ Deleted backend\__pycache__\
)

if exist "frontend\.next" (
    rmdir /s /q "frontend\.next"
    echo ✅ Deleted frontend\.next\
)

if exist "frontend\node_modules" (
    rmdir /s /q "frontend\node_modules"
    echo ✅ Deleted frontend\node_modules\
)

echo.
echo 🧹 Removing uploaded files...
if exist "backend\uploads" (
    rmdir /s /q "backend\uploads"
    mkdir "backend\uploads"
    echo ✅ Cleaned backend\uploads\
)

echo.
echo 🧹 Removing virtual environment...
if exist ".venv" (
    rmdir /s /q ".venv"
    echo ✅ Deleted .venv\
)

echo.
echo ========================================
echo ✅ CLEANUP COMPLETE!
echo ========================================
echo.
echo 📦 Your code is now safe to share!
echo 📁 Size reduced from ~200-500MB to ~5-10MB
echo.
echo 📋 Recipient setup instructions:
echo 1. Extract the zip file
echo 2. Create backend\.env with their MongoDB credentials
echo 3. Run: cd frontend ^&^& npm install
echo 4. Run: python -m venv .venv
echo 5. Run: .venv\Scripts\activate ^&^& pip install -r backend\requirements.txt
echo.
pause
