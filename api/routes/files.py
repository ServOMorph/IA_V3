from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from config import SAVE_DIR
from pathlib import Path

router = APIRouter(prefix="/files", tags=["files"])

@router.get("/{session}/{filename}")
def get_file(session: str, filename: str):
    file_path = Path(SAVE_DIR) / session / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    return FileResponse(file_path)
