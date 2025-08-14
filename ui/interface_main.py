from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
import ui.config_ui as cfg

class MainUI(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Image de fond
        self.background = Image(
            source=cfg.BACKGROUND_IMAGE,
            allow_stretch=True,
            keep_ratio=False
        )
        self.add_widget(self.background)
