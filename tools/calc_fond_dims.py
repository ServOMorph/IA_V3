import ctypes

# Constantes Windows
SM_CXSCREEN = 0
SM_CYSCREEN = 1
SM_CXFULLSCREEN = 16  # largeur zone utilisable (sans barre des tâches)
SM_CYFULLSCREEN = 17  # hauteur zone utilisable (sans barre titre ni barre des tâches)

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

# Taille totale écran
screen_w = user32.GetSystemMetrics(SM_CXSCREEN)
screen_h = user32.GetSystemMetrics(SM_CYSCREEN)

# Taille zone utilisable
usable_w = user32.GetSystemMetrics(SM_CXFULLSCREEN)
usable_h = user32.GetSystemMetrics(SM_CYFULLSCREEN)

# Moitié gauche
window_w = screen_w // 2
window_h = usable_h  # on prend hauteur utilisable, pas la totale

print(f"📐 Résolution écran : {screen_w}x{screen_h}")
print(f"📐 Zone utilisable : {usable_w}x{usable_h}")
print(f"📐 Taille image idéale pour fond_window.png : {window_w}x{window_h}")
