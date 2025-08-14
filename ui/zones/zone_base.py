import pygame
from ui.config_ui import ZONE_TITRE_TEXT_COLOR

class ZoneBase:
    def __init__(self, surface, x, y, width, height):
        """
        Classe de base pour toutes les zones UI.
        """
        self.surface = surface
        self.rect = pygame.Rect(x, y, width, height)

    def afficher(self):
            """Ne dessine rien par défaut."""
            pass