@echo off
echo Starting Luca AI Voice Assistant...
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python run_luca_gui.py
pause
