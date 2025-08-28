@echo off
echo ========================================
echo  FORCE RENDER DEPLOYMENT - Rev9 Timeline Fix
echo ========================================
echo Local timeline shows 2 weeks correctly
echo Render deployment needs to be updated
echo.

REM Check if we're in Rev9 directory
if not exist "manage.py" (
    echo ERROR: Not in Rev9 directory
    echo Please run: cd Rev9
    pause
    exit /b 1
)

echo Step 1: Checking Git status...
git status --short

echo.
echo Step 2: Adding deployment marker...
echo # Deployment Force - %date% %time% >> DEPLOYMENT_LOG.md
echo Rev9 timeline fixes - 2 week view working locally >> DEPLOYMENT_LOG.md
echo Forcing Render rebuild to update production >> DEPLOYMENT_LOG.md
echo. >> DEPLOYMENT_LOG.md

echo.
echo Step 3: Committing changes...
git add .
git commit -m "FORCE RENDER REBUILD: Rev9 timeline 2-week fix working locally"

if %errorlevel% neq 0 (
    echo Git commit failed - checking if changes exist...
    git status
)

echo.
echo Step 4: Pushing to GitHub...
git push origin main

if %errorlevel% neq 0 (
    echo Git push failed - please check your connection and try manual push
    pause
    exit /b 1
)

echo.
echo ========================================
echo  DEPLOYMENT INITIATED SUCCESSFULLY!
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Go to: https://dashboard.render.com
echo 2. Find: hotel-snow-pms-docker service
echo 3. Watch build logs for completion
echo 4. Test: https://hotel-snow-pms-docker.onrender.com/timeline/
echo 5. Hard refresh browser (Ctrl+F5)
echo.
echo The timeline should now show 2 weeks on Render!
echo.
pause