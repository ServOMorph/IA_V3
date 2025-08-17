from core.chat_manager import ChatManager
<<<<<<< HEAD
from core.session_manager import SessionManager
from pathlib import Path
from config import SAVE_DIR, LOGS_DIR
import shutil, logging
=======
from Refacto.core import session_manager
>>>>>>> 5116532caa83a3349b98419997f4dcd8736fca1b


class IAClient:
    def __init__(self):
        self.backend = ChatManager()

    def send_message(self, message: str) -> str:
        return self.backend.client.send_prompt(message)

    def save_conversation(self, last_response: str | None = None):
        try:
            self.backend.save_manager.save_md(self.backend.client.history)
            if last_response:
                self.backend.save_manager.save_python_from_response(last_response)
                self.backend.save_manager.save_txt_from_response(last_response)
        except Exception as e:
            print(f"[ERREUR SAVE] {e}")

<<<<<<< HEAD
    def rename_session(self, old_name: str, new_name: str) -> bool:
        if self.backend.save_manager.session_name == old_name:
            return SessionManager.rename_session(self.backend, new_name)

        # Sinon, renommage d'une autre session
        old_dir = Path(SAVE_DIR) / old_name
        new_dir = Path(SAVE_DIR) / new_name
        if not old_dir.exists():
            logging.error(f"Dossier {old_name} introuvable")
=======
    # ===== Outil interne =====
    def _close_logger(self):
        """Ferme tous les handlers du conv_logger actif (utile sous Windows)."""
        if getattr(self.backend.client, "conv_logger", None):
            for h in list(self.backend.client.conv_logger.handlers):
                try:
                    h.flush()
                    h.close()
                except Exception:
                    pass
                self.backend.client.conv_logger.removeHandler(h)

    # ===== Renommage d'une session =====
    def rename_session(self, old_name: str, new_name: str) -> bool:
        """
        Renomme une session.
        - Si old_name est la session active → session_manager.rename_session
        - Sinon → session_manager.rename_other_session
        """
        try:
            if self.backend.save_manager.session_name == old_name:
                # Fermer le logger avant le move
                self._close_logger()
                ok = session_manager.rename_session(self.backend.save_manager, new_name)
                if ok:
                    from core.logging.conv_logger import setup_conv_logger
                    self.backend.client.conv_logger, self.backend.client.conv_log_file = setup_conv_logger(new_name)
                return ok
            else:
                # Fermer aussi pour éviter tout lock
                self._close_logger()
                return session_manager.rename_other_session(old_name, new_name)
        except Exception as e:
            print(f"[ERREUR RENAME] {e}")
>>>>>>> 5116532caa83a3349b98419997f4dcd8736fca1b
            return False
        if new_dir.exists():
            logging.error(f"Dossier {new_name} existe déjà")
            return False
        shutil.move(str(old_dir), str(new_dir))
        old_log = Path(LOGS_DIR) / f"{old_name}.log"
        if old_log.exists():
            shutil.move(str(old_log), str(Path(LOGS_DIR) / f"{new_name}.log"))
        return True

    def delete_session(self, name: str) -> bool:
<<<<<<< HEAD
        return SessionManager.delete_session(self.backend, name)
=======
        """Supprime une session via session_manager et rebind si active."""
        try:
            # Fermer le logger avant suppression
            self._close_logger()
            ok, new_session = session_manager.delete_session(self.backend.save_manager, name)
            if ok and new_session:
                self.backend.save_manager = new_session
                from core.logging.conv_logger import setup_conv_logger
                self.backend.client.conv_logger, self.backend.client.conv_log_file = setup_conv_logger(
                    new_session.session_dir.name
                )
            return ok
        except Exception as e:
            print(f"[ERREUR DELETE] {e}")
            return False
>>>>>>> 5116532caa83a3349b98419997f4dcd8736fca1b
