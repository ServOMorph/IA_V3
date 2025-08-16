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
        self.zone_chat.clear_messages()
        conv_md = path / "conversation.md"
        conv_txt = path / "conversation.txt"
        conv_file = conv_md if conv_md.exists() else conv_txt
        if not conv_file.exists():
            self.zone_chat.add_message("System", f"Aucun conversation.md/.txt dans {name}")
            return
        try:
            with conv_file.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("**Vous**") or line.startswith("Vous:"):
                        msg = line.split(":", 1)[-1].strip()
                        self.zone_chat.add_message("Vous", msg)
                    elif line.startswith("**IA**") or line.startswith("IA:"):
                        msg = line.split(":", 1)[-1].strip()
                        self.zone_chat.add_message("IA", msg)
                    else:
                        self.zone_chat.add_message("System", line)
        except Exception as e:
            self.zone_chat.add_message("Erreur", f"Lecture impossible: {e}")
