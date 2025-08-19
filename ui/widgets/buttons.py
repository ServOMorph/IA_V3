# ui/widgets/buttons.py

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window

from ui import config_ui
from ui.behaviors.hover_behavior import HoverBehavior


class ImageButton(ButtonBehavior, Image):
    """Bouton image basique (aucune logique supplémentaire)."""
    pass


class HoverableImageButton(ImageButton, HoverBehavior):
    """
    Bouton image avec hover simplifié.
    Éclaircit automatiquement quand la souris passe dessus.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (1, 1, 1, 1)
        self.bind(hovered=self._on_hover)

    def _on_hover(self, *_):
        self.color = (1.3, 1.3, 1.3, 1) if self.hovered else (1, 1, 1, 1)


class CopyButton(ImageButton):
    """
    Bouton image spécialisé pour copier un texte :
    - Au clic, copie dans le presse-papier.
    - Change d’icône pendant 1s pour confirmer.
    - Gère aussi l’effet hover animé.
    """
    def __init__(self, text_supplier, **kwargs):
        """
        :param text_supplier: fonction (sans argument) qui retourne le texte à copier
        """
        super().__init__(**kwargs)
        self.text_supplier = text_supplier
        self.source = config_ui.ICON_COPY
        self.color = (1, 1, 1, 1)

        self.bind(on_press=self._on_copy_press)
        Window.bind(mouse_pos=self._on_mouse_pos)

    def _on_copy_press(self, *_):
        text = self.text_supplier() or ""
        Clipboard.copy(text)
        self.source = config_ui.ICON_CHECK
        Clock.schedule_once(lambda dt: setattr(self, "source", config_ui.ICON_COPY), 1)

    def _on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        if self.collide_point(*self.to_widget(*pos)):
            Animation(color=config_ui.COLOR_COPY_ICON_HOVER, d=0.15).start(self)
        else:
            Animation(color=(1, 1, 1, 1), d=0.15).start(self)


class SendButton(Button):
    """
    Bouton d'envoi centralisé.
    Rendu pur icône (pas de fond).
    Se désactive si busy ou si aucun texte à envoyer.
    """
    def __init__(self, **kwargs):
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_down", "")
        kwargs.setdefault("background_color", (0, 0, 0, 0))  # fond transparent
        kwargs.setdefault("border", (0, 0, 0, 0))  # pas de bordure
        super().__init__(**kwargs)
        self._zone_message = None

    def bind_to_zone(self, zone_message):
        """Associe ce bouton à une ZoneMessage pour suivre ses états."""
        self._zone_message = zone_message
        zone_message.bind(can_send=lambda *_: self._refresh_state())
        zone_message.bind(busy=lambda *_: self._refresh_state())
        self._refresh_state()

    def _refresh_state(self):
        if not self._zone_message:
            return
        self.disabled = (not self._zone_message.can_send) or self._zone_message.busy
