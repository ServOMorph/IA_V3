from ui.zones.zone_base import ZoneBase
from ui.config_ui import (
    ZONE_LISTE_X,
    ZONE_LISTE_Y,
    ZONE_LISTE_WIDTH,
    ZONE_LISTE_HEIGHT,
    ZONE_LISTE_BG_COLOR,
)

class ZoneListeConv(ZoneBase):
    def __init__(self, surface):
        super().__init__(
            surface,
            ZONE_LISTE_X,
            ZONE_LISTE_Y,
            ZONE_LISTE_WIDTH,
            ZONE_LISTE_HEIGHT,
            ZONE_LISTE_BG_COLOR,
            nom_zone="Conversations sauvegardées"
        )
