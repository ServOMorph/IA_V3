from ui.config_ui import *

from threading import Thread
from pathlib import Path
from kivy.clock import Clock
from kivy.metrics import dp

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# Backend
from core.chat_manager import ChatManager

# UI widgets
from ui.zones.zone_message import ZoneMessage
from ui.zones.zone_chat import ZoneChat
from ui.zones.zone_liste_conv import ZoneListeConv


class BackgroundBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self._bg = Rectangle(source=BACKGROUND_IMAGE, size=self.size, pos=self.pos)
        self.bind(size=self._sync, pos=self._sync)

    def _sync(self, *_):
        self._bg.size, self._bg.pos = self.size, self.pos


class ColoredBox(BoxLayout):
    def __init__(self, title="", bg_color=(1, 1, 1, 0.28), **kwargs):
        super().__init__(**kwargs)
        self._rect = None
        if SHOW_COLORS:
            with self.canvas.before:
                Color(*bg_color)
                self._rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._upd, pos=self._upd)

    def _upd(self, *_):
        if self._rect:
            self._rect.size, self._rect.pos = self.size, self.pos


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chat_manager = ChatManager()
        self.zone_chat = None
        self.zone_message = None
        self.zone_liste_conv = None
        self.thinking_label = None

    def build(self):
        Window.size = WINDOW_SIZE
        Window.left, Window.top = WINDOW_POSITION
        Window.title = WINDOW_TITLE

        main_layout = BackgroundBox(orientation="horizontal")

        # Colonne gauche
        zone_gauche = BoxLayout(orientation="vertical", size_hint=(None, 1), width=ZONE_GAUCHE_WIDTH)

        self.zone_liste_conv = ZoneListeConv(
            sav_dir="./sav",
            size_hint=(1, None),
            height=ZONE_GAUCHE_HAUT_HEIGHT,
        )

        zone_param_gauche = ColoredBox(
            bg_color=COLOR_ZONE_PARAM_GAUCHE,
            orientation="vertical",
            size_hint=(1, 1),
        )

        zone_gauche.add_widget(self.zone_liste_conv)
        zone_gauche.add_widget(zone_param_gauche)

        # Colonne droite
        zone_droite = BoxLayout(orientation="vertical", size_hint=(1, 1))

        self.zone_chat = ZoneChat(size_hint=(1, None), height=ZONE_DROITE_HAUT_HEIGHT)

        zone_droite_bas = BoxLayout(orientation="vertical", size_hint=(1, 1))

        zone_message_wrapper = BoxLayout(orientation="vertical", size_hint=(1, None), height=ZONE_DROITE_BAS_HAUT_HEIGHT)

        self.thinking_label = Label(
            text="Je suis en train de réfléchir…",
            color=(0.7, 0.7, 0.7, 1),
            font_size="14sp",
            size_hint=(1, None),
            height=dp(20),
            opacity=0
        )
        zone_message_wrapper.add_widget(self.thinking_label)

        zone_message_container = ColoredBox(
            bg_color=COLOR_ZONE_MESSAGE,
            orientation="vertical",
            size_hint=(1, 1)
        )

        self.zone_message = ZoneMessage(clear_on_send=True)
        self.zone_message.bind(on_submit=self._on_zone_message_submit)
        zone_message_container.add_widget(self.zone_message)

        zone_message_wrapper.add_widget(zone_message_container)

        zone_info = ColoredBox(
            bg_color=COLOR_ZONE_INFO_DROITE,
            orientation="vertical",
            size_hint=(1, 1),
        )

        zone_droite_bas.add_widget(zone_message_wrapper)
        zone_droite_bas.add_widget(zone_info)

        zone_droite.add_widget(self.zone_chat)
        zone_droite.add_widget(zone_droite_bas)

        main_layout.add_widget(zone_gauche)
        main_layout.add_widget(zone_droite)

        # Sélection conversation -> chargement
        self.zone_liste_conv.set_on_select(self._on_conv_selected)

        return main_layout

    # ====== Flux message UI -> backend -> UI ======

    def _on_zone_message_submit(self, instance, message: str):
        # UI immédiate
        self.zone_chat.add_message("Vous", message)
        if self.zone_message:
            self.zone_message.set_busy(True)
        if self.thinking_label:
            self.thinking_label.opacity = 1

        # Appel modèle en thread
        Thread(target=self._ask_backend, args=(message,), daemon=True).start()

    def _ask_backend(self, message: str):
        try:
            # Envoie message -> IA (ajoute automatiquement user + assistant dans history)
            response = self.chat_manager.client.send_prompt(message)
        except Exception as e:
            response = f"[Erreur backend] {e}"

        # Sauvegarde conversation + éventuels fichiers
        self._backend_save(response)

        # UI
        def _finish(dt):
            self.zone_chat.add_message("IA", response)
            if self.zone_message:
                self.zone_message.set_busy(False)
            if self.thinking_label:
                self.thinking_label.opacity = 0
        Clock.schedule_once(_finish, 0)

    # ====== Helpers backend ======

    def _backend_save(self, last_response=None):
        """Appelle SaveManager comme dans ChatManager.start_chat()."""
        try:
            self.chat_manager.save_manager.save_md(self.chat_manager.client.history)

            if last_response:
                self.chat_manager.save_manager.save_python_from_response(last_response)
                self.chat_manager.save_manager.save_txt_from_response(last_response)
        except Exception as e:
            print(f"[ERREUR SAVE] {e}")

    # ====== Chargement conversation sauvegardée ======

    def _on_conv_selected(self, name, path: Path):
        """Ouvre sav/<name>/conversation.md et l’affiche dans ZoneChat."""
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
                    if line.startswith("**Vous**") or line.startswith("Vous"):
                        msg = line.split(":", 1)[-1].strip()
                        self.zone_chat.add_message("Vous", msg)
                    elif line.startswith("**IA**") or line.startswith("IA"):
                        msg = line.split(":", 1)[-1].strip()
                        self.zone_chat.add_message("IA", msg)
                    else:
                        self.zone_chat.add_message("IA", line)
        except Exception as e:
            self.zone_chat.add_message("Erreur", f"Lecture impossible: {e}")


if __name__ == "__main__":
    MyApp().run()
