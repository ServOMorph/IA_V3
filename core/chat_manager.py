# core/chat_manager.py
from core.ollama_client import OllamaClient
from core.sav_manager import SaveManager
from core.commands import CommandHandler
from core.logging.conv_logger import setup_conv_logger
from core.summarizer import Summarizer
from core.auto_titler import AutoTitler
from core.session_manager import SessionManager
from config import (
    DEFAULT_MODEL,
    SAVE_DIR,
    WELCOME_MESSAGE,
    EMPTY_PROMPT_WARNING,
    DEFAULT_SYSTEM_PROMPT,
    MAX_HISTORY_MESSAGES,
)


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

        # Gestion du résumeur avec debug activé
        self.summarizer = Summarizer(self.save_manager.session_dir)

        # Créer conversation.md vide si absent
        if not self.save_manager.session_md.exists():
            self.save_manager.session_md.write_text("", encoding="utf-8")

        # === Correction : réinitialiser complètement l'historique ===
        self.client.history = []
        self.client.history.append(
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT}
        )

        # === DEBUG ===
        print(f"[DEBUG] Nouvelle session créée : {self.save_manager.session_dir.name}")
        # Nouveau : compteur pour détecter les 2 premiers échanges
        self.auto_titler = AutoTitler(self.save_manager.session_dir)

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
            print(f"🤖 VertIA : {answer}")

            # Résumé glissant avec numérotation
            GLIDE_SIZE = 2
            GLOBAL_TRIGGER = 3  # génère un résumé global tous les 3 résumés partiels

            if len(self.client.history) > (GLIDE_SIZE + MAX_HISTORY_MESSAGES):
                old_chunk = self.client.history[:GLIDE_SIZE]
                remaining = self.client.history[GLIDE_SIZE:]

                # Résumé partiel
                summary, idx = self.summarizer.generate_summary(old_chunk)

                # Réinjection : résumé partiel
                self.client.history = (
                    [{"role": "system", "content": f"[Résumé partiel #{idx}] {summary}"}]
                    + remaining
                )

                # Tous les N résumés partiels → générer un résumé global
                if idx % GLOBAL_TRIGGER == 0:
                    global_summary, gidx = self.summarizer.generate_global_summary()
                    self.client.history = (
                        [{"role": "system", "content": f"[Résumé global] {global_summary}"}]
                        + self.client.history[-MAX_HISTORY_MESSAGES:]
                    )

            # Sauvegarde conversation en MD
            self.save_manager.save_md(self.client.history)

            # Sauvegarde auto des blocs selon leur type
            self.save_manager.save_blocks_from_response(answer, "python", "py")
            self.save_manager.save_blocks_from_response(answer, "txt", "txt")
            # Futur : tu peux activer d’autres formats ici
            # self.save_manager.save_blocks_from_response(answer, "csv", "csv")
            # self.save_manager.save_blocks_from_response(answer, "pdf", "pdf")
            
    def resume_session(self, name: str) -> bool:
        """
        Raccourci pour SessionManager.load_session.
        """
        from core.session_manager import SessionManager
        return SessionManager.load_session(self, name)
    
    def process_prompt(self, user_prompt: str) -> str:
        """
        Traite un prompt utilisateur : envoie au modèle, applique le mécanisme
        de résumé, sauvegarde la conversation et retourne la réponse.
        """
        answer = self.client.send_prompt(user_prompt)

        # Résumé glissant avec numérotation
        GLIDE_SIZE = 2
        GLOBAL_TRIGGER = 3
        if len(self.client.history) > (GLIDE_SIZE + MAX_HISTORY_MESSAGES):
            old_chunk = self.client.history[:GLIDE_SIZE]
            remaining = self.client.history[GLIDE_SIZE:]

            summary, idx = self.summarizer.generate_summary(old_chunk)
            self.client.history = (
                [{"role": "system", "content": f"[Résumé partiel #{idx}] {summary}"}]
                + remaining
            )

            if idx % GLOBAL_TRIGGER == 0:
                global_summary, gidx = self.summarizer.generate_global_summary()
                self.client.history = (
                    [{"role": "system", "content": f"[Résumé global] {global_summary}"}]
                    + self.client.history[-MAX_HISTORY_MESSAGES:]
                )

        """
        # === DEBUG ajouté ici ===
        print("====== DEBUG process_prompt ======")
        print("[PROMPT]", user_prompt)
        print("[ANSWER]", answer)
        print("[HISTORY]", self.client.history)
        print("====== END DEBUG ======")
        """

        # Sauvegardes
        self.save_manager.save_md(self.client.history)
        self.save_manager.save_blocks_from_response(answer, "python", "py")
        self.save_manager.save_blocks_from_response(answer, "txt", "txt")
        
        # === Nouveau : renommage automatique après 1 user + 1 assistant ===
        new_title = self.auto_titler.maybe_generate_title(self.client.history)
        if new_title:
            old_name = self.save_manager.session_name

            # Vérifier collisions
            base_title = new_title
            counter = 1
            from pathlib import Path
            from config import SAVE_DIR
            while (Path(SAVE_DIR) / new_title).exists():
                new_title = f"{base_title}_{counter}"
                counter += 1

            if new_title != old_name:
                success = SessionManager.rename_session(self, old_name, new_title)
                if success:
                    print(f"[DEBUG] Session renommée automatiquement → {new_title}")



        return answer

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
                    if not lines:
                        return
                    break
                lines.append(line)

            user_prompt = "\n".join(lines).strip()
            if not user_prompt:
                print(EMPTY_PROMPT_WARNING)
                continue

            if self.commands.is_command(user_prompt):
                handled, should_exit = self.commands.handle(user_prompt)
                if should_exit:
                    break
                if handled:
                    continue

            # Nouveau : centralisation
            answer = self.process_prompt(user_prompt)
            print(f"🤖 VertIA : {answer}")

