import pygame
from ui.zones.zone_base import ZoneBase
from ui.config_ui import (
    INPUT_RECT_X,
    INPUT_RECT_Y,
    INPUT_RECT_WIDTH,
    INPUT_RECT_HEIGHT,
    INPUT_RECT_BG_COLOR,
    INPUT_RECT_BORDER_COLOR,
    INPUT_RECT_BORDER_WIDTH,
    ZONE_MESSAGE_TEXT_COLOR,
    ZONE_MESSAGE_FONT_SIZE,
)

class ZoneMessage(ZoneBase):
    def __init__(self, surface):
        super().__init__(surface, INPUT_RECT_X, INPUT_RECT_Y, INPUT_RECT_WIDTH, INPUT_RECT_HEIGHT)
        self.input_text = ""
        self.font_message = pygame.font.Font(None, ZONE_MESSAGE_FONT_SIZE)

        self.placeholder = "Poser une question"
        self.has_focus = False

        # Définition du rectangle de saisie
        self.input_rect = pygame.Rect(INPUT_RECT_X, INPUT_RECT_Y, INPUT_RECT_WIDTH, INPUT_RECT_HEIGHT)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Focus si clic dans le rectangle
            if self.input_rect.collidepoint(event.pos):
                self.has_focus = True
            else:
                self.has_focus = False

        if self.has_focus and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # SHIFT + Entrée = saut de ligne
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    self.input_text += "\n"
                else:
                    print(f"Message envoyé :\n{self.input_text}")
                    self.input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode

    def afficher(self):
        # Forme pilule
        border_radius = self.input_rect.height // 2
        pygame.draw.rect(self.surface, INPUT_RECT_BG_COLOR, self.input_rect, border_radius=border_radius)
        pygame.draw.rect(self.surface, INPUT_RECT_BORDER_COLOR, self.input_rect, INPUT_RECT_BORDER_WIDTH, border_radius=border_radius)

        # Texte à afficher
        if self.input_text.strip() == "":
            text_color = ZONE_MESSAGE_TEXT_COLOR
            text = self.placeholder
        else:
            text_color = ZONE_MESSAGE_TEXT_COLOR
            text = self.input_text

        # Découper le texte en lignes
        lines = text.split("\n")
        y_offset = self.input_rect.y + 10
        for line in lines:
            text_surface = self.font_message.render(line, True, text_color)
            self.surface.blit(text_surface, (self.input_rect.x + 15, y_offset))
            y_offset += text_surface.get_height() + 4
