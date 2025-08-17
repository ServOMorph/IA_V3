from core.chat_manager import ChatManager
from core.session_manager import SessionManager
from pathlib import Path
from config import SAVE_DIR, LOGS_DIR
import shutil, logging


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

    def rename_session(self, old_name: str, new_name: str) -> bool:
        if self.backend.save_manager.session_name == old_name:
            return SessionManager.rename_session(self.backend, new_name)

        # Sinon, renommage d'une autre session
        old_dir = Path(SAVE_DIR) / old_name
        new_dir = Path(SAVE_DIR) / new_name
        if not old_dir.exists():
            logging.error(f"Dossier {old_name} introuvable")
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
        return SessionManager.delete_session(self.backend, name)
