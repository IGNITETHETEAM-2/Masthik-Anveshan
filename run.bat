@echo off
setlocal enabledelayedexpansion
title Masthik Anveshan - Advanced Brain Tumor Diagnostic Platform

echo =========================================================================
echo   MASTHIK ANVESHAN: AI Brain Tumor Segmentation & Diagnostic Intelligence
echo   PyTorch U-Net + ResNet-50 + BraTS Multimodal Engine
echo =========================================================================
echo.

:: Ensure working directory is strictly set to script's directory
cd /d "%~dp0"

:: Resolve Python executable (prefer bundled environment, fallback to system PATH)
set "PY_EXE=%~dp0.python\python.exe"
if not exist "!PY_EXE!" (
    set "PY_EXE=python"
)

echo [*] Initializing runtime: "!PY_EXE!"
echo [*] Starting unified server on http://localhost:5000 ...

start "Masthik Anveshan Server" cmd /k ""!PY_EXE!" "%~dp0app.py""

echo [*] Waiting for model engine initialization...
timeout /t 3 /nobreak >nul

echo [*] Opening clinical workstation in browser...
start http://localhost:5000

echo.
echo =========================================================================
echo   Workstation is online at: http://localhost:5000
echo   To stop the server, close the 'Masthik Anveshan Server' console window.
echo =========================================================================
echo.
