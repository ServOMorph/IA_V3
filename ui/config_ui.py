# config_ui.py
# Toutes les constantes et données configurables pour l'UI

import os

# Détermine le chemin absolu de la racine du projet
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Fenêtre
WINDOW_TITLE = "ServOMorph IA - V3"
WINDOW_SIZE = (960, 1000)  # largeur, hauteur
WINDOW_POSITION = (0, 30)  # position X, position Y à l'ouverture

# Image de fond (chemin absolu)
BACKGROUND_IMAGE = os.path.join(BASE_DIR, "assets", "images", "fond_window.png")

# Couleurs (RGBA)
BG_COLOR = (0.15, 0.15, 0.15, 1)
TEXT_COLOR = (1, 1, 1, 1)

