from ui.zones.zone_base import Zone, rgb_to_kivy
from ui import config_ui as cfg

class ZoneInfo(Zone):
    def __init__(self, **kwargs):
        super().__init__(
            pos=(cfg.ZONE_INFO_X, cfg.ZONE_INFO_Y),
            size=(cfg.ZONE_INFO_WIDTH, cfg.ZONE_INFO_HEIGHT),
            **kwargs
        )
        self.title = "Info"
        self.bg_color = rgb_to_kivy(cfg.ZONE_INFO_BG_COLOR)
