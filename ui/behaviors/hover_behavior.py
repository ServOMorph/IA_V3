# ui/behaviors/hover_behavior.py
from kivy.properties import BooleanProperty
from kivy.core.window import Window


class HoverBehavior:
    """
    Mixin à utiliser avec un Widget Kivy pour ajouter un état "hovered".
    - hovered: BoolProperty, True si la souris est au-dessus du widget.

    Exemple d'utilisation :
        class SelectableItem(ButtonBehavior, HoverBehavior, Label):
            selected = BooleanProperty(False)
    """
    hovered = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self._on_mouse_pos)

    def _on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        inside = self.collide_point(*self.to_widget(*pos))
        self.hovered = inside
