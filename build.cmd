@echo off
setlocal
cd /d "%~dp0"
python scripts\build.py %*
if errorlevel 1 (
  echo Build failed. Inspect the build logs.
  pause
  exit /b 1
)
echo Build completed. The PDF is in the repository root.
pause
