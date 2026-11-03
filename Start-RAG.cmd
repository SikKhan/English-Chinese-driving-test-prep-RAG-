@echo off
setlocal
cd /d "%~dp0"
if not exist "%~dp0.venv\Scripts\python.exe" (
    echo The project Python environment is missing. See LOCAL_RAG.md for setup.
    pause
    exit /b 1
)
"%~dp0.venv\Scripts\python.exe" "%~dp0ask_rag.py" %*
if errorlevel 1 pause
