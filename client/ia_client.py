from core.chat_manager import ChatManager
from core.session_manager import SessionManager
from core.commands import CommandHandler
from pathlib import Path
from config import SAVE_DIR, LOGS_DIR, PRESET_MESSAGES
import shutil, logging


class IAClient:
    def __init__(self):
        self.backend = ChatManager()
        self.command_handler = CommandHandler(self.backend)

        # pour rester aligné avec le backend
        self.save_manager = self.backend.save_manager
        self.client = self.backend.client

    def send_message(self, message: str) -> str:
        answer = self.client.send_prompt(message)
        # Sauvegarde auto dans la session active
        self.save_conversation(answer)
        return answer

    def save_conversation(self, last_response: str | None = None):
        try:
            self.save_manager.save_md(self.client.history)
            if last_response:
                self.save_manager.save_python_from_response(last_response)
                self.save_manager.save_txt_from_response(last_response)
        except Exception as e:
            print(f"[ERREUR SAVE] {e}")

    def load_session(self, name: str) -> bool:
        """Charge une session via CommandHandler et recrée le client Ollama."""
        ok, _ = self.command_handler.handle(f"&load {name}")
        if not ok:
            return False

        # Recréer OllamaClient lié au nouveau fichier .md
        from core.ollama_client import OllamaClient
        self.backend.client = OllamaClient(
            model=self.backend.client.model,
            session_file=self.backend.save_manager.session_md
        )

        # Reconfigurer le logger
        from core.logging.conv_logger import setup_conv_logger
        self.backend.client.conv_logger, self.backend.client.conv_log_file = setup_conv_logger(
            self.backend.save_manager.session_name
        )

        # Réaligner les références IAClient
        self.save_manager = self.backend.save_manager
        self.client = self.backend.client

        return True

    def rename_session(self, old_name: str, new_name: str) -> bool:
        if self.save_manager.session_name == old_name:
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

    def new_session(self) -> bool:
        """Crée une nouvelle session (nouveau dossier de sauvegarde et client)"""
        try:
            self.backend = ChatManager()
            self.command_handler = CommandHandler(self.backend)

            # Réaligner les références internes
            self.save_manager = self.backend.save_manager
            self.client = self.backend.client

            logging.info(f"[IAClient] Nouvelle session créée : {self.save_manager.session_name}")
            return True
        except Exception as e:
            logging.error(f"[IAClient] Erreur lors de la création de nouvelle session : {e}")
            return False

    # === Commandes spéciales pour l'UI ===
    def run_msg1(self) -> str:
        """Exécute la commande &msg1 côté UI"""
        answer = self.client.send_prompt(PRESET_MESSAGES["msg1"])
        self.save_conversation(answer)
        return answer

    def run_msg2(self) -> str:
        """Exécute la commande &msg2 côté UI"""
        answer = self.client.send_prompt(PRESET_MESSAGES["msg2"])
        self.save_conversation(answer)
        return answer
