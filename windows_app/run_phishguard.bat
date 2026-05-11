@echo off
echo Starting PhishGuard Pro Windows Application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or later
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import requests, tkinter" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install requests
)

REM Run the application
python launcher.py

pause