from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

from ui.config_ui import *
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


def build_layout(app):
    """
    Construit le layout principal et attache les zones dans l'app.
    """
    Window.size = WINDOW_SIZE
    Window.left, Window.top = WINDOW_POSITION
    Window.title = WINDOW_TITLE

    main_layout = BackgroundBox(orientation="horizontal")

    # Colonne gauche
    zone_gauche = BoxLayout(orientation="vertical", size_hint=(None, 1), width=ZONE_GAUCHE_WIDTH)

    app.zone_liste_conv = ZoneListeConv(
        sav_dir="./sav",
        size_hint=(1, None),
        height=ZONE_GAUCHE_HAUT_HEIGHT,
    )

    zone_param_gauche = ColoredBox(
        bg_color=COLOR_ZONE_PARAM_GAUCHE,
        orientation="vertical",
        size_hint=(1, 1),
    )

    zone_gauche.add_widget(app.zone_liste_conv)
    zone_gauche.add_widget(zone_param_gauche)

    # Colonne droite
    zone_droite = BoxLayout(orientation="vertical", size_hint=(1, 1))
    app.zone_chat = ZoneChat(size_hint=(1, None), height=ZONE_DROITE_HAUT_HEIGHT)

    zone_droite_bas = BoxLayout(orientation="vertical", size_hint=(1, 1))

    zone_message_wrapper = BoxLayout(orientation="vertical", size_hint=(1, None), height=ZONE_DROITE_BAS_HAUT_HEIGHT)

    app.thinking_label = Label(
        text="Je suis en train de réfléchir…",
        color=(0.7, 0.7, 0.7, 1),
        font_size="14sp",
        size_hint=(1, None),
        height=dp(20),
        opacity=0
    )
    zone_message_wrapper.add_widget(app.thinking_label)

    zone_message_container = ColoredBox(
        bg_color=COLOR_ZONE_MESSAGE,
        orientation="vertical",
        size_hint=(1, 1)
    )

    app.zone_message = ZoneMessage(clear_on_send=True)
    app.zone_message.bind(on_submit=app._on_zone_message_submit)
    zone_message_container.add_widget(app.zone_message)

    zone_message_wrapper.add_widget(zone_message_container)

    zone_info = ColoredBox(
        bg_color=COLOR_ZONE_INFO_DROITE,
        orientation="vertical",
        size_hint=(1, 1),
    )

    zone_droite_bas.add_widget(zone_message_wrapper)
    zone_droite_bas.add_widget(zone_info)

    zone_droite.add_widget(app.zone_chat)
    zone_droite.add_widget(zone_droite_bas)

    main_layout.add_widget(zone_gauche)
    main_layout.add_widget(zone_droite)

    # Callback sélection conv
    app.zone_liste_conv.set_on_select(app._on_conv_selected)

    return main_layout
