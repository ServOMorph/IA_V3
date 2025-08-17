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
