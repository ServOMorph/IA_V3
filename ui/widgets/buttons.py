from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window

from ui import config_ui


class IconButton(ButtonBehavior, Image):
    """
    Bouton icône unifié :
    - éclairci au survol
    - affiche une coche pendant 0.8s après clic
    """

    def __init__(self, icon_source, **kwargs):
        super().__init__(**kwargs)
        self.default_source = icon_source
        self.source = icon_source
        self.allow_stretch = True
        self.keep_ratio = True
        self.color = (1, 1, 1, 1)

        self.bind(on_press=self._on_click)
        Window.bind(mouse_pos=self._on_mouse_pos)

    def _on_click(self, *_):
        self.source = config_ui.ICON_CHECK
        Clock.schedule_once(lambda dt: setattr(self, "source", self.default_source), 0.8)

    def _on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        if self.collide_point(*self.to_widget(*pos)):
            Animation(color=(1.3, 1.3, 1.3, 1), d=0.15).start(self)
        else:
            Animation(color=(1, 1, 1, 1), d=0.15).start(self)


class CopyButton(IconButton):
    """Bouton copier (icône copier → coche après clic)."""
    def __init__(self, text_supplier, **kwargs):
        self._text_supplier = text_supplier
        super().__init__(config_ui.ICON_COPY, **kwargs)

    def _on_click(self, *_):
        from kivy.core.clipboard import Clipboard
        Clipboard.copy(self._text_supplier() or "")
        super()._on_click()


class PlusButton(IconButton):
    """Bouton + pour nouvelle conversation."""
    def __init__(self, **kwargs):
        super().__init__("assets/images/plus_icon.png", **kwargs)


class SendButton(IconButton):
    """Bouton envoyer."""
    def __init__(self, **kwargs):
        super().__init__("assets/images/send_icon.png", **kwargs)
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
