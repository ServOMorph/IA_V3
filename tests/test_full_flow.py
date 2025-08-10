# tests/test_full_flow.py
import os
from pathlib import Path
from core.chat_manager import ChatManager

def run_full_flow():
    print("=== TEST FLUX COMPLET ===")
    
    # 1. Création du gestionnaire de chat
    chat = ChatManager(model="mistral", save_dir="sav")

    # 2. Commande /msg1
    print("\n>>> Test /msg1")
    chat.client.send_prompt("Quelle est la capitale de la France ?")
    chat.save_manager.save_txt(chat.client.history)

    # 3. Commande /msg2
    print("\n>>> Test /msg2")
    chat.client.send_prompt("Raconte moi une histoire en 20 caractères sur la ville dont tu viens de parler")
    chat.save_manager.save_txt(chat.client.history)

    # 4. Renommer
    print("\n>>> Test /rename")
    chat.save_manager.rename_session_file("test_conv")

    # 5. Charger
    print("\n>>> Test /load")
    loaded_content = chat.save_manager.load_session_file("test_conv")
    assert loaded_content is not None
    print(loaded_content)

    # 6. Vérifications des fichiers
    save_file = Path("sav/test_conv.txt")
    assert save_file.exists(), "❌ Le fichier de sauvegarde n'existe pas"
    print(f"✅ Fichier de sauvegarde trouvé : {save_file}")

    conv_log_file = Path(f"logs/test_conv.log")
    assert conv_log_file.exists(), "❌ Le fichier de log de conversation n'existe pas"
    print(f"✅ Fichier de log trouvé : {conv_log_file}")

    print("\n=== TEST TERMINÉ AVEC SUCCÈS ===")

if __name__ == "__main__":
    run_full_flow()
