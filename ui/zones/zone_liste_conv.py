from __future__ import annotations
from pathlib import Path
from typing import List, Callable

from kivy.properties import StringProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout as KVBox
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.app import App
import os

from ui.widgets.buttons import PlusButton
from ui.behaviors.hover_behavior import HoverBehavior

KV_PATH = os.path.join(os.path.dirname(__file__), "zone_liste_conv.kv")
Builder.load_file(KV_PATH)


class SelectableItem(ButtonBehavior, HoverBehavior, Label):
    """Élément cliquable de la liste de conversations"""
    selected = BooleanProperty(False)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == "right":
                self.show_context_menu()
                return True
        return super().on_touch_down(touch)

    def get_zone_liste_conv(self):
        parent = self.parent
        from ui.zones.zone_liste_conv import ZoneListeConv
        while parent and not isinstance(parent, ZoneListeConv):
            parent = getattr(parent, "parent", None)
        return parent

    def show_context_menu(self):
        content = KVBox(orientation="vertical", spacing=5, padding=10)
        btn_rename = Button(text="Renommer", size_hint_y=None, height=40)
        btn_delete = Button(text="Supprimer", size_hint_y=None, height=40)

        popup = Popup(
            title=f"Actions : {self.text}",
            content=content,
            size_hint=(None, None),
            size=(300, 200),
            auto_dismiss=True,
        )

        zone = self.get_zone_liste_conv()
        if zone:
            btn_rename.bind(on_release=lambda *_: zone.rename_item(self.text, popup))
            btn_delete.bind(on_release=lambda *_: zone.delete_item(self.text, popup))

        content.add_widget(btn_rename)
        content.add_widget(btn_delete)
        popup.open()


class ZoneListeConv(BoxLayout):
    sav_dir = StringProperty("./sav")
    items = ListProperty([])
    on_select_cb = ObjectProperty(allownone=True)
    selected_name = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        Clock.schedule_once(lambda *_: self.refresh(), 0)
        Clock.schedule_once(lambda *_: self._bind_plus_button(), 0)

    def _bind_plus_button(self):
        btn = self.ids.get("btn_plus")
        if btn:
            btn.bind(on_release=lambda *_: self.create_new_conv())

    def create_new_conv(self):
        app = App.get_running_app()
        if app.client.new_session():
            new_name = app.client.save_manager.session_name
            print(f"[ZoneListeConv] Nouvelle conversation créée : {new_name}")
            self.refresh()
            self.select(new_name)
            if "zone_chat" in app.root.ids:
                app.root.ids["zone_chat"].clear_messages()
                
    def refresh(self) -> None:
        base = Path(self.sav_dir)
        if not base.exists():
            base.mkdir(parents=True, exist_ok=True)

        dirs: List[Path] = [p for p in base.iterdir() if p.is_dir()]
        dirs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        self.items = [d.name for d in dirs]

        rv = self.ids.get("rv")
        if rv:
            rv.data = [
                {
                    "text": name,
                    "selected": (name == self.selected_name),
                    "on_release": (lambda n=name: self.select(n)),
                }
                for name in self.items
            ]

    def set_on_select(self, cb: Callable[[str, Path], None]) -> None:
        self.on_select_cb = cb

    def select(self, name: str) -> None:
        self.selected_name = name
        self._update_selection_visuals()
        if callable(self.on_select_cb):
            self.on_select_cb(name, Path(self.sav_dir) / name)

    def _update_selection_visuals(self) -> None:
        rv = self.ids.get("rv")
        if not rv:
            return
        current = self.selected_name
        rv.data = [
            {
                "text": name,
                "selected": (name == current),
                "on_release": (lambda n=name: self.select(n)),
            }
            for name in self.items
        ]
