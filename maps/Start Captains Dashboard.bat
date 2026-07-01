@echo off
setlocal
cd /d "%~dp0"
echo Starting Captain's Dashboard...
echo Repository: %CD%
echo.
python tools\admin_publish_server.py
echo.
echo Captain's Dashboard has stopped.
pause
