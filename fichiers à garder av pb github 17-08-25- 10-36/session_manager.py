<<<<<<< HEAD
# core/session_manager.py
from pathlib import Path
import shutil
from config import SAVE_DIR, LOGS_DIR
from core.logging.conv_logger import setup_conv_logger


class SessionManager:
    @staticmethod
    def rename_session(chat_manager, new_name: str) -> bool:
        """
        Renomme la session active via ChatManager.
        Ferme le logger avant, puis réinitialise après.
        """
        try:
            # Fermer logger actif
            if hasattr(chat_manager.client, "conv_logger"):
                for handler in list(chat_manager.client.conv_logger.handlers):
                    handler.close()
                    chat_manager.client.conv_logger.removeHandler(handler)

            ok = chat_manager.save_manager.rename_session_file(new_name)

            if ok:
                chat_manager.client.conv_logger, chat_manager.client.conv_log_file = setup_conv_logger(new_name)

            return ok
        except Exception as e:
            print(f"[ERREUR RENAME] {e}")
            return False

    @staticmethod
    def delete_session(chat_manager, name: str) -> bool:
        """
        Supprime une session et son log.
        Si la session active est supprimée, recrée une session vide.
        """
        try:
            session_dir = Path(SAVE_DIR) / name
            log_file = Path(LOGS_DIR) / f"{name}.log"

            # Fermer logger si c'est la session active
            if chat_manager.save_manager.session_name == name and hasattr(chat_manager.client, "conv_logger"):
                for handler in list(chat_manager.client.conv_logger.handlers):
                    handler.close()
                    chat_manager.client.conv_logger.removeHandler(handler)

            # Supprimer le dossier
            if session_dir.exists():
                shutil.rmtree(session_dir)

            # Supprimer le log
            if log_file.exists():
                log_file.unlink()

            # Si c'était la session active → recréer une session vide
            if chat_manager.save_manager.session_name == name:
                chat_manager.__init__()  # reset complet

            return True
        except Exception as e:
            print(f"[ERREUR DELETE] {e}")
            return False
=======
"""
core/session_manager.py

Responsabilités:
- Gestion centralisée des sessions: renommer, supprimer, charger, créer, déplacer, créer dossier.
- Ferme proprement les handlers de log si la session courante est impactée.
- Manipule les dossiers /sav et /logs pour garantir la cohérence.
- Ne contient AUCUNE logique de chat ou d'interprétation de commandes.
"""
from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Optional, Tuple

from config import SAVE_DIR, LOGS_DIR
from core.sav_manager import SaveManager


# --- Helpers internes --- #

def _sanitize_name(name: str) -> str:
    """Remplace les espaces et nettoie le nom pour éviter problèmes de FS."""
    return name.strip().replace(" ", "_")


def _log_path_for(name: str) -> Path:
    return Path(LOGS_DIR) / f"{name}.log"


def _close_log_handlers_for_logfile(log_file: Path) -> None:
    """
    Ferme tout handler pointant vers `log_file` sur tous les loggers connus.
    Tolère les erreurs.
    """
    try:
        for logger_name, logger in logging.root.manager.loggerDict.items():
            if not isinstance(logger, logging.Logger):
                continue
            to_remove = []
            for h in getattr(logger, "handlers", []):
                base = getattr(getattr(h, "stream", None), "name", None)
                if not base and hasattr(h, "baseFilename"):
                    base = getattr(h, "baseFilename", None)
                if base and Path(base) == log_file:
                    try:
                        h.flush()
                    except Exception:
                        pass
                    try:
                        h.close()
                    except Exception:
                        pass
                    to_remove.append(h)
            for h in to_remove:
                try:
                    logger.removeHandler(h)
                except Exception:
                    pass
    except Exception as e:
        logging.warning("Erreur fermeture handlers log: %s", e)


# --- API publique --- #

