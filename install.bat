@echo off
echo ===== DNG Reader Installation =====

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python and try again.
    exit /b 1
)

echo Creating virtual environment...
if exist .venv (
    echo Virtual environment already exists.
) else (
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment.
        exit /b 1
    )
    echo Virtual environment created successfully.
)

echo Activating virtual environment...
call .venv\Scripts\activate
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment.
    exit /b 1
)

echo Installing elmclient package...
pip install elmclient
if %errorlevel% neq 0 (
    echo Error: Failed to install elmclient.
    exit /b 1
)

echo.
echo ===== Installation Complete =====
echo Virtual environment is now active and elmclient is installed.
echo To deactivate the virtual environment, type 'deactivate'
echo.