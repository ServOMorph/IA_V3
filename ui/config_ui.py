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

# Couleur de fond par défaut
WINDOW_BG_COLOR = (30, 30, 30)

# --- Couleur du texte pour les titres de zones ---
ZONE_TITRE_TEXT_COLOR = (255, 255, 255)  # Blanc

# --- Zone Chat ---
ZONE_CHAT_X = 241
ZONE_CHAT_Y = 0
ZONE_CHAT_WIDTH = 722
ZONE_CHAT_HEIGHT = 773
ZONE_CHAT_BG_COLOR = (255, 192, 203)   # Rose clair

# --- Zone Liste Conversations ---
ZONE_LISTE_X = 0
ZONE_LISTE_Y = 0
ZONE_LISTE_WIDTH = 236
ZONE_LISTE_HEIGHT = 773
ZONE_LISTE_BG_COLOR = (200, 200, 200)  # Gris clair

# --- Zone Paramètres ---
ZONE_PARAM_X = 0
ZONE_PARAM_Y = 778
ZONE_PARAM_WIDTH = 236
ZONE_PARAM_HEIGHT = 222
ZONE_PARAM_BG_COLOR = (180, 180, 180)

# --- Zone Message ---
ZONE_MESSAGE_X = 241
ZONE_MESSAGE_Y = 778
ZONE_MESSAGE_WIDTH = 718
ZONE_MESSAGE_HEIGHT = 100
ZONE_MESSAGE_BG_COLOR = (235, 235, 235)
ZONE_MESSAGE_TEXT_COLOR = (236, 236, 236)
ZONE_MESSAGE_FONT_SIZE = 24

# --- Rectangle de saisie interne ---
INPUT_RECT_X = 251   # position X
INPUT_RECT_Y = 813   # position Y
INPUT_RECT_WIDTH = 600
INPUT_RECT_HEIGHT = 50
INPUT_RECT_BG_COLOR = (25, 25, 25)  
INPUT_RECT_BORDER_COLOR = (51, 51, 51)   
INPUT_RECT_BORDER_WIDTH = 2

# --- Zone Info ---
ZONE_INFO_X = 241
ZONE_INFO_Y = 880
ZONE_INFO_WIDTH = 718
ZONE_INFO_HEIGHT = 95
ZONE_INFO_BG_COLOR = (210, 210, 210)
