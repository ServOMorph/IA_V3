from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import os

KV_PATH = os.path.join(os.path.dirname(__file__), "zone_message.kv")
Builder.load_file(KV_PATH)

class SubmitTextInput(TextInput):
    """Champ d'entrée avec envoi sur Entrée."""
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        _, key = keycode
        if key in ('enter', 'kpenter'):
            parent = self.parent
            while parent and not isinstance(parent, ZoneMessage):
                parent = getattr(parent, 'parent', None)
            if isinstance(parent, ZoneMessage):
                parent.submit()
                return True
        return super().keyboard_on_key_down(window, keycode, text, modifiers)

class ZoneMessage(BoxLayout):
    placeholder = StringProperty("Poser une question")
    text = StringProperty("")
    clear_on_send = BooleanProperty(True)
    can_send = BooleanProperty(False)

    __events__ = ('on_submit', )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda *_: self._refresh_state(), 0)

    def submit(self):
        msg = (self.text or "").strip()
        if not msg:
            return
        self.dispatch('on_submit', msg)
        if self.clear_on_send:
            self.text = ""
            if 'input' in self.ids:
                self.ids.input.text = ""
        self._refresh_state()

    def on_submit(self, message: str):
        pass

    def _on_text(self, value: str):
        if self.text != value:
            self.text = value
        self._refresh_state()

    def on_text(self, *_):
        self._refresh_state()

    def _refresh_state(self):
        self.can_send = bool((self.text or "").strip())
