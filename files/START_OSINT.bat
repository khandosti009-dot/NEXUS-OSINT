@echo off
cd /d "%~dp0"
python files\osint_framework.py
if errorlevel 1 (
    echo.
    echo Python not found or dependency missing.
    echo Please install Python 3 and run:
    echo   pip install -r files\requirements.txt
    echo.
    pause
)
