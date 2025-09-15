from fastapi import APIRouter, HTTPException
from core.chat_manager import ChatManager
from pathlib import Path
from config import SAVE_DIR

router = APIRouter(prefix="/sessions", tags=["sessions"])

# Dictionnaire de ChatManager par session
chat_managers: dict[str, ChatManager] = {}

@router.post("/")
def new_session():
    cm = ChatManager()
    name = cm.save_manager.session_name
    chat_managers[name] = cm
    print(f"[DEBUG] Session créée : {cm.save_manager.session_dir.resolve()}")
    return {"session": name}

@router.get("/")
def list_sessions():
    sessions = [d.name for d in Path(SAVE_DIR).iterdir() if d.is_dir()]
    return {"sessions": sessions}

@router.get("/{name}/history")
def get_history(name: str):
    cm = chat_managers.get(name)
    if not cm:
        raise HTTPException(status_code=404, detail="Session introuvable")
    return {"history": cm.save_manager.session_dir.joinpath("conversation.md").read_text(encoding="utf-8")}
