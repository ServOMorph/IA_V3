import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

import kivy
kivy.logger.Logger.disabled = True

from kivy.app import App
from kivy.core.window import Window
from ui.interface_main import MainUI
import ui.config_ui as cfg

class MainApp(App):
    def build(self):
        # Taille et position de la fenêtre
        Window.size = cfg.WINDOW_SIZE
        Window.left, Window.top = cfg.WINDOW_POSITION

        # Couleur et titre
        Window.clearcolor = cfg.BG_COLOR
        self.title = cfg.WINDOW_TITLE

        return MainUI()

if __name__ == "__main__":
    MainApp().run()
