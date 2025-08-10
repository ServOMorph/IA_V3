from core.ollama_client import OllamaClient
from core.sav_manager import SaveManager
from core.commands import show_commands
from core.logging.conv_logger import setup_conv_logger  # pour recréer le logger après /rename
from config import DEFAULT_MODEL, SAVE_DIR, PRESET_MESSAGES, WELCOME_MESSAGE, EXIT_SAVE_MESSAGE, EXIT_NO_SAVE_MESSAGE, EMPTY_PROMPT_WARNING


class ChatManager:
    def __init__(self, model=DEFAULT_MODEL, save_dir=SAVE_DIR):
        self.save_manager = SaveManager(save_dir=save_dir)
        self.client = OllamaClient(model=model, session_file=self.save_manager.session_file)

    def start_chat(self):
        print(WELCOME_MESSAGE)

        while True:
            user_prompt = input("\n💬 Vous : ").strip()

            # Sauvegarder et quitter
            if user_prompt.lower() == "/q":
                print(EXIT_SAVE_MESSAGE)
                break

            # Quitter sans sauvegarde
            if user_prompt.lower() in {"/exit", "exit", "quit"}:
                print(EXIT_NO_SAVE_MESSAGE)
                break

            # Afficher l'aide
            if user_prompt.lower() == "/help":
                show_commands()
                continue

            # Renommer la conversation
            if user_prompt.lower().startswith("/rename"):
                parts = user_prompt.split(" ", 1)
                if len(parts) == 2 and parts[1].strip():
                    new_name = parts[1].strip()
                    success = self.save_manager.rename_session_file(new_name)
                    if success:
                        # Recréation du conv_logger avec le nouveau nom
                        session_name = self.save_manager.session_file.stem
                        self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(session_name)
                        print(f"✅ Conversation renommée en : {new_name}.txt")
                    else:
                        print("⚠️ Impossible de renommer la conversation (nom déjà utilisé ou erreur).")
                else:
                    print("⚠️ Usage : /rename NOM")
                continue

            # Message pré-enregistré 1
            if user_prompt.lower() == "/msg1":
                answer = self.client.send_prompt(PRESET_MESSAGES["msg1"])
                print(f"🤖 Ollama : {answer}")
                self.save_manager.save_txt(self.client.history)
                continue

            # Message pré-enregistré 2
            if user_prompt.lower() == "/msg2":
                answer = self.client.send_prompt(PRESET_MESSAGES["msg2"])
                print(f"🤖 Ollama : {answer}")
                self.save_manager.save_txt(self.client.history)
                continue

            # Charger une conversation
            if user_prompt.lower().startswith("/load"):
                parts = user_prompt.split(" ", 1)
                if len(parts) == 2 and parts[1].strip():
                    name = parts[1].strip()
                    loaded_content = self.save_manager.load_session_file(name)
                    if loaded_content is not None:
                        from pathlib import Path
                        new_file = self.save_manager.save_dir / f"{name}.txt"
                        self.save_manager.session_file = new_file
                        self.client.session_file = new_file

                        # Recréation du conv_logger avec le nom chargé
                        self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(name)

                        print("\n📂 Conversation chargée :\n")
                        print(loaded_content)
                    else:
                        print(f"⚠️ Impossible de charger '{name}.txt'.")
                else:
                    print("⚠️ Usage : /load NOM")
                continue

            # Empêcher les prompts vides
            if not user_prompt:
                print(EMPTY_PROMPT_WARNING)
                continue

            # Envoyer la question à l'IA avec le contexte du fichier de sauvegarde
            answer = self.client.send_prompt(user_prompt)
            print(f"🤖 Ollama : {answer}")

            # Sauvegarde automatique après chaque réponse
            self.save_manager.save_txt(self.client.history)
