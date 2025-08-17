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
        self.client = IAClient()
        self.zone_chat = None
        self.zone_message = None
        self.zone_liste_conv = None
        self.thinking_label = None

    def build(self):
        return build_layout(self)

    # ====== Flux message UI -> client -> UI ======

    def _on_zone_message_submit(self, instance, message: str):
        self.zone_chat.add_message("Vous", message)
        if self.zone_message:
            self.zone_message.set_busy(True)
        if self.thinking_label:
            self.thinking_label.opacity = 1
        Thread(target=self._ask_client, args=(message,), daemon=True).start()

    def _ask_client(self, message: str):
        try:
            response = self.client.send_message(message)
        except Exception as e:
            response = f"[Erreur backend] {e}"

        self.client.save_conversation(response)

        def _finish(dt):
            self.zone_chat.add_message("IA", response)
            if self.zone_message:
                self.zone_message.set_busy(False)
            if self.thinking_label:
                self.thinking_label.opacity = 0
        Clock.schedule_once(_finish, 0)

    # ====== Chargement conversation sauvegardée ======

    def _on_conv_selected(self, name, path: Path):
        """Charge une session backend et affiche son contenu dans ZoneChat."""
        # Charger la session côté backend
        ok = self.client.load_session(name)
        if not ok:
            self.zone_chat.add_message("Erreur", f"Impossible de charger la session {name}")
            return

        # Vider l'affichage existant
        self.zone_chat.clear_messages()

        # Lire le fichier de conversation
        conv_md = path / "conversation.md"
        conv_txt = path / "conversation.txt"
        conv_file = conv_md if conv_md.exists() else conv_txt
        if not conv_file.exists():
            self.zone_chat.add_message("System", f"Aucun conversation.md/.txt dans {name}")
            return

        last_sender = None

        try:
            with conv_file.open("r", encoding="utf-8") as f:
                for raw_line in f:
                    line = raw_line.strip()
                    if not line:
                        continue

                    # Détection des rôles
                    if line.startswith("**Vous**"):
                        last_sender = "Vous"
                        continue
                    elif line.startswith("**IA**"):
                        last_sender = "IA"
                        continue

                    # Ignorer métadonnées et prompts système
                    if (
                        line.startswith("#")
                        or line.startswith("_")
                        or line.startswith("--")
                        or line.startswith("**[system]**")
                        or line.startswith("**20")  # timestamp
                        or line.lower().startswith("répond en")
                    ):
                        continue

                    # Contenu → assigné au dernier speaker connu
                    if last_sender:
                        self.zone_chat.add_message(last_sender, line)
                    else:
                        self.zone_chat.add_message("System", line)

        except Exception as e:
            self.zone_chat.add_message("Erreur", f"Lecture impossible: {e}")
