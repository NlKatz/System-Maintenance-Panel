@echo off
REM System Maintenance Panel Launcher
REM This script checks dependencies and runs the System Maintenance Panel

echo ========================================
echo   System Maintenance Panel Launcher
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python is not installed or not in PATH
        echo Please install Python from https://www.python.org/
        pause
        exit /b 1
    )
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo Checking dependencies...
echo.

REM Check if PyQt6 is installed
%PYTHON_CMD% -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo PyQt6 is not installed!
    echo Installing required dependencies...
    echo.
    %PYTHON_CMD% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        echo Please run: %PYTHON_CMD% -m pip install -r requirements.txt
        pause
        exit /b 1
    )
    echo.
    echo Dependencies installed successfully!
    echo.
) else (
    echo All dependencies are installed.
    echo.
)

echo Starting System Maintenance Panel...
echo.
%PYTHON_CMD% system_maintenance_panel.py

REM Pause if there was an error
if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch System Maintenance Panel
    pause
)
