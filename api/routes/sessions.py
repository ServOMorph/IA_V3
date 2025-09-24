from fastapi import APIRouter, HTTPException
from core.chat_manager import ChatManager
from pathlib import Path
from config import SAVE_DIR, LOGS_DIR
import shutil
import logging

print(f"[DEBUG API] SAVE_DIR = {SAVE_DIR}")

router = APIRouter(prefix="/sessions", tags=["sessions"])

# Dictionnaire de ChatManager par session
chat_managers: dict[str, ChatManager] = {}

@router.post("/")
def new_session():
    cm = ChatManager()
    name = cm.save_manager.session_name
    chat_managers[name] = cm

    # Forcer la création du dossier et du fichier
    cm.save_manager.session_dir.mkdir(parents=True, exist_ok=True)
    cm.save_manager.session_md.write_text("", encoding="utf-8")

    print(f"[DEBUG API] Session créée : {name}")
    print(f"[DEBUG API] Dossier attendu : {cm.save_manager.session_dir.resolve()}")
    print(f"[DEBUG API] exists() = {cm.save_manager.session_dir.exists()}")
    print(f"[DEBUG API] conversation.md exists() = {cm.save_manager.session_md.exists()}")

    return {"session": name}

@router.get("/")
def list_sessions():
    sessions = [d.name for d in Path(SAVE_DIR).iterdir() if d.is_dir()]
    return {"sessions": sessions}

@router.get("/{name}/history")
def get_history(name: str):
    cm = chat_managers.get(name)

    if cm:
        # Cas normal (session gérée par l'API)
        return {"history": cm.save_manager.session_md.read_text(encoding="utf-8")}

    # Cas CLI : session pas connue de l'API, mais dossier présent
    file_path = Path(SAVE_DIR) / name / "conversation.md"
    if file_path.exists():
        return {"history": file_path.read_text(encoding="utf-8")}

    raise HTTPException(status_code=404, detail="Session introuvable")

@router.put("/{name}/rename")
def rename_session(name: str, new_name: str):
    print("========== DEBUG API rename ==========")
    print(f"name reçu = {name}, new_name = {new_name}")
    print("Sessions présentes dans chat_managers:", list(chat_managers.keys()))

    cm = chat_managers.get(name)
    print("cm trouvé ?", cm is not None)

    if cm:
        print("cm.save_manager.session_name =", cm.save_manager.session_name)
        print("cm.save_manager.session_dir =", cm.save_manager.session_dir)
        print("cm.save_manager.session_dir.exists() =", cm.save_manager.session_dir.exists())

    print("======================================")

    if not cm:
        raise HTTPException(status_code=404, detail="Session introuvable")

    ok = cm.save_manager.rename_session_file(new_name)
    if not ok:
        raise HTTPException(status_code=400, detail="Impossible de renommer la session")

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
