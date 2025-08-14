from ui.zones.zone_base import ZoneBase
from ui.config_ui import (
    ZONE_PARAM_X,
    ZONE_PARAM_Y,
    ZONE_PARAM_WIDTH,
    ZONE_PARAM_HEIGHT,
    ZONE_PARAM_BG_COLOR,
)

class ZoneParam(ZoneBase):
    def __init__(self, surface):
        super().__init__(
            surface,
            ZONE_PARAM_X,
            ZONE_PARAM_Y,
            ZONE_PARAM_WIDTH,
            ZONE_PARAM_HEIGHT,
            ZONE_PARAM_BG_COLOR,
            nom_zone="Paramètres"
        )
