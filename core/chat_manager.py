from core.ollama_client import OllamaClient
from core.sav_manager import SaveManager
from core.commands import CommandHandler
from config import (
    DEFAULT_MODEL,
    SAVE_DIR,
    PRESET_MESSAGES,
    WELCOME_MESSAGE,
    EMPTY_PROMPT_WARNING,
    DEFAULT_SYSTEM_PROMPT,  # 📌 Ajout du prompt système
)

class ChatManager:
    def __init__(self, model=DEFAULT_MODEL, save_dir=SAVE_DIR):
        self.save_manager = SaveManager(save_dir=save_dir)
        self.client = OllamaClient(model=model, session_file=self.save_manager.session_file)
        self.commands = CommandHandler(self)

        # 📌 Création immédiate du fichier de sauvegarde vide s'il n'existe pas encore
        if not self.save_manager.session_file.exists():
            self.save_manager.session_file.write_text("", encoding="utf-8")

        # 📌 Ajout du prompt système si c'est une nouvelle session
        if not self.client.history:  # Pas encore d'historique → première utilisation
            self.client.history.append({"role": "system", "content": DEFAULT_SYSTEM_PROMPT})

    def start_chat(self):
        print(WELCOME_MESSAGE)

        while True:
            user_prompt = input("\n💬 Vous : ").strip()

            # Empêcher les prompts vides tôt
            if not user_prompt:
                print(EMPTY_PROMPT_WARNING)
                continue

            # Délégation des commandes
            if self.commands.is_command(user_prompt):
                handled, should_exit = self.commands.handle(user_prompt)
                if should_exit:
                    break
                if handled:
                    continue  # ne pas envoyer à l'IA si la commande a été traitée

            # Requête classique → envoi à l'IA
            answer = self.client.send_prompt(user_prompt)
            print(f"🤖 Ollama : {answer}")

            # Sauvegarde automatique après chaque réponse
            self.save_manager.save_txt(self.client.history)
