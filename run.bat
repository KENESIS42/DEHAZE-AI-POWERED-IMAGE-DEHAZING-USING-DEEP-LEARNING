@echo off
TITLE Dehaze Project Launcher
echo ========================================================
echo   Starting Dehaze Project (MAXIM-S2 Model Dashboard)
echo ========================================================
echo.

echo [1/2] Starting Python FastAPI Backend...
start "Dehaze Backend API" cmd /k "cd backend && set PYTHONUTF8=1 && venv310\Scripts\python.exe app.py"

echo [2/2] Starting React Frontend...
start "Dehaze Frontend" cmd /k "cd frontend && npm start"

echo.
echo All services have been launched in separate windows!
echo Waiting for services to initialize...
timeout /t 5 /nobreak >nul

echo Opening browser...
start http://localhost:3000

echo Done! You can close this window.
exit
