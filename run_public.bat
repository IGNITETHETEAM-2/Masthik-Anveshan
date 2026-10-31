@echo off
setlocal enabledelayedexpansion
title Masthik Anveshan - Public Cloud Deployment Launcher

echo =========================================================================
echo   MASTHIK ANVESHAN: PUBLIC DEPLOYMENT & LIVE ACCESS LAUNCHER
echo =========================================================================
echo.

cd /d "%~dp0"

:: Resolve Python executable
set "PY_EXE=%~dp0.python\python.exe"
if not exist "!PY_EXE!" (
    set "PY_EXE=python"
)

echo [*] Starting local AI server on port 5000...
start "Masthik Anveshan Server" cmd /k ""!PY_EXE!" "%~dp0app.py""

echo [*] Waiting 3 seconds for server initialization...
timeout /t 3 /nobreak >nul

echo [*] Establishing live public HTTPS tunnel via localhost.run...
echo [*] Your public working URL will appear below:
echo.
echo =========================================================================
echo   LIVE PUBLIC HTTPS URL:
echo =========================================================================
echo.

ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:127.0.0.1:5000 nokey@localhost.run

