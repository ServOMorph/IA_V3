from ui.zones.zone_base import Zone, rgb_to_kivy
from ui import config_ui as cfg

class ZoneChat(Zone):
    def __init__(self, **kwargs):
        super().__init__(
            pos=(cfg.ZONE_CHAT_X, cfg.ZONE_CHAT_Y),
            size=(cfg.ZONE_CHAT_WIDTH, cfg.ZONE_CHAT_HEIGHT),
            **kwargs
        )
        self.title = "Chat"
        self.bg_color = rgb_to_kivy(cfg.ZONE_CHAT_BG_COLOR)
