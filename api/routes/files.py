# api/routes/files.py
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
import tempfile

from config import SAVE_DIR
from core.file_manager import copy_file_to_session, add_file_as_system_context
from api.routes import sessions  # accès à chat_managers

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/{session}/{filename}")
def get_file(session: str, filename: str):
    file_path = Path(SAVE_DIR) / session / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    return FileResponse(file_path)


@router.post("/{session}/upload")
async def upload_file(session: str, file: UploadFile = File(...)):
    """
    Upload d’un fichier vers une session :
      - copie dans SAVE_DIR/<session>/
      - ajoute le contenu au contexte système de la session (comme &copyfile)
    """
    try:
        # Vérifier que la session existe côté API
        chat_manager = sessions.chat_managers.get(session)
        if not chat_manager:
            raise HTTPException(status_code=404, detail=f"Session {session} introuvable")

        # Écrire le fichier uploadé en temporaire
        tmp_path = Path(tempfile.gettempdir()) / file.filename
        with tmp_path.open("wb") as buffer:
            buffer.write(await file.read())

        # Copier dans le dossier de la session
        dst = copy_file_to_session(session, tmp_path)

        # Ajouter le contenu au contexte système de ce ChatManager
        add_file_as_system_context(chat_manager.client, dst)

        return {"filename": dst.name, "session": session}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
