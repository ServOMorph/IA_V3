import pygame
from ui.config_ui import ZONE_TITRE_TEXT_COLOR

class ZoneBase:
    def __init__(self, surface, x, y, width, height, bg_color, nom_zone="Zone"):
        """
        Classe de base pour toutes les zones UI.
        """
        self.surface = surface
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.nom_zone = nom_zone
        # Police par défaut
        self.font = pygame.font.Font(None, 24)  # 24 px

    def afficher(self):
            """Dessine uniquement le titre de la zone (pas de fond)."""
            texte_surface = self.font.render(self.nom_zone, True, ZONE_TITRE_TEXT_COLOR)
            self.surface.blit(
                texte_surface,
                (self.rect.x + 2, self.rect.y + 2)  # petit décalage
            )