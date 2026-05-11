@echo off
echo ================================================
echo   PhishGuard Pro - Quick Start for Windows
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from: https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found! Starting PhishGuard Pro...
echo.

REM Run the quick start script
python QUICK_START.py

pause