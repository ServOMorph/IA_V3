from ui.zones.zone_base import Zone, rgb_to_kivy
from ui import config_ui as cfg

class ZoneMessage(Zone):
    def __init__(self, **kwargs):
        super().__init__(
            pos=(cfg.ZONE_MESSAGE_X, cfg.ZONE_MESSAGE_Y),
            size=(cfg.ZONE_MESSAGE_WIDTH, cfg.ZONE_MESSAGE_HEIGHT),
            **kwargs
        )
        self.title = "Message"
        self.bg_color = rgb_to_kivy(cfg.ZONE_MESSAGE_BG_COLOR)
