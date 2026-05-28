@echo off
echo ======================================================
echo  🚀 Automated Setup: Crypto Time Series Analysis
echo ======================================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found. Attempting to install via winget...
    winget install -e --id Python.Python.3.11 --accept-package-agreements --accept-source-agreements
    if %errorlevel% neq 0 (
        echo [!] Winget failed. Please install Python 3.11+ manually from python.org.
        pause
        exit /b
    )
    echo [!] Python installed. Please restart this script.
    pause
    exit /b
)

echo [+] Python found. Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [!] Dependency installation failed.
    pause
    exit /b
)

echo [+] Everything is ready! Starting the dashboard...
python main.py
if %errorlevel% neq 0 (
    echo [!] Application crashed. Error code: %errorlevel%
)
pause
