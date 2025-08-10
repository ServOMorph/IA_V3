from config import (
    PRESET_MESSAGES,
    EXIT_SAVE_MESSAGE,
    EXIT_NO_SAVE_MESSAGE,
)
from core.logging.conv_logger import setup_conv_logger
from pathlib import Path

COMMANDS = {
    "/q": "Sauvegarder la conversation et quitter",
    "/exit": "Quitter sans sauvegarder",
    "/help": "Afficher la liste des commandes",
    "/rename": "Renommer la conversation actuelle (/rename NOM)",
    "/msg1": "Demander à l'IA : Quelle est la capitale de la France ?",
    "/msg2": "Demander à l'IA : Raconte moi une histoire en 20 caractères sur la ville dont tu viens de parler",
    "/load": "Charger une conversation depuis le dossier /sav (/load NOM)",
    "/suppr": "Supprimer une conversation et son log (/suppr NOM)",
    "/copie_ia": "Copier la dernière réponse de l'IA dans le presse-papier",
    "/copie_user": "Copier le dernier message utilisateur dans le presse-papier"


}


def show_commands():
    """Affiche toutes les commandes disponibles."""
    print("\n📜 Commandes disponibles :")
    for cmd, desc in COMMANDS.items():
        print(f"{cmd:<10} → {desc}")
    print()


class CommandHandler:
    """
    Gère l'exécution des commandes côté chat.
    On lui passe l'instance de ChatManager pour accéder à save_manager, client, etc.
    """

    def __init__(self, chat_manager):
        self.chat_manager = chat_manager
        self.save_manager = chat_manager.save_manager
        self.client = chat_manager.client

    @staticmethod
    def is_command(text: str) -> bool:
        return text.startswith("/")

    def handle(self, user_input: str) -> tuple[bool, bool]:
        """
        Exécute la commande et renvoie (handled, should_exit).
        - handled: True si c'était une commande reconnue (même si erreurs d'arguments)
        - should_exit: True si la commande implique de quitter la boucle (ex: /q, /exit)
        """
        raw = user_input.strip()
        lower = raw.lower()
        parts = raw.split(" ", 1)
        cmd = parts[0]
        arg = parts[1].strip() if len(parts) == 2 else None

        # --------------------
        # Commandes de sortie
        # --------------------
        if lower == "/q":
            try:
                self.save_manager.save_txt(self.client.history)
            except Exception:
                pass
            print(EXIT_SAVE_MESSAGE)
            return True, True

        if lower in {"/exit", "exit", "quit"}:
            print(EXIT_NO_SAVE_MESSAGE)
            return True, True

        # -------------
        # Aide / liste
        # -------------
        if lower == "/help":
            show_commands()
            return True, False

        # ----------------
        # Renommer session
        # ----------------
        if lower.startswith("/rename"):
            if not arg:
                print("⚠️ Usage : /rename NOM")
                return True, False

            new_name = arg
            success = self.save_manager.rename_session_file(new_name)
            if success:
                session_name = self.save_manager.session_file.stem
                self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(session_name)
                print(f"✅ Conversation renommée en : {new_name}.txt")
            else:
                print("⚠️ Impossible de renommer la conversation (nom déjà utilisé ou erreur).")
            return True, False

        # -------------------
        # Messages préfaits
        # -------------------
        if lower == "/msg1":
            answer = self.client.send_prompt(PRESET_MESSAGES["msg1"])
            print(f"🤖 Ollama : {answer}")
            self.save_manager.save_txt(self.client.history)
            return True, False

        if lower == "/msg2":
            answer = self.client.send_prompt(PRESET_MESSAGES["msg2"])
            print(f"🤖 Ollama : {answer}")
            self.save_manager.save_txt(self.client.history)
            return True, False

        # -----------------------
        # Charger une sauvegarde
        # -----------------------
        if lower.startswith("/load"):
            if not arg:
                print("⚠️ Usage : /load NOM")
                return True, False

            name = arg
            loaded_content = self.save_manager.load_session_file(name)
            if loaded_content is not None:
                new_file = self.save_manager.save_dir / f"{name}.txt"
                self.save_manager.session_file = new_file
                self.client.session_file = new_file
                self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(name)
                print("\n📂 Conversation chargée :\n")
                print(loaded_content)
            else:
                print(f"⚠️ Impossible de charger '{name}.txt'.")
            return True, False

        # ----------------------
        # Supprimer une session
        # ----------------------
        if lower.startswith("/suppr"):
            if not arg:
                print("⚠️ Usage : /suppr NOM")
                return True, False

            name = arg
            sav_file = self.save_manager.save_dir / f"{name}.txt"
            log_file = Path("logs") / f"{name}.log"

            deleted = False

            # Fermer le logger si c'est le log courant
            if self.client.conv_log_file and Path(self.client.conv_log_file).resolve() == log_file.resolve():
                for handler in list(self.client.conv_logger.handlers):
                    handler.close()
                    self.client.conv_logger.removeHandler(handler)

            # Supprimer la sauvegarde
            if sav_file.exists():
                try:
                    sav_file.unlink()
                    deleted = True
                except Exception as e:
                    print(f"⚠️ Impossible de supprimer {sav_file.name} : {e}")

            # Supprimer le log
            if log_file.exists():
                try:
                    log_file.unlink()
                    deleted = True
                except Exception as e:
                    print(f"⚠️ Impossible de supprimer {log_file.name} : {e}")

            if deleted:
                print(f"🗑️ Conversation '{name}' supprimée (sauvegarde et log).")
            else:
                print(f"⚠️ Aucun fichier trouvé pour '{name}'.")
            return True, False
        
        # ----------------------
        # Nouvelle conversation
        # ----------------------
        if lower == "/new":
            try:
                self.save_manager.save_txt(self.client.history)
            except Exception:
                pass

            if self.client.conv_logger:
                for handler in list(self.client.conv_logger.handlers):
                    handler.close()
                    self.client.conv_logger.removeHandler(handler)

            # Nouvelle instance de SaveManager et OllamaClient
            self.chat_manager.save_manager = self.save_manager.__class__(save_dir=self.save_manager.save_dir)
            self.chat_manager.client = self.client.__class__(
                model=self.client.model,
                session_file=self.chat_manager.save_manager.session_file
            )

            # Création immédiate du fichier .txt vide
            self.chat_manager.save_manager.session_file.write_text("", encoding="utf-8")

            print(f"🆕 Nouvelle conversation démarrée : {self.chat_manager.save_manager.session_file.name}")
            return True, False
        
        # ----------------------
        # Copier la dernière réponse IA
        # ----------------------
        if lower == "/copie_ia":
            import pyperclip

            if not self.client.history:
                print("⚠️ Aucune réponse IA à copier.")
                return True, False

            last_ai_response = self.client.history[-1].get("response", "").strip()
            if not last_ai_response:
                print("⚠️ La dernière réponse de l'IA est vide.")
                return True, False

            pyperclip.copy(last_ai_response)
            print("📋 Dernière réponse de l'IA copiée dans le presse-papier.")
            return True, False


        # ----------------------
        # Copier le dernier message utilisateur
        # ----------------------
        if lower == "/copie_user":
            import pyperclip

            if not self.client.history:
                print("⚠️ Aucun message utilisateur à copier.")
                return True, False

            last_user_message = self.client.history[-1].get("prompt", "").strip()
            if not last_user_message:
                print("⚠️ Le dernier message utilisateur est vide.")
                return True, False

            pyperclip.copy(last_user_message)
            print("📋 Dernier message utilisateur copié dans le presse-papier.")
            return True, False


