# PowerShell Advanced Deletion Script
Write-Host "=== Advanced Folder Deletion Tool ===" -ForegroundColor Green
Write-Host ""

# Step 1: Kill locking processes
Write-Host "Step 1: Stopping potential locking processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -match "python|searchindexer|dbsvc"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Step 2: Take ownership and delete Rev6
Write-Host "Step 2: Processing Rev6..." -ForegroundColor Yellow
if (Test-Path "Rev6") {
    try {
        takeown /f "Rev6" /r /d y | Out-Null
        icacls "Rev6" /grant administrators:F /t | Out-Null
        Remove-Item "Rev6" -Recurse -Force -ErrorAction Stop
        Write-Host "Rev6: SUCCESS - Deleted" -ForegroundColor Green
    }
    catch {
        Write-Host "Rev6: FAILED - $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "Rev6: Not found (already deleted)" -ForegroundColor Gray
}

# Step 3: Take ownership and delete Rev9
Write-Host "Step 3: Processing Rev9..." -ForegroundColor Yellow
if (Test-Path "Rev9") {
    try {
        takeown /f "Rev9" /r /d y | Out-Null
        icacls "Rev9" /grant administrators:F /t | Out-Null
        Remove-Item "Rev9" -Recurse -Force -ErrorAction Stop
        Write-Host "Rev9: SUCCESS - Deleted" -ForegroundColor Green
    }
    catch {
        Write-Host "Rev9: FAILED - $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "Rev9: Not found (already deleted)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== Deletion Complete ===" -ForegroundColor Green
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")