from ui.zones.zone_base import Zone, rgb_to_kivy
from ui import config_ui as cfg

class ZoneParam(Zone):
    def __init__(self, **kwargs):
        super().__init__(
            pos=(cfg.ZONE_PARAM_X, cfg.ZONE_PARAM_Y),
            size=(cfg.ZONE_PARAM_WIDTH, cfg.ZONE_PARAM_HEIGHT),
            **kwargs
        )
        self.title = "Paramètres"
        self.bg_color = rgb_to_kivy(cfg.ZONE_PARAM_BG_COLOR)
