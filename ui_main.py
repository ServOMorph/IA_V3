import os
import ctypes
from ctypes import wintypes
import pygame
import ui.config_ui  
from ui.zones.zone_chat import ZoneChat
from ui.zones.zone_liste_conv import ZoneListeConv
from ui.zones.zone_param import ZoneParam
from ui.zones.zone_message import ZoneMessage
from ui.zones.zone_info import ZoneInfo

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
    """Toujours moitié gauche de l'écran utilisable (sans barre des tâches)."""
    SM_CXSCREEN = 0
    SM_CXFULLSCREEN = 16
    SM_CYFULLSCREEN = 17

    screen_w = user32.GetSystemMetrics(SM_CXSCREEN)
    usable_h = user32.GetSystemMetrics(SM_CYFULLSCREEN)

    win_w = screen_w // 2
    win_h = usable_h
    pos_x = -6
    pos_y = 0

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
    pygame.display.set_caption("ServOMorph IA - V3")

    # Charger l'image de fond
    try:
        bg_path = os.path.join("assets", "images", "fond_window.png")
        background = pygame.image.load(bg_path).convert()
        background = pygame.transform.scale(background, (win_w, win_h))
    except pygame.error as e:
        print(f"Erreur chargement image de fond : {e}")
        background = None

    # Forcer la position
    try:
        hwnd = pygame.display.get_wm_info().get("window")
        if hwnd:
            force_window_pos(hwnd, pos_x, pos_y)
    except Exception:
        pass
    
    # --- Création des zones ---
    zone_chat = ZoneChat(window)
    zone_liste_conv = ZoneListeConv(window)
    zone_param = ZoneParam(window)
    zone_message = ZoneMessage(window)
    zone_info = ZoneInfo(window)
    

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                win_w, win_h = event.w, event.h
                if background:
                    background = pygame.image.load(bg_path).convert()
                    background = pygame.transform.scale(background, (win_w, win_h))

        if background:
            window.blit(background, (0, 0))
        else:
            window.fill(getattr(ui.config_ui, "WINDOW_BG_COLOR", (30, 30, 30)))

        # Affichage de la zone de chat
        zone_chat.afficher()
        zone_liste_conv.afficher()
        zone_param.afficher()
        zone_message.afficher()
        zone_info.afficher()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
