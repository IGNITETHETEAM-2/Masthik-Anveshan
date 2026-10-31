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
    echo   Public URL to put in About website field:
    echo   https://a22aac9d53a20336-103-165-15-20.serveousercontent.com
    echo =========================================================================
)
pause
