# core/chat_manager.py
from core.ollama_client import OllamaClient
from core.sav_manager import SaveManager
from core.commands import CommandHandler
from core.logging.conv_logger import setup_conv_logger
from config import (
    DEFAULT_MODEL,
    SAVE_DIR,
    PRESET_MESSAGES,
    WELCOME_MESSAGE,
    EMPTY_PROMPT_WARNING,
    DEFAULT_SYSTEM_PROMPT,
    LOGS_DIR,
)
from pathlib import Path
import shutil


class ChatManager:
    def __init__(self, model=DEFAULT_MODEL, save_dir=SAVE_DIR):
        # Gestion dossier de session + conversation.md
        self.save_manager = SaveManager(save_dir=save_dir)

        # Client Ollama lié au fichier MD de la session
        self.client = OllamaClient(model=model, session_file=self.save_manager.session_md)

        # Forcer le logger sur le nom du dossier de session
        self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(
            self.save_manager.session_dir.name
        )

        self.commands = CommandHandler(self)

        # Créer conversation.md vide si absent
        if not self.save_manager.session_md.exists():
            self.save_manager.session_md.write_text("", encoding="utf-8")

        # Injecter le prompt système si nouvelle session
        if not self.client.history:
            self.client.history.append(
                {"role": "system", "content": DEFAULT_SYSTEM_PROMPT}
            )

    def start_chat(self):
        print(WELCOME_MESSAGE)

        while True:
            user_prompt = input("\n💬 Vous : ").strip()

            if not user_prompt:
                print(EMPTY_PROMPT_WARNING)
                continue

            # Commandes
            if self.commands.is_command(user_prompt):
                handled, should_exit = self.commands.handle(user_prompt)
                if should_exit:
                    break
                if handled:
                    continue

            # Requête IA
            answer = self.client.send_prompt(user_prompt)
            print(f"🤖 Ollama : {answer}")

            # Sauvegarde conversation en MD
            self.save_manager.save_md(self.client.history)

            # Sauvegarde auto du code s'il y en a
            self.save_manager.save_python_from_response(answer)

            # Sauvegarde auto des documents texte s'il y en a
            self.save_manager.save_txt_from_response(answer)

    def rename_session(self, new_name: str) -> bool:
        """
        Renomme la session courante en fermant le logger actif avant.
        """
        # Fermer le logger actif
        if hasattr(self.client, "conv_logger"):
            for handler in list(self.client.conv_logger.handlers):
                handler.close()
                self.client.conv_logger.removeHandler(handler)

        ok = self.save_manager.rename_session_file(new_name)

        if ok:
            # Réinitialiser le logger avec le nouveau nom
            self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(
                new_name
            )

        return ok

    def delete_session(self, name: str) -> bool:
        """
        Supprime une session et son log.
        Si la session active est supprimée, recrée une session vide.
        """
        try:
            session_dir = Path(SAVE_DIR) / name
            log_file = Path(LOGS_DIR) / f"{name}.log"

            # Fermer logger si c'est la session active
            if self.save_manager.session_name == name and hasattr(self.client, "conv_logger"):
                for handler in list(self.client.conv_logger.handlers):
                    handler.close()
                    self.client.conv_logger.removeHandler(handler)

            # Supprimer le dossier de sauvegarde
            if session_dir.exists():
                shutil.rmtree(session_dir)

            # Supprimer le log
            if log_file.exists():
                log_file.unlink()

            # Si c'était la session active → recréer une nouvelle session
            if self.save_manager.session_name == name:
                self.__init__()  # Réinitialise proprement le ChatManager

            return True
        except Exception as e:
            print(f"[ERREUR DELETE] {e}")
            return False
