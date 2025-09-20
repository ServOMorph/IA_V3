@echo off
echo [INFO] Recherche des processus sur le port 8001...

:: Tuer tous les PID associés au port 8001
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8001') do (
    echo [INFO] Kill PID %%a
    taskkill /PID %%a /F >nul 2>&1
)

:: Petite pause pour laisser Windows libérer le port
timeout /t 2 >nul

:: Vérification
echo [INFO] Vérification du port 8001...
netstat -ano | findstr :8001 >nul
if %ERRORLEVEL%==0 (
    echo [ERREUR] Port 8001 encore occupé ❌
) else (
    echo [OK] Port 8001 libre ✅
)

pause