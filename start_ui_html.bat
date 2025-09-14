@echo off
REM ==============================================
REM Script de démarrage API + UI_HTML (Windows)
REM ==============================================

echo [INFO] Fermeture des anciens serveurs éventuels...

REM Fermer http.server s'il est déjà actif sur le port 8080
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080') do taskkill /PID %%a /F >nul 2>&1

REM Fermer uvicorn s'il est déjà actif sur le port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /PID %%a /F >nul 2>&1

echo [INFO] Lancement de l'API FastAPI...
start cmd /k "uvicorn api.main_api:app --port 8000 --reload"

REM Attendre un peu pour laisser l'API démarrer
timeout /t 2 >nul

echo [INFO] Lancement du serveur web UI_HTML...
cd ui_html
start cmd /k "python -m http.server 8080"

REM Attendre un peu pour laisser le serveur web démarrer
timeout /t 2 >nul

echo [INFO] Ouverture de l'UI dans le navigateur...
start http://localhost:8080/index.html

REM Revenir à la racine du projet
cd ..
