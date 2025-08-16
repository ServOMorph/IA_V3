from __future__ import annotations
from pathlib import Path
from typing import List, Callable

from kivy.properties import StringProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder
import os

# HoverBehavior
from ui.behaviors.hover_behavior import HoverBehavior

KV_PATH = os.path.join(os.path.dirname(__file__), "zone_liste_conv.kv")
Builder.load_file(KV_PATH)


class SelectableItem(ButtonBehavior, HoverBehavior, Label):
    """Élément cliquable de la liste de conversations"""
    selected = BooleanProperty(False)


class ZoneListeConv(BoxLayout):
    """
    Liste scrollable des dossiers de ./sav
    - Triée par date de modification décroissante
    - API publique :
        refresh() -> recharge la liste
        set_on_select(cb: Callable[[str, Path], None]) -> callback sélection
        selected_name -> nom du dossier sélectionné
    """
    sav_dir = StringProperty("./sav")
    items = ListProperty([])
    on_select_cb = ObjectProperty(allownone=True)
    selected_name = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda *_: self.refresh(), 0)

    def refresh(self) -> None:
        """Scan du dossier sav et alimente la RecycleView"""
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
