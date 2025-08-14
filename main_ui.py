from ui.config_ui import *

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# ⬇️ Import du widget ZoneMessage (UI-only)
from ui.zones.zone_message import ZoneMessage


class BackgroundBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self._bg = Rectangle(source=BACKGROUND_IMAGE, size=self.size, pos=self.pos)
        self.bind(size=self._sync, pos=self._sync)
    def _sync(self, *_):
        self._bg.size, self._bg.pos = self.size, self.pos


class ColoredBox(BoxLayout):
    def __init__(self, title="", bg_color=(1,1,1,0.28), **kwargs):
        super().__init__(**kwargs)
        self._rect = None
        if SHOW_COLORS:
            with self.canvas.before:
                Color(*bg_color)
                self._rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._upd, pos=self._upd)
        if SHOW_LABELS and title:
            self.add_widget(Label(text=title, font_size='18sp'))
    def _upd(self, *_):
        if self._rect:
            self._rect.size, self._rect.pos = self.size, self.pos


class MyApp(App):
    def build(self):
        Window.size = WINDOW_SIZE
        Window.left, Window.top = WINDOW_POSITION
        Window.title = WINDOW_TITLE

        main_layout = BackgroundBox(orientation='horizontal')

        # ---- Colonne gauche ----
        zone_gauche = BoxLayout(orientation='vertical', size_hint=(None, 1), width=ZONE_GAUCHE_WIDTH)

        zone_liste_conv_gauche = ColoredBox(
            title=AREA_NAME_LEFT_TOP,
            bg_color=COLOR_ZONE_LISTE_CONV_GAUCHE,
            orientation='vertical', size_hint=(1, None), height=ZONE_GAUCHE_HAUT_HEIGHT
        )
        zone_param_gauche = ColoredBox(
            title=AREA_NAME_LEFT_BOTTOM,
            bg_color=COLOR_ZONE_PARAM_GAUCHE,
            orientation='vertical', size_hint=(1, 1)
        )
        zone_gauche.add_widget(zone_liste_conv_gauche)
        zone_gauche.add_widget(zone_param_gauche)

        # ---- Colonne droite ----
        zone_droite = BoxLayout(orientation='vertical', size_hint=(1, 1))

        # >>> zone droite haut = zone_chat
        zone_chat = ColoredBox(
            title=AREA_NAME_RIGHT_TOP,
            bg_color=COLOR_ZONE_CHAT_DROITE,
            orientation='vertical', size_hint=(1, None), height=ZONE_DROITE_HAUT_HEIGHT
        )

        # >>> zone droite bas
        zone_droite_bas = BoxLayout(orientation='vertical', size_hint=(1, 1))

        # --- zone_message (haut de la partie basse à droite)
        zone_message_container = ColoredBox(
            title=AREA_NAME_RIGHT_BOTTOM_TOP,
            bg_color=COLOR_ZONE_MESSAGE,
            orientation='vertical', size_hint=(1, None), height=ZONE_DROITE_BAS_HAUT_HEIGHT
        )

        # ⬇️ Insertion du widget ZoneMessage dans le conteneur
        zone_message = ZoneMessage(clear_on_send=True)
        zone_message.bind(on_submit=self._on_zone_message_submit)
        zone_message_container.add_widget(zone_message)

        # >>> zone droite bas bas = zone_info
        zone_info = ColoredBox(
            title=AREA_NAME_RIGHT_BOTTOM_BOTTOM,
            bg_color=COLOR_ZONE_INFO_DROITE,
            orientation='vertical', size_hint=(1, 1)
        )

        zone_droite_bas.add_widget(zone_message_container)
        zone_droite_bas.add_widget(zone_info)

        zone_droite.add_widget(zone_chat)
        zone_droite.add_widget(zone_droite_bas)

        main_layout.add_widget(zone_gauche)
        main_layout.add_widget(zone_droite)
        return main_layout

    # ── Handler provisoire (UI-only, pas de backend) ──
    def _on_zone_message_submit(self, instance, message: str):
        print(f"[ZoneMessage] Message envoyé : {message!r}")
        # Plus tard : branchement vers core/chat_manager.py


if __name__ == "__main__":
    MyApp().run()
