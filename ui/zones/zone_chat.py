from ui.zones.zone_base import ZoneBase
from ui.config_ui import (
    ZONE_CHAT_X,
    ZONE_CHAT_Y,
    ZONE_CHAT_WIDTH,
    ZONE_CHAT_HEIGHT,
    ZONE_CHAT_BG_COLOR,
)

class ZoneChat(ZoneBase):
    def __init__(self, surface):
        super().__init__(
            surface,
            ZONE_CHAT_X,
            ZONE_CHAT_Y,
            ZONE_CHAT_WIDTH,
            ZONE_CHAT_HEIGHT,
            ZONE_CHAT_BG_COLOR,
            nom_zone="Zone Chat"
        )
