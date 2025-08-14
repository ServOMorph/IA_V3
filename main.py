import pygame
import pygame_gui
from ui.zones.zone_message import ZoneMessage

def main():
    pygame.init()
    window = pygame.display.set_mode((1024, 900))
    pygame.display.set_caption("Zone Message avec pygame_gui")

    # Création du UIManager
    ui_manager = pygame_gui.UIManager((1024, 900))

    # Création de la zone message
    zone_message = ZoneMessage(window, ui_manager)

    clock = pygame.time.Clock()
    running = True

    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            zone_message.handle_event(event)

        window.fill((30, 30, 30))  # fond global
        zone_message.update(time_delta)
        zone_message.afficher()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
