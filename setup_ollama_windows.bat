@echo off
echo This helper assumes Ollama is installed from https://ollama.com/download
echo It downloads Gemma 3 1B, which can take several minutes and requires internet.
ollama pull gemma3:1b
if errorlevel 1 (
  echo Could not download the model. Install/start Ollama and try again.
  pause
  exit /b 1
)
echo Done. Start Ollama, then run run_windows.bat in another terminal.
pause
