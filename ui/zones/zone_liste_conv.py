from ui.zones.zone_base import Zone, rgb_to_kivy
from ui import config_ui as cfg

class ZoneListeConv(Zone):
    def __init__(self, **kwargs):
        super().__init__(
            pos=(cfg.ZONE_LISTE_X, cfg.ZONE_LISTE_Y),
            size=(cfg.ZONE_LISTE_WIDTH, cfg.ZONE_LISTE_HEIGHT),
            **kwargs
        )
        self.title = "Conversations"
        self.bg_color = rgb_to_kivy(cfg.ZONE_LISTE_BG_COLOR)
