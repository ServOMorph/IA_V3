# === Correction rond rouge clic droit ===
from kivy.config import Config
Config.set("input", "mouse", "mouse,multitouch_on_demand")

from threading import Thread
from pathlib import Path
from kivy.clock import Clock
from kivy.app import App

from client.ia_client import IAClient
from ui.layout_builder import build_layout


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "ServOMorph IA" 
        self.client = IAClient()
        self.zone_chat = None
        self.zone_message = None
        self.zone_liste_conv = None
        self.thinking_label = None

    def build(self):
        root = build_layout(self)

        # Sélectionner la conversation courante dès l'ouverture
        if self.zone_liste_conv and self.client and self.client.save_manager:
            current_name = self.client.save_manager.session_dir.name
            if current_name:
                self.zone_liste_conv.select(current_name)

        return root

    # ====== Flux message UI -> client -> UI ======
    def _on_zone_message_submit(self, instance, message: str):
        if self.zone_message:
            self.zone_message.set_busy(True)
        if self.thinking_label:
            self.thinking_label.opacity = 1

        def run_background():
            # Affichage du message utilisateur dans le thread principal
            def add_user(dt):
                if message == "__MSG1__":
                    self.zone_chat.add_message("Vous", "[CMD] msg1")
                elif message == "__MSG2__":
                    self.zone_chat.add_message("Vous", "[CMD] msg2")
                elif message == "__RUN__":
                    self.zone_chat.add_message("Vous", "[CMD] run")
                else:
                    self.zone_chat.add_message("Vous", message)
            Clock.schedule_once(add_user, 0)

            # Calcul de la réponse en thread secondaire
            if message == "__MSG1__":
                response = self.client.run_msg1()
            elif message == "__MSG2__":
                response = self.client.run_msg2()
            elif message == "__RUN__":
                response = self.client.run_last_script()
            else:
                response = self.client.send_message(message)

            self.client.save_conversation(response if isinstance(response, str) else None)

            # Affichage de la réponse IA dans le thread principal
            def _finish(dt):
                if response and isinstance(response, str):
                    self.zone_chat.add_message("IA", response)
                if self.zone_message:
                    self.zone_message.set_busy(False)
                if self.thinking_label:
                    self.thinking_label.opacity = 0
            Clock.schedule_once(_finish, 0)

        Thread(target=run_background, daemon=True).start()

    # ====== Chargement conversation sauvegardée ======
    def _on_conv_selected(self, name, path: Path):
        """Charge une session backend et affiche son contenu dans ZoneChat."""
        ok = self.client.load_session(name)
        if not ok:
            self.zone_chat.add_message("Erreur", f"Impossible de charger la session {name}")
            return

        self.zone_chat.clear_messages()

        conv_md = path / "conversation.md"
        conv_txt = path / "conversation.txt"
        conv_file = conv_md if conv_md.exists() else conv_txt
        if not conv_file.exists():
            self.zone_chat.add_message("System", f"Aucun conversation.md/.txt dans {name}")
            return

        last_sender = None

        try:
            skip_system_block = False
            with conv_file.open("r", encoding="utf-8") as f:
                for raw_line in f:
                    line = raw_line.strip()
                    if not line:
                        continue

                    if line.startswith("**[system]**"):
                        skip_system_block = True
                        continue

                    if skip_system_block:
                        if line.startswith("###") or line.startswith("---"):
                            skip_system_block = False
                        continue

                    if line.startswith("**Vous**"):
                        last_sender = "Vous"
                        continue
                    elif line.startswith("**IA**"):
                        last_sender = "IA"
                        continue

                    if (
                        line.startswith("#")
                        or line.startswith("_")
                        or line.startswith("--")
                        or line.startswith("**20")
                        or line.lower().startswith("répond en")
                    ):
                        continue

                    if last_sender:
                        self.zone_chat.add_message(last_sender, line)
                    else:
                        self.zone_chat.add_message("System", line)

        except Exception as e:
            self.zone_chat.add_message("Erreur", f"Lecture impossible: {e}")
