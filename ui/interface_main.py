# ui/interface_main.py
from kivy.uix.floatlayout import FloatLayout
from ui.zones.zone_chat import ZoneChat
from ui.zones.zone_liste_conv import ZoneListeConv
from ui.zones.zone_param import ZoneParam
from ui.zones.zone_message import ZoneMessage
from ui.zones.zone_info import ZoneInfo

class MainUI(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Ajout des zones
        self.add_widget(ZoneListeConv())   # Liste conversations
        self.add_widget(ZoneParam())       # Paramètres
        self.add_widget(ZoneChat())        # Zone principale de chat
        self.add_widget(ZoneMessage())     # Zone de saisie de message
        self.add_widget(ZoneInfo())        # Zone info
