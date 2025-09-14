from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, sessions, files

app = FastAPI(title="IA_V3 API", version="1.0")

# Activer CORS pour permettre l'accès depuis UI_HTML
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en dev : tout autoriser, à restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(chat.router)
app.include_router(sessions.router)
app.include_router(files.router)
