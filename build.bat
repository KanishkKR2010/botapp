@echo off
setlocal
python -m pip install -r requirements.txt
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
python -m PyInstaller --noconfirm --clean --onedir --windowed --name PythonAI ^
  --add-data "templates;templates" ^
  --add-data "static;static" ^
  app.py
echo.
echo Build complete: dist\PythonAI\PythonAI.exe
pause
