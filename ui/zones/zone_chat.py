from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation

from ui import config_ui

MAX_BUBBLE_W = dp(420)
RADIUS = dp(12)
PADX, PADY = dp(10), dp(6)


class ImageButton(ButtonBehavior, Image):
    """Bouton basé sur une image (utilisé pour l’icône copier)."""
    pass


class ChatBubble(BoxLayout):
    def __init__(self, text, bubble_rgba, text_rgba, sender="IA", **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.orientation = "horizontal"
        self.spacing = dp(6)
        self.text_content = text  # stocker le texte pour copier

        if sender == "IA":
            self.add_widget(Image(
                source="assets/images/Logo_IA.png",
                size_hint=(None, None),
                size=(dp(32), dp(32)),
                allow_stretch=True,
                keep_ratio=True
            ))

        # conteneur vertical : texte + bouton copier
        vbox = BoxLayout(orientation="vertical", spacing=dp(2), size_hint=(None, None))
        self.add_widget(vbox)

        # bulle texte
        self.bubble_box = BoxLayout(size_hint=(None, None), padding=[PADX, PADY])
        vbox.add_widget(self.bubble_box)

        self.lbl = Label(
            text=text,
            color=text_rgba,
            halign="left",
            valign="top",
            size_hint=(None, None),
            text_size=(None, None),
        )
        self.lbl.bind(texture_size=lambda *_: Clock.schedule_once(self._sync_sizes, 0))
        self.bubble_box.add_widget(self.lbl)

        with self.bubble_box.canvas.before:
            Color(*bubble_rgba)
            self.bg = RoundedRectangle(radius=[RADIUS])
        self.bubble_box.bind(pos=self._update_bg, size=self._update_bg)

        # bouton copier
        self.copy_btn = ImageButton(
            source=config_ui.ICON_COPY,
            size_hint=(None, None),
            size=(dp(18), dp(18)),
            color=(1, 1, 1, 1),
        )
        vbox.add_widget(self.copy_btn)

        # action clic copier -> coche temporaire
        def _on_copy_press(*_):
            Clipboard.copy(self.text_content)
            self.copy_btn.source = config_ui.ICON_CHECK
            Clock.schedule_once(lambda dt: setattr(self.copy_btn, "source", config_ui.ICON_COPY), 1)

        self.copy_btn.bind(on_press=_on_copy_press)

        # bind souris pour hover
        Window.bind(mouse_pos=self._on_mouse_pos)

        Clock.schedule_once(self._sync_sizes, 0)

    def _on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        if self.copy_btn.collide_point(*self.copy_btn.to_widget(*pos)):
            Animation(color=config_ui.COLOR_COPY_ICON_HOVER, d=0.15).start(self.copy_btn)
        else:
            Animation(color=(1, 1, 1, 1), d=0.15).start(self.copy_btn)

    def _sync_sizes(self, *_):
        w_txt = min(self.lbl.texture_size[0], MAX_BUBBLE_W)
        self.lbl.text_size = (w_txt, None)
        self.lbl.texture_update()

        h_txt = self.lbl.texture_size[1]
        self.lbl.size = (w_txt, h_txt)
        self.bubble_box.size = (w_txt + 2 * PADX, h_txt + 2 * PADY)

        # ajustement conteneur vertical
        parent_vbox = self.children[0] if self.children else self.bubble_box
        if hasattr(parent_vbox, "children") and len(parent_vbox.children) > 1:
            total_h = self.bubble_box.height + dp(20)
            parent_vbox.size = (self.bubble_box.width, total_h)

        self.size = (
            self.bubble_box.width + (dp(38) if len(self.children) > 1 else 0),
            self.bubble_box.height + dp(20),
        )

    def _update_bg(self, *args):
        self.bg.pos = self.bubble_box.pos
        self.bg.size = self.bubble_box.size


class ZoneChat(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_scroll_x = False
        self.do_scroll_y = True

        self._anchor = AnchorLayout(anchor_y="bottom", size_hint_y=None)
        self.add_widget(self._anchor)

        self.messages_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8),
            padding=[dp(10), dp(10)],
        )
        self.messages_box.bind(minimum_height=self.messages_box.setter("height"))
        self._anchor.add_widget(self.messages_box)

        self.bind(size=self._sync_anchor_height)
        self.messages_box.bind(height=lambda *_: self._sync_anchor_height())

    def _sync_anchor_height(self, *args):
        self._anchor.height = max(self.height, self.messages_box.height)

    def add_message(self, sender: str, text: str):
        if sender == "Vous":
            bubble_rgba = config_ui.COLOR_USER_BUBBLE
            text_rgba = config_ui.COLOR_USER_TEXT
            line = AnchorLayout(anchor_x="right", size_hint_y=None)
        else:
            bubble_rgba = config_ui.COLOR_IA_BUBBLE
            text_rgba = config_ui.COLOR_IA_TEXT
            line = AnchorLayout(anchor_x="left", size_hint_y=None)

        bubble = ChatBubble(text, bubble_rgba, text_rgba, sender=sender)
        line.add_widget(bubble)

        def _finalize(*_):
            line.height = bubble.height
            self._sync_anchor_height()
            Clock.schedule_once(lambda __: setattr(self, "scroll_y", 0), 0)

        self.messages_box.add_widget(line)
        Clock.schedule_once(_finalize, 0)

    def clear_messages(self):
        self.messages_box.clear_widgets()
        self._sync_anchor_height()
