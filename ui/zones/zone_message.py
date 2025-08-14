from ui.zones.zone_base import ZoneBase
from ui.config_ui import (
    ZONE_MESSAGE_X,
    ZONE_MESSAGE_Y,
    ZONE_MESSAGE_WIDTH,
    ZONE_MESSAGE_HEIGHT,
    ZONE_MESSAGE_BG_COLOR,
)

class ZoneMessage(ZoneBase):
    def __init__(self, surface):
        super().__init__(
            surface,
            ZONE_MESSAGE_X,
            ZONE_MESSAGE_Y,
            ZONE_MESSAGE_WIDTH,
            ZONE_MESSAGE_HEIGHT,
            ZONE_MESSAGE_BG_COLOR,
            nom_zone="Message"
        )
