import pytest
from pathlib import Path
from core.chat_manager import ChatManager
from core.commands import CommandHandler

def test_command_load(tmp_path):
    """
    Vérifie que la commande &load recharge bien une session existante.
    """
    # Créer un dossier de session avec conversation.md
    session_name = "sav_conv_2099-01-01_15-00-00"
    session_dir = tmp_path / session_name
    session_dir.mkdir(parents=True)
    (session_dir / "conversation.md").write_text(
        f"""# Conversation
_Dossier_: {session_name}
_Démarrée_: 2099-01-01 15:00:00

---
### 2099-01-01 15:01
**[user]**

Bonjour IA

### 2099-01-01 15:02
**[assistant]**

Bonjour humain
""",
        encoding="utf-8",
    )

    # Créer un ChatManager et rediriger save_root vers tmp_path
    cm = ChatManager()
    cm.save_manager.save_root = tmp_path
    handler = CommandHandler(cm)

    # Exécuter la commande &load
    handled, should_exit = handler.handle(f"&load {session_name}")

    # Vérifications
    assert handled is True
    assert should_exit is False
    assert cm.client.history, "L'historique devrait être rechargé"
    assert cm.client.history[0]["role"] == "user"
    assert "Bonjour IA" in cm.client.history[0]["content"]
    assert cm.client.history[1]["role"] == "assistant"
    assert "Bonjour humain" in cm.client.history[1]["content"]
