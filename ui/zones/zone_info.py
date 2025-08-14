from ui.zones.zone_base import ZoneBase
from ui.config_ui import (
    ZONE_INFO_X,
    ZONE_INFO_Y,
    ZONE_INFO_WIDTH,
    ZONE_INFO_HEIGHT,
    ZONE_INFO_BG_COLOR,
)

class ZoneInfo(ZoneBase):
    def __init__(self, surface):
        super().__init__(
            surface,
            ZONE_INFO_X,
            ZONE_INFO_Y,
            ZONE_INFO_WIDTH,
            ZONE_INFO_HEIGHT,
            ZONE_INFO_BG_COLOR,
            nom_zone="Info"
        )
