from fastapi import APIRouter, HTTPException
from core.chat_manager import ChatManager
from pathlib import Path
from config import SAVE_DIR, LOGS_DIR
import shutil
import logging

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

@router.put("/{name}/rename")
def rename_session(name: str, new_name: str):
    """
    Renommer une session (dossier + log).
    """
    cm = chat_managers.get(name)
    if not cm:
        raise HTTPException(status_code=404, detail="Session introuvable")

    ok = cm.save_manager.rename_session_file(new_name)
    if not ok:
        raise HTTPException(status_code=400, detail="Impossible de renommer la session")

    # mettre à jour la clé dans le dictionnaire
    chat_managers[new_name] = chat_managers.pop(name)
    return {"old_name": name, "new_name": new_name}

@router.delete("/{name}")
def delete_session(name: str):
    cm = chat_managers.pop(name, None)

    session_dir = Path(SAVE_DIR) / name
    if not session_dir.exists():
        raise HTTPException(status_code=404, detail="Session introuvable")

    try:
        # fermer le logger s'il existe
        log_file = Path(LOGS_DIR) / f"{name}.log"
        for handler in logging.root.handlers[:]:
            if getattr(handler, "baseFilename", None) == str(log_file):
                handler.close()
                logging.root.removeHandler(handler)

        shutil.rmtree(session_dir)
        if log_file.exists():
            log_file.unlink(missing_ok=True)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur suppression: {e}")

    return {"deleted": name}
