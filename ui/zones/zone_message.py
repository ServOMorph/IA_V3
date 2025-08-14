# ui/zones/zone_message.py
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.clock import Clock

KV = '''
<ZoneMessage>:
    # Mise en page: texte à gauche, bouton à droite
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(120)
    padding: dp(10)
    spacing: dp(8)

    SubmitTextInput:
        id: input
        text: root.text
        hint_text: root.placeholder
        multiline: True
        cursor_blink: True
        write_tab: False
        size_hint_x: 1
        on_text: root._on_text(self.text)

    Button:
        text: 'Envoyer'
        size_hint_x: None
        width: dp(110)
        disabled: not root.can_send
        on_release: root.submit()
'''
# Charger la règle KV une seule fois (évite les doublons/règles redéfinies)
Builder.load_string(KV)


class SubmitTextInput(TextInput):
    """Entrée: envoyer | Shift+Entrée: nouvelle ligne."""
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        _, key = keycode
        if key in ('enter', 'kpenter'):
            # Shift/Alt/Ctrl + Entrée => nouvelle ligne
            if any(m in modifiers for m in ('shift', 'alt', 'ctrl')):
                return super().keyboard_on_key_down(window, keycode, text, modifiers)
            # Entrée seul => submit
            parent = self.parent
            while parent is not None and not isinstance(parent, ZoneMessage):
                parent = getattr(parent, 'parent', None)
            if isinstance(parent, ZoneMessage):
                parent.submit()
                return True
        return super().keyboard_on_key_down(window, keycode, text, modifiers)


class ZoneMessage(BoxLayout):
    """Zone de message (UI only) — émet on_submit(message)."""
    placeholder = StringProperty("Écrivez votre question ici… (Entrée pour envoyer, Shift+Entrée pour nouvelle ligne)")
    text = StringProperty("")
    clear_on_send = BooleanProperty(True)
    can_send = BooleanProperty(False)

    __events__ = ('on_submit', )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda *_: self._refresh_state(), 0)

    # --- API ---
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

    # Événement à binder depuis l'UI appelante
    def on_submit(self, message: str):
        pass

    # --- Interne ---
    def _on_text(self, value: str):
        if self.text != value:
            self.text = value
        self._refresh_state()

    def on_text(self, *_):
        self._refresh_state()

    def _refresh_state(self):
        self.can_send = bool((self.text or "").strip())
