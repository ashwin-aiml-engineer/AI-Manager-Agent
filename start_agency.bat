@echo off
TITLE The Sovereign AI Agency - Auto Launcher
COLOR 0A

:: ====================================================
:: 1. CHECK FOR OLLAMA (The Brain)
:: ====================================================
echo [1/4] Checking AI Core (Ollama)...
tasklist /FI "IMAGENAME eq ollama_app.exe" 2>NUL | find /I /N "ollama_app.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo    - Ollama is already running. Good.
) else (
    echo    - Ollama is sleeping. Waking it up...
    :: Start Ollama hidden in background
    start /B ollama serve
    timeout /t 5 >nul
)

:: ====================================================
:: 2. ACTIVATE CONDA ENVIRONMENT
:: ====================================================
echo [2/4] Activating Neural Pathways (Conda)...
:: This command finds Conda even if you installed it in a weird place
call "C:\Users\DELL\miniconda3\Scripts\activate.bat" ai_manager

:: ====================================================
:: 3. SYSTEM DIAGNOSTICS
:: ====================================================
echo [3/4] Running System Checks...
python -c "import torch; print(f'   - PyTorch Engine: {torch.__version__}')"
python -c "import whisper; print(f'   - Voice Engine: Online')"

:: ====================================================
:: 4. LAUNCH INTERFACE
:: ====================================================
echo [4/4] Launching Central Command...
echo.
echo ==================================================
echo    SOVEREIGN AI AGENCY IS LIVE
echo    Access UI at: http://localhost:8501
echo    (Close this window to shut down the agency)
echo ==================================================
echo.

streamlit run app.py

pause