def rename_session(current_session: SaveManager, new_name: str) -> bool:
    """Renomme la session COURANTE (celle liée à `current_session`)."""
    new_name = _sanitize_name(new_name)
    old_name = current_session.session_dir.name
    if not new_name or new_name == old_name:
        return False

    old_dir = current_session.session_dir
    new_dir = current_session.save_root / new_name
    if new_dir.exists():
        return False

    _close_log_handlers_for_logfile(_log_path_for(old_name))

    try:
        shutil.move(str(old_dir), str(new_dir))
        old_log = _log_path_for(old_name)
        if old_log.exists():
            shutil.move(str(old_log), str(_log_path_for(new_name)))

        # MAJ internes du SaveManager
        current_session.session_name = new_name
        current_session.session_dir = new_dir
        current_session.session_md = new_dir / "conversation.md"
        return True
    except Exception as e:
        logging.warning("Erreur rename_session: %s", e)
        return False


def rename_other_session(old_name: str, new_name: str) -> bool:
    """Renomme une AUTRE session (non courante)."""
    old_name = _sanitize_name(old_name)
    new_name = _sanitize_name(new_name)
    if not old_name or not new_name or old_name == new_name:
        return False

    old_dir = Path(SAVE_DIR) / old_name
    new_dir = Path(SAVE_DIR) / new_name
    if not old_dir.exists() or new_dir.exists():
        return False

    _close_log_handlers_for_logfile(_log_path_for(old_name))

    try:
        shutil.move(str(old_dir), str(new_dir))
        old_log = _log_path_for(old_name)
        if old_log.exists():
            shutil.move(str(old_log), str(_log_path_for(new_name)))
        return True
    except Exception as e:
        logging.warning("Erreur rename_other_session: %s", e)
        return False


def delete_session(current_session: SaveManager, name: str) -> Tuple[bool, Optional[SaveManager]]:
    """
    Supprime la session `name` dans /sav et /logs.
    Retourne (ok, new_session):
      - ok = True si suppression réussie
      - new_session = SaveManager recréé si c'était la session active, sinon None
    """
    name = _sanitize_name(name)
    session_dir = Path(SAVE_DIR) / name
    log_file = _log_path_for(name)

    is_active = current_session.session_dir.name == name
    if is_active:
        _close_log_handlers_for_logfile(log_file)

    try:
        if session_dir.exists():
            shutil.rmtree(session_dir)
        if log_file.exists():
            log_file.unlink()

        if is_active:
            return True, SaveManager(save_dir=SAVE_DIR)
        return True, None
    except Exception as e:
        logging.warning("Erreur delete_session: %s", e)
        return False, None


def load_session(name: str) -> Optional[SaveManager]:
    """
    Charge une session existante par son nom.
    Retourne un nouveau SaveManager ou None si introuvable.
    """
    name = _sanitize_name(name)
    target_dir = Path(SAVE_DIR) / name
    if not target_dir.exists():
        return None

    try:
        sm = SaveManager(save_dir=SAVE_DIR)
        sm.session_name = name
        sm.session_dir = target_dir
        sm.session_md = target_dir / "conversation.md"
        sm.session_dir.mkdir(parents=True, exist_ok=True)
        return sm
    except Exception as e:
        logging.warning("Erreur load_session: %s", e)
        return None


def new_session() -> SaveManager:
    """Crée une nouvelle session vide."""
    return SaveManager(save_dir=SAVE_DIR)


def create_folder(name: str) -> bool:
    """Crée un dossier d'organisation dans /sav et /logs."""
    name = _sanitize_name(name)
    if not name:
        return False
    try:
        (Path(SAVE_DIR) / name).mkdir(parents=True, exist_ok=True)
        (Path(LOGS_DIR) / name).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logging.warning("Erreur create_folder: %s", e)
        return False


def move_session(conv_name: str, folder: str) -> bool:
    """Déplace une session `conv_name` dans un sous-dossier `folder`."""
    conv_name = _sanitize_name(conv_name)
    folder = _sanitize_name(folder)
    if not conv_name or not folder:
        return False

    src_dir = Path(SAVE_DIR) / conv_name
    dst_dir = Path(SAVE_DIR) / folder / conv_name
    if not src_dir.exists():
        return False

    try:
        dst_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_dir), str(dst_dir))

        src_log = _log_path_for(conv_name)
        if src_log.exists():
            dst_log_dir = Path(LOGS_DIR) / folder
            dst_log_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_log), str(dst_log_dir / f"{conv_name}.log"))
        return True
    except Exception as e:
        logging.warning("Erreur move_session: %s", e)
        return False
>>>>>>> 5116532caa83a3349b98419997f4dcd8736fca1b
