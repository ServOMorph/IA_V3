# ui/zones/zone_base.py
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, ListProperty
from ui import config_ui as cfg


def rgb_to_kivy(rgb_tuple):
    """Convertit (R, G, B) 0-255 en (r, g, b, a) 0-1"""
    return [c / 255 for c in rgb_tuple] + [1]


class Zone(FloatLayout):
    """
    Zone générique avec fond coloré et titre en haut à gauche.
    """
    title = StringProperty("Zone")
    bg_color = ListProperty(rgb_to_kivy(cfg.WINDOW_BG_COLOR))
    title_color = ListProperty(rgb_to_kivy(cfg.ZONE_TITRE_TEXT_COLOR))

    def __init__(self, pos=(0, 0), size=(100, 100), **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.pos = pos

        # Dessin du fond
        with self.canvas.before:
            self.color_instruction = Color(*self.bg_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        # Titre
        self.label = Label(
            text=self.title,
            size_hint=(None, None),
            pos=(5, self.height - 25),
            color=self.title_color,
            halign="left",
            valign="top"
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.add_widget(self.label)

        # Bindings
        self.bind(pos=self._update_rect, size=self._update_rect, bg_color=self._update_color)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.label.pos = (5, self.height - 25)

    def _update_color(self, *args):
        self.color_instruction.rgba = self.bg_color
