@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title BlindSpot Workstation
set "PYTHONPATH=%~dp0;%PYTHONPATH%"

:: Resolve Python executable (prefer local venv if present)
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PY_CMD=%~dp0.venv\Scripts\python.exe"
) else if exist "%~dp0venv\Scripts\python.exe" (
    set "PY_CMD=%~dp0venv\Scripts\python.exe"
) else (
    set "PY_CMD=python"
)

"%PY_CMD%" -m blindspot.launcher %*
if errorlevel 1 (
    echo.
    echo [ERROR] BlindSpot failed to start or exited with error code %errorlevel%.
    echo Please verify Python is installed and accessible in your PATH.
    echo.
    pause
)

