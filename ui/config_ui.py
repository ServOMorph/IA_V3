# /tests/fenetre_kivy/config_kivy.py

# ----- Configuration fenêtre -----
WINDOW_TITLE = "ServOMorph IA - V3"
WINDOW_SIZE = (960, 1000)         # (largeur, hauteur)
WINDOW_POSITION = (0, 30)         # (x, y) à l'ouverture
BACKGROUND_IMAGE = "assets/images/fond_window.png"

# ----- Toggles d’affichage -----
SHOW_COLORS = False   # Affiche les rectangles semi-transparents
SHOW_LABELS = False   # Affiche les noms des zones

# ----- Dimensions fixes -----
ZONE_GAUCHE_WIDTH = 242
ZONE_GAUCHE_HAUT_HEIGHT = 771
ZONE_DROITE_HAUT_HEIGHT = 771
ZONE_DROITE_BAS_HAUT_HEIGHT = 100

# ----- Couleurs (RGBA) -----
COLOR_ZONE_LISTE_CONV = (0.4, 0.6, 0.9, 0.28)
COLOR_ZONE_PARAM_GAUCHE      = (0.6, 0.9, 0.6, 0.28)
COLOR_ZONE_CHAT_DROITE       = (0.9, 0.7, 0.7, 0.28)  # (ex- liste_conv droite)
COLOR_ZONE_MESSAGE           = (0.9, 0.9, 0.6, 0.28)
COLOR_ZONE_INFO_DROITE       = (0.6, 0.9, 0.9, 0.28)  # (ex- param droite)

# ----- Noms des zones -----
NAME_ZONE_LISTE_CONV = "zone_liste_conv"
NAME_ZONE_PARAM      = "zone_param"
NAME_ZONE_MESSAGE    = "zone_message"
NAME_ZONE_INFO       = "zone_info"
NAME_ZONE_CHAT       = "zone_chat"

# ----- Mapping logique (position -> nom affiché) -----
AREA_NAME_LEFT_TOP            = NAME_ZONE_LISTE_CONV    # zone gauche-haut
AREA_NAME_LEFT_BOTTOM         = NAME_ZONE_PARAM         # zone gauche-bas
AREA_NAME_RIGHT_TOP           = NAME_ZONE_CHAT          # zone droite-haut  ✅
AREA_NAME_RIGHT_BOTTOM_TOP    = NAME_ZONE_MESSAGE       # zone droite bas haut
AREA_NAME_RIGHT_BOTTOM_BOTTOM = NAME_ZONE_INFO          # zone droite bas bas ✅
