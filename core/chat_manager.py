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
            print("\n💬 Vous (une ligne = Entrée, plusieurs lignes = Entrée deux fois) :")
            lines = []
            while True:
                try:
                    line = input()
                except EOFError:
                    return
                if line == "":
                    # Cas 1 : rien du tout → re-demander
                    if not lines:
                        return
                    # Cas 2 : fin d’un bloc multi-lignes
                    break
                lines.append(line)

            # Si une seule ligne → l’envoyer directement
            if len(lines) == 1:
                user_prompt = lines[0].strip()
            else:
                user_prompt = "\n".join(lines).strip()


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

