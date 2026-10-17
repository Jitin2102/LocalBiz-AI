@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Creating Python virtual environment...
  py -m venv .venv
  if errorlevel 1 goto error
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 goto error
echo.
echo Starting LocalBiz AI at http://127.0.0.1:8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
goto end
:error
echo Setup failed. Ensure Python 3.10+ is installed and available as "py".
pause
:end
endlocal
