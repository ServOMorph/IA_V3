"""
config_ui.py
Constantes spécifiques à l'interface Kivy de ServOMorph IA (Windows uniquement).
"""

from pathlib import Path
import ctypes
from ctypes import wintypes

# === Nom et titre de l'application ===
APP_NAME = "ServOMorph IA"
WINDOW_TITLE = "ServOMorph IA"

# === Chemin vers le log commun avec le backend ===
ROOT_DIR = Path(__file__).parent
DEBUG_LOG_PATH = ROOT_DIR / "debug.log"

# === Récupération de la zone de travail Windows (hors barre des tâches) ===
user32 = ctypes.windll.user32
SPI_GETWORKAREA = 48
rect = wintypes.RECT()
ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0)

WORK_WIDTH = rect.right - rect.left
WORK_HEIGHT = rect.bottom - rect.top
WORK_LEFT = rect.left
WORK_TOP = rect.top

# === Décalage pour voir la barre de titre ===
TITLEBAR_OFFSET = 30  # hauteur en pixels à ajouter
BOTTOM_MARGIN = 5     # pour éviter de toucher la barre des tâches

# === Dimensions et position de la fenêtre ===
WINDOW_WIDTH = WORK_WIDTH // 2
WINDOW_HEIGHT = WORK_HEIGHT - TITLEBAR_OFFSET - BOTTOM_MARGIN
WINDOW_LEFT = WORK_LEFT
WINDOW_TOP = WORK_TOP + TITLEBAR_OFFSET

# === Styles ===
FONT_SIZE_TITLE = 24
FONT_SIZE_TEXT = 16
BACKGROUND_COLOR = (0.1, 0.1, 0.1, 1)  # gris très foncé
TEXT_COLOR = (1, 1, 1, 1)  # blanc

# === Marges ===
PADDING = 10