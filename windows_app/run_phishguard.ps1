# PhishGuard Pro Windows Application Launcher
# PowerShell Script

Write-Host "🛡️ PhishGuard Pro Windows Application" -ForegroundColor Green
Write-Host "=" * 40 -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or later from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if required packages are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import requests, tkinter" 2>$null
    Write-Host "Dependencies OK" -ForegroundColor Green
} catch {
    Write-Host "Installing required packages..." -ForegroundColor Yellow
    pip install requests
}

# Run the application
Write-Host "Starting PhishGuard Pro..." -ForegroundColor Green
python launcher.py

Read-Host "Press Enter to exit"