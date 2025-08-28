@echo off
title Hotel Snow PMS Setup
color 0A
echo ========================================
echo    Hotel Snow PMS - Setup and Run
echo ========================================
echo.

:: Check if we're in the right directory
if not exist "manage.py" (
    echo Error: manage.py not found!
    echo Please make sure you're running this from the hotel_pms_project directory.
    pause
    exit /b 1
)

echo [1/5] Checking Python installation...
python --version
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.10+ and try again
    pause
    exit /b 1
)

echo [2/5] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [3/5] Setting up database...
if not exist "db.sqlite3" (
    echo Creating new database...
    python manage.py migrate
    python manage.py setup_rooms
    python manage.py create_initial_users
    echo.
    echo Database setup complete!
    echo Login credentials:
    echo - Super User: superadmin / snow2024!
    echo - Admin User: admin / admin2024!
    echo - Member User: frontdesk / front2024!
    echo.
) else (
    echo Database already exists, skipping setup...
    python manage.py migrate
)

echo [4/5] Collecting static files...
python manage.py collectstatic --noinput
if %ERRORLEVEL% neq 0 (
    echo Warning: Static files collection failed, continuing anyway...
)

echo [5/5] Starting development server...
echo.
echo ========================================
echo   Hotel Snow PMS is starting...
echo   URL: http://127.0.0.1:8000
echo   
echo   Login Credentials:
echo   - Super: superadmin / snow2024!
echo   - Admin: admin / admin2024!
echo   - Member: frontdesk / front2024!
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver 127.0.0.1:8000
pause