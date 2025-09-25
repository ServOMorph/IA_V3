# core/file_manager.py
from pathlib import Path
import shutil
from config import SAVE_DIR

def copy_file_to_session(session: str, src_path: Path) -> Path:
    """
    Copie un fichier dans le dossier de session et retourne son chemin cible.
    """
    session_dir = Path(SAVE_DIR) / session
    if not session_dir.exists():
        raise FileNotFoundError(f"Session {session} introuvable")

    dst = session_dir / src_path.name
    shutil.copy(src_path, dst)
    return dst


def add_file_as_system_context(client, dst: Path):
    """
    Ajoute le contenu du fichier comme message système au client.
    Si un message system existe déjà, ajoute le contenu à la suite.
    """
    try:
        text = dst.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        raise RuntimeError(f"Erreur lecture {dst}: {e}")

    if not text.strip():
        # Fichier vide → rien à faire
        return

    # Vérifier si un message système existe déjà
    system_msg = next((m for m in client.history if m.get("role") == "system"), None)
    if system_msg:
        system_msg["content"] += f"\n\n[Contexte importé depuis {dst.name}]\n{text}"
    else:
        client.history.append({
            "role": "system",
            "content": f"Ecris en Français\n\n[Contexte importé depuis {dst.name}]\n{text}"
        })
