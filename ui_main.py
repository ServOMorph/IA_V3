import os
import ctypes
from ctypes import wintypes
import pygame
import config

# --- Win32
user32 = ctypes.windll.user32

# Constantes pour positionnement
SWP_NOSIZE       = 0x0001
SWP_NOZORDER     = 0x0004
SWP_NOACTIVATE   = 0x0010

def get_screen_size():
    """Retourne la taille de l'écran principal."""
    try:
        user32.SetProcessDPIAware()
    except Exception:
        pass
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def compute_window_geometry():
    screen_w, screen_h = get_screen_size()
    win_w = screen_w // 2
    win_h = screen_h

    # Appliquer réduction hauteur
    win_h += getattr(config, "WINDOW_HEIGHT_ADJUST", 0)

    align = (getattr(config, "WINDOW_ALIGN", "left") or "left").lower()
    pos_x = screen_w - win_w if align == "right" else 0
    pos_x += getattr(config, "WINDOW_X_OFFSET", 0)

    pos_y = getattr(config, "WINDOW_Y_OFFSET", 0)

    return pos_x, pos_y, win_w, win_h

def force_window_pos(hwnd, x, y):
    """Force la position de la fenêtre via l'API Win32."""
    user32.SetWindowPos(wintypes.HWND(hwnd), None, x, y, 0, 0,
                        SWP_NOSIZE | SWP_NOZORDER | SWP_NOACTIVATE)

def main():
    # Géométrie souhaitée
    pos_x, pos_y, win_w, win_h = compute_window_geometry()

    # Positionner avant init Pygame
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{pos_x},{pos_y}"

    pygame.init()
    window = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
    pygame.display.set_caption("IA_V3 - Interface Pygame (moitié d'écran)")

    # Forcer la position
    try:
        hwnd = pygame.display.get_wm_info().get("window")
        if hwnd:
            force_window_pos(hwnd, pos_x, pos_y)
    except Exception:
        pass

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(getattr(config, "WINDOW_BG_COLOR", (30, 30, 30)))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
