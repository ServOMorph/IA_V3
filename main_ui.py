from ui.config_ui import *

from threading import Thread
from kivy.clock import Clock
from kivy.metrics import dp   # <-- AJOUT ICI ✅

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# Backend
from core.chat_manager import ChatManager

# UI widgets
from ui.zones.zone_message import ZoneMessage
from ui.zones.zone_chat import ZoneChat   # <-- nouveau


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
        self.chat_manager = ChatManager()  # backend
        self.zone_chat = None
        self.zone_message = None
        self.thinking_label = None  # <-- label "réfléchit"

    def build(self):
        Window.size = WINDOW_SIZE
        Window.left, Window.top = WINDOW_POSITION
        Window.title = WINDOW_TITLE

        main_layout = BackgroundBox(orientation="horizontal")

        # ---- Colonne gauche ----
        zone_gauche = BoxLayout(orientation="vertical", size_hint=(None, 1), width=ZONE_GAUCHE_WIDTH)

        zone_liste_conv_gauche = ColoredBox(
            title=AREA_NAME_LEFT_TOP,
            bg_color=COLOR_ZONE_LISTE_CONV_GAUCHE,
            orientation="vertical",
            size_hint=(1, None),
            height=ZONE_GAUCHE_HAUT_HEIGHT,
        )
        zone_param_gauche = ColoredBox(
            title=AREA_NAME_LEFT_BOTTOM,
            bg_color=COLOR_ZONE_PARAM_GAUCHE,
            orientation="vertical",
            size_hint=(1, 1),
        )
        zone_gauche.add_widget(zone_liste_conv_gauche)
        zone_gauche.add_widget(zone_param_gauche)

        # ---- Colonne droite ----
        zone_droite = BoxLayout(orientation="vertical", size_hint=(1, 1))

        # >>> zone droite haut = zone_chat
        self.zone_chat = ZoneChat(size_hint=(1, None), height=ZONE_DROITE_HAUT_HEIGHT)

        # >>> zone droite bas
        zone_droite_bas = BoxLayout(orientation="vertical", size_hint=(1, 1))

        # --- container pour "réfléchit" + zone_message ---
        zone_message_wrapper = BoxLayout(orientation="vertical", size_hint=(1, None), height=ZONE_DROITE_BAS_HAUT_HEIGHT)

        # Label "réfléchit" (invisible au départ)
        self.thinking_label = Label(
            text="Je suis en train de réfléchir…",
            color=(0.7, 0.7, 0.7, 1),
            font_size="14sp",
            size_hint=(1, None),
            height=dp(20),
            opacity=0
        )
        zone_message_wrapper.add_widget(self.thinking_label)

        # zone_message
        zone_message_container = ColoredBox(
            bg_color=COLOR_ZONE_MESSAGE,
            orientation="vertical",
            size_hint=(1, 1)
        )

        self.zone_message = ZoneMessage(clear_on_send=True)   # <-- garde la ref
        self.zone_message.bind(on_submit=self._on_zone_message_submit)
        zone_message_container.add_widget(self.zone_message)

        zone_message_wrapper.add_widget(zone_message_container)

        # >>> zone droite bas bas = zone_info
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
        return main_layout

    # ── Handler non bloquant ──
    def _on_zone_message_submit(self, instance, message: str):
        # Masque le bouton envoyer
        if self.zone_message:
            self.zone_message.set_busy(True)

        # Affiche "réfléchit"
        if self.thinking_label:
            self.thinking_label.opacity = 1

        # 1) afficher tout de suite le message utilisateur (à droite)
        self.zone_chat.add_message("Vous", message)

        # 2) lancer l'appel backend en thread
        Thread(target=self._ask_backend, args=(message,), daemon=True).start()

    def _ask_backend(self, message: str):
        try:
            response = self.chat_manager.client.send_prompt(message)
        except Exception as e:
            response = f"[Erreur backend] {e}"

        # 3) poster la réponse IA (à gauche) sur le thread UI
        def _finish(dt):
            self.zone_chat.add_message("IA", response)
            if self.zone_message:
                self.zone_message.set_busy(False)  # <-- réaffiche le bouton
            if self.thinking_label:
                self.thinking_label.opacity = 0   # <-- cache "réfléchit"
        Clock.schedule_once(_finish, 0)


if __name__ == "__main__":
    MyApp().run()
