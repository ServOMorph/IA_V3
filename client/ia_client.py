from core.chat_manager import ChatManager


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

    # ===== Nouveau : renommage d'une session =====
    def rename_session(self, old_name: str, new_name: str) -> bool:
        """
        Renomme une session existante. Retourne True si succès.
        - old_name : nom du dossier actuel
        - new_name : nouveau nom demandé
        """
        try:
            # Si c'est la session en cours → utiliser le save_manager courant
            if self.backend.save_manager.session_name == old_name:
                return self.backend.save_manager.rename_session_file(new_name)

            # Sinon, renommer un autre dossier directement
            from pathlib import Path
            from config import SAVE_DIR, LOGS_DIR
            import shutil, logging

            save_root = Path(SAVE_DIR)
            old_dir = save_root / old_name
            new_dir = save_root / new_name

            if not old_dir.exists():
                logging.error(f"Dossier {old_name} introuvable")
                return False
            if new_dir.exists():
                logging.error(f"Dossier {new_name} existe déjà")
                return False

            shutil.move(str(old_dir), str(new_dir))

            old_log = Path(LOGS_DIR) / f"{old_name}.log"
            if old_log.exists():
                new_log = Path(LOGS_DIR) / f"{new_name}.log"
                shutil.move(str(old_log), str(new_log))

            return True
        except Exception as e:
            print(f"[ERREUR RENAME] {e}")
            return False
