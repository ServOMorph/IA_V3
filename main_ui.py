from kivy.app import App
from kivy.core.window import Window
import ui.config_ui as cfg
from ui.interface_main import MainUI

class MainApp(App):
    def build(self):
        Window.size = cfg.WINDOW_SIZE
        Window.left, Window.top = cfg.WINDOW_POSITION
        Window.clearcolor = cfg.BG_COLOR
        self.title = cfg.WINDOW_TITLE
        return MainUI()

if __name__ == "__main__":
    MainApp().run()
