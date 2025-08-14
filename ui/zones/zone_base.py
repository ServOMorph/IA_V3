import pygame

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
        """Dessine uniquement le fond de la zone."""
        pygame.draw.rect(self.surface, self.bg_color, self.rect)

         # Titre
        texte_surface = self.font.render(self.nom_zone, True, (0, 0, 0))  # Noir
        self.surface.blit(
            texte_surface,
            (self.rect.x + 2, self.rect.y + 2)  # un petit décalage du bord
        )