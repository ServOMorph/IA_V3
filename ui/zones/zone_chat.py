from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.clock import Clock

MAX_BUBBLE_W = dp(420)
RADIUS = dp(12)
PADX, PADY = dp(10), dp(6)


class ChatBubble(BoxLayout):
    def __init__(self, text, bubble_rgba, text_rgba, sender="IA", **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.orientation = "horizontal"
        self.spacing = dp(6)

        if sender == "IA":
            self.add_widget(Image(
                source="assets/images/Logo_IA.png",
                size_hint=(None, None),
                size=(dp(32), dp(32)),
                allow_stretch=True,
                keep_ratio=True
            ))

        self.bubble_box = BoxLayout(size_hint=(None, None), padding=[PADX, PADY])
        self.add_widget(self.bubble_box)

        self.lbl = Label(
            text=text,
            color=text_rgba,
            halign="left",
            valign="middle",
            size_hint=(None, None),
            text_size=(MAX_BUBBLE_W, None),
        )
        self.lbl.bind(texture_size=lambda *_: Clock.schedule_once(self._sync_sizes, 0))
        self.bubble_box.add_widget(self.lbl)

        with self.bubble_box.canvas.before:
            Color(*bubble_rgba)
            self.bg = RoundedRectangle(radius=[RADIUS])
        self.bubble_box.bind(pos=self._update_bg, size=self._update_bg)

        Clock.schedule_once(self._sync_sizes, 0)

    def _sync_sizes(self, *_):
        w_txt = min(self.lbl.texture_size[0], MAX_BUBBLE_W)
        h_txt = self.lbl.texture_size[1]
        self.lbl.size = (w_txt, h_txt)
        self.bubble_box.size = (w_txt + 2 * PADX, h_txt + 2 * PADY)
        self.size = (self.bubble_box.width + (dp(38) if len(self.children) > 1 else 0),
                     self.bubble_box.height)

    def _update_bg(self, *args):
        self.bg.pos = self.bubble_box.pos
        self.bg.size = self.bubble_box.size


class ZoneChat(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_scroll_x = False
        self.do_scroll_y = True

        # Conteneur ancré en bas
        self._anchor = AnchorLayout(anchor_y="bottom", size_hint_y=None)
        self.add_widget(self._anchor)

        # Colonne des messages
        self.messages_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8),
            padding=[dp(10), dp(10)],
        )
        self.messages_box.bind(minimum_height=self.messages_box.setter("height"))
        self._anchor.add_widget(self.messages_box)

        # Maintient l'ancre à au moins la hauteur visible du ScrollView
        self.bind(size=self._sync_anchor_height)
        self.messages_box.bind(height=lambda *_: self._sync_anchor_height())

    def _sync_anchor_height(self, *args):
        # ancre = max(vue, contenu) -> contenu collé en bas si petit
        self._anchor.height = max(self.height, self.messages_box.height)

    def add_message(self, sender: str, text: str):
        if sender == "Vous":
            bubble_rgba = (0.20, 0.60, 1.00, 1)
            text_rgba = (1, 1, 1, 1)
            line = AnchorLayout(anchor_x="right", size_hint_y=None)
        else:
            bubble_rgba = (0.20, 0.20, 0.20, 1)
            text_rgba = (1, 1, 1, 1)
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
        """Efface toutes les bulles du chat."""
        self.messages_box.clear_widgets()
        self._sync_anchor_height()
