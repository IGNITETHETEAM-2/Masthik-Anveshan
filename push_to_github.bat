@echo off
title Publish to GitHub - Masthik Anveshan
echo =========================================================================
echo   PUBLISHING TO GITHUB: IGNITETHETEAM-2 / Masthik-Anveshan
echo =========================================================================
echo.
cd /d "%~dp0"
git push -u origin master
if %errorlevel% neq 0 (
    echo.
    echo [*] Note: If the push returned 'Repository not found', please ensure
    echo     you have clicked 'Create repository' at:
    echo     https://github.com/new?name=Masthik-Anveshan
) else (
    echo.
    echo =========================================================================
    echo   [SUCCESS] Repository published successfully to GitHub!
    echo.
    echo   Stable Public Showcase URL for Repository "About" Website Field:
    echo   https://IGNITETHETEAM-2.github.io/Masthik-Anveshan/
    echo.
    echo   Dynamic Flask Workstation Cloud Deployment:
    echo   Pre-configured for Render, Railway, Fly.io, or VPS / Docker.
    echo =========================================================================
)
pause
