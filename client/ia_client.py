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
        """
        Charge une session en évitant d'écraser son contenu
        et recharge l'historique pour l'UI.
        """
        target_dir = Path(SAVE_DIR) / name
        md_path = target_dir / "conversation.md"
        if not md_path.exists():
            logging.error(f"[IAClient] Conversation introuvable : {md_path}")
            return False

        # Basculer vers la session cible sans sauver l’ancienne
        self.save_manager.session_dir = target_dir
        self.save_manager.session_md = md_path
        self.save_manager.session_name = target_dir.name

        from core.ollama_client import OllamaClient
        self.backend.client = OllamaClient(
            model=self.backend.client.model,
            session_file=md_path
        )

        from core.logging.conv_logger import setup_conv_logger
        self.backend.client.conv_logger, self.backend.client.conv_log_file = setup_conv_logger(
            self.save_manager.session_name
        )

        # Synchroniser aussi côté backend
        self.backend.save_manager.session_dir = target_dir
        self.backend.save_manager.session_md = md_path
        self.backend.save_manager.session_name = target_dir.name

        # Réaligner les références
        self.save_manager = self.backend.save_manager
        self.client = self.backend.client

        # === Recharger l'historique depuis conversation.md ===
        try:
            if md_path.exists():
                lines = md_path.read_text(encoding="utf-8").splitlines()
                history = []
                current_role, buffer = None, []
                for line in lines:
                    if line.startswith("**[system]**"):
                        if current_role and buffer:
                            history.append({"role": current_role, "content": "\n".join(buffer).strip()})
                        current_role, buffer = "system", []
                        continue
                    if line.startswith("**Vous**"):
                        if current_role and buffer:
                            history.append({"role": current_role, "content": "\n".join(buffer).strip()})
                        current_role, buffer = "user", []
                        continue
                    if line.startswith("**IA**"):
                        if current_role and buffer:
                            history.append({"role": current_role, "content": "\n".join(buffer).strip()})
                        current_role, buffer = "assistant", []
                        continue
                    # Ligne de contenu
                    if current_role:
                        buffer.append(line)

                if current_role and buffer:
                    history.append({"role": current_role, "content": "\n".join(buffer).strip()})

                self.backend.client.history = history
                logging.info(f"[IAClient] Historique rechargé : {len(history)} échanges.")
        except Exception as e:
            logging.error(f"[IAClient] Erreur de rechargement historique: {e}")

        logging.info(f"[IAClient] Session chargée : {name}")
        return True

    def rename_session(self, old_name: str, new_name: str) -> bool:
        if self.save_manager.session_name == old_name:
            return SessionManager.rename_session(self.backend, new_name)

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
        try:
            self.backend = ChatManager()
            self.command_handler = CommandHandler(self.backend)
            self.save_manager = self.backend.save_manager
            self.client = self.backend.client
            logging.info(f"[IAClient] Nouvelle session créée : {self.save_manager.session_name}")
            return True
        except Exception as e:
            logging.error(f"[IAClient] Erreur lors de la création de nouvelle session : {e}")
            return False

    # === Commandes spéciales pour l'UI ===
    def run_msg1(self) -> str:
        answer = self.client.send_prompt(PRESET_MESSAGES["msg1"])
        self.save_conversation(answer)
        return answer

    def run_msg2(self) -> str:
        answer = self.client.send_prompt(PRESET_MESSAGES["msg2"])
        self.save_conversation(answer)
        return answer

    def run_last_script(self) -> str:
        """
        Exécute la commande &run côté UI.
        Retourne un message lisible avec gestion des erreurs.
        """
        try:
            handled, _ = self.command_handler.handle("&run")
            if handled:
                return "▶️ Commande &run envoyée au backend (un terminal devrait s’ouvrir)."
            return "⚠️ Aucun script trouvé à exécuter."
        except Exception as e:
            return f"❌ Erreur lors du lancement du script : {e}"
