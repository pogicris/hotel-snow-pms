@echo off
REM Force Render.com deployment script for Rev9 timeline fixes

echo 🚀 Forcing Render.com deployment for Rev9 timeline fixes...
echo Local timeline shows 2 weeks correctly ✅
echo Render deployment needs to be updated 🔄
echo.

REM Step 1: Verify we're in Rev9 directory
if not exist "manage.py" (
    echo ❌ Error: Not in Rev9 directory. Please cd to Rev9 folder first.
    pause
    exit /b 1
)

REM Step 2: Show current git status
echo 📋 Current Git Status:
git status --short

REM Step 3: Add deployment timestamp
echo # 🕐 Deployment Force - %date% %time% >> DEPLOYMENT_LOG.md
echo Rev9 timeline fixes - 2 week view working locally >> DEPLOYMENT_LOG.md
echo Forcing Render rebuild to update production >> DEPLOYMENT_LOG.md
echo. >> DEPLOYMENT_LOG.md

REM Step 4: Commit and push
echo 📤 Adding deployment log and pushing to trigger rebuild...
git add DEPLOYMENT_LOG.md
git add .
git commit -m "🔄 FORCE RENDER REBUILD: Rev9 timeline 2-week fix (working locally)"

echo 🌐 Pushing to GitHub to trigger Render deployment...
git push origin main

echo.
echo ✅ Force deployment initiated!
echo.
echo 📋 Next steps:
echo 1. Go to https://dashboard.render.com
echo 2. Find your 'hotel-snow-pms-docker' service
echo 3. Watch the build logs for:
echo    - Static files collection ✅
echo    - Database migrations ✅
echo    - Build completion ✅
echo 4. Wait 2-3 minutes for full deployment
echo 5. Test: https://hotel-snow-pms-docker.onrender.com/timeline/
echo 6. Hard refresh browser (Ctrl+F5) to clear cache
echo.
echo 🎯 The timeline should now show 2 weeks on Render!

pause