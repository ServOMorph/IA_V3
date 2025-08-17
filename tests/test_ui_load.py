from client.ia_client import IAClient
from pathlib import Path
from config import SAVE_DIR

# Init client
client = IAClient()

# 1) Envoie un premier message dans la session par défaut
print(">>> Premier message (session par défaut)")
client.send_message("Bonjour, test session 1")

# Vérifie la sauvegarde
default_session = client.backend.save_manager.session_name
print(f"Session active après 1er message : {default_session}")
print("Contenu conversation.md :")
print((Path(SAVE_DIR) / default_session / "conversation.md").read_text(encoding="utf-8"))

# 2) Charge une autre session (ex: "test2")
print("\n>>> On charge la session test2")
client.load_session("test2")

print(f"Session active maintenant : {client.backend.save_manager.session_name}")

# 3) Envoie un message dans la nouvelle session
client.send_message("Bonjour, test session 2")

# Vérifie que ça s’est bien enregistré dans test2/conversation.md
print("Contenu conversation.md (test2) :")
print((Path(SAVE_DIR) / "test2" / "conversation.md").read_text(encoding="utf-8"))

# 4) Vérifie que la session initiale n’a pas bougé
print("\nRelecture de la première session :")
print((Path(SAVE_DIR) / default_session / "conversation.md").read_text(encoding="utf-8"))
