@echo off
REM System Maintenance Panel Launcher
REM This script runs the System Maintenance Panel with Python

echo Starting System Maintenance Panel...
python system_maintenance_panel.py

REM If Python command fails, try py command
if errorlevel 1 (
    echo.
    echo Python command failed, trying 'py' command...
    py system_maintenance_panel.py
)

REM Pause if there was an error
if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch System Maintenance Panel
    echo Please make sure Python is installed and in your PATH
    pause
)
