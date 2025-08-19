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
COLOR_ZONE_CHAT_DROITE       = (0.9, 0.7, 0.7, 0.28)
COLOR_ZONE_MESSAGE           = (0.9, 0.9, 0.6, 0.28)
COLOR_ZONE_INFO_DROITE       = (0.6, 0.9, 0.9, 0.28)

# ----- Noms des zones -----
NAME_ZONE_LISTE_CONV = "zone_liste_conv"
NAME_ZONE_PARAM      = "zone_param"
NAME_ZONE_MESSAGE    = "zone_message"
NAME_ZONE_INFO       = "zone_info"
NAME_ZONE_CHAT       = "zone_chat"

# ----- Mapping logique (position -> nom affiché) -----
AREA_NAME_LEFT_TOP            = NAME_ZONE_LISTE_CONV
AREA_NAME_LEFT_BOTTOM         = NAME_ZONE_PARAM
AREA_NAME_RIGHT_TOP           = NAME_ZONE_CHAT
AREA_NAME_RIGHT_BOTTOM_TOP    = NAME_ZONE_MESSAGE
AREA_NAME_RIGHT_BOTTOM_BOTTOM = NAME_ZONE_INFO

# ----- Couleurs zone_chat -----
COLOR_USER_BUBBLE   = (0.20, 0.60, 1.00, 1)  # bulle utilisateur
COLOR_USER_TEXT     = (1, 1, 1, 1)
COLOR_IA_BUBBLE     = (0.20, 0.20, 0.20, 1)  # bulle IA
COLOR_IA_TEXT       = (1, 1, 1, 1)

# Curseur
COLOR_CURSOR        = COLOR_USER_BUBBLE

# ----- Couleurs zone_liste_conv -----
COLOR_USER_BUBBLE_LIGHT = (0.40, 0.75, 1.00, 1)

# ----- Styles zone_liste_conv -----
FONT_SIZE_CONV_LIST = "13sp"

# ----- Icônes -----
ICON_COPY = "assets/images/copier_icon.png"
COLOR_COPY_ICON_HOVER = (1, 1, 1, 0.6)  # couleur au survol
ICON_CHECK = "assets/images/coche_icon.png"
