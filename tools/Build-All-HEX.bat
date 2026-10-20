@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build_all_hex.ps1" %*
set RC=%ERRORLEVEL%
echo.
echo Exit code: %RC%   (0 = all good, 1 = over the 2 KB limit, 2 = build failed)
pause
