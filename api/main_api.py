from fastapi import FastAPI
from api.routes import chat, sessions, files

app = FastAPI(title="IA_V3 API", version="1.0")

# Inclure les routers
app.include_router(chat.router)
app.include_router(sessions.router)
app.include_router(files.router)
