@echo off
REM ==============================================
REM Script de démarrage API + UI_HTML (Windows)
REM ==============================================

REM Lancer l'API FastAPI dans une nouvelle fenêtre
start cmd /k "uvicorn api.main_api:app --port 8000 --reload"

REM Attendre 2 secondes pour laisser le temps à l'API de démarrer
timeout /t 2 >nul

REM Aller dans le dossier UI et lancer le serveur web
cd ui_html

REM Lancer le serveur web dans une nouvelle fenêtre
start cmd /k "python -m http.server 8080"

REM Attendre encore 2 secondes pour que le serveur web soit prêt
timeout /t 2 >nul

REM Ouvrir automatiquement l'UI dans le navigateur par défaut
start http://localhost:8080/index.html
