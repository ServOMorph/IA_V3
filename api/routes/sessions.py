from fastapi import APIRouter, HTTPException, Body
from core.chat_manager import ChatManager
from core.session_manager import SessionManager
from core.sav_manager import SaveManager
from config import SAVE_DIR
from pathlib import Path

router = APIRouter(prefix="/sessions", tags=["sessions"])

# Instance globale
chat_manager = ChatManager()

@router.post("/")
def new_session():
    global chat_manager
    chat_manager = ChatManager()
    print(f"[DEBUG] Session créée : {chat_manager.save_manager.session_dir.resolve()}")
    return {"session": chat_manager.save_manager.session_name}

@router.get("/")
def list_sessions():
    sessions = [d.name for d in Path(SAVE_DIR).iterdir() if d.is_dir()]
    return {"sessions": sessions}

@router.put("/{name}/rename")
def rename_session(name: str, new_name: str):
    ok = SessionManager.rename_session(chat_manager, name, new_name)
    if not ok:
        raise HTTPException(status_code=400, detail="Impossible de renommer la session")
    return {"old": name, "new": new_name}

@router.delete("/{name}")
def delete_session(name: str):
    ok = SessionManager.delete_session(chat_manager, name)
    if not ok:
        raise HTTPException(status_code=400, detail="Impossible de supprimer la session")
    return {"deleted": name}

@router.get("/{name}/history")
def get_history(name: str):
    md_file = Path(SAVE_DIR) / name / "conversation.md"
    if not md_file.exists():
        raise HTTPException(status_code=404, detail="Session introuvable")
    return {"history": md_file.read_text(encoding="utf-8")}

@router.post("/{name}/message")
def add_message(name: str, msg: dict = Body(...)):
    """
    Ajoute un message (user ou assistant) à l'historique de la session
    et déclenche la sauvegarde automatique.
    """
    global chat_manager
    if not hasattr(chat_manager, "history"):
        chat_manager.history = []

    chat_manager.history.append(msg)
    chat_manager.save_manager.save_md(chat_manager.history)

    return {"status": "ok", "count": len(chat_manager.history)}
