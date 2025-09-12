import pytest
from pathlib import Path
from core.chat_manager import ChatManager

def test_resume_session(tmp_path):
    """
    Vérifie que resume_session recharge bien une conversation existante.
    """
    # Préparer un faux dossier de session
    session_name = "sav_conv_2099-01-01_12-00-00"
    session_dir = tmp_path / session_name
    session_dir.mkdir(parents=True)

    md_file = session_dir / "conversation.md"
    md_file.write_text(
        f"""# Conversation
_Dossier_: {session_name}
_Démarrée_: 2099-01-01 12:00:00

---
### 2099-01-01 12:01  
**[user]**

Bonjour IA

### 2099-01-01 12:02  
**[assistant]**

Bonjour humain
""",
        encoding="utf-8",
    )

    # Créer un ChatManager mais rediriger SAVE_DIR vers tmp_path
    cm = ChatManager()
    cm.save_manager.save_root = tmp_path

    # Reprendre la session
    ok = cm.resume_session(session_name)

    assert ok, "Le chargement de session a échoué"
    assert cm.client.history, "L'historique est vide après chargement"
    assert cm.client.history[0]["role"] == "user"
    assert "Bonjour IA" in cm.client.history[0]["content"]
    assert cm.client.history[1]["role"] == "assistant"
    assert "Bonjour humain" in cm.client.history[1]["content"]


def test_resume_session_with_summary(tmp_path):
    """
    Vérifie que resume_session recharge aussi le fichier summary.md s'il existe.
    """
    # Préparer un faux dossier de session
    session_name = "sav_conv_2099-01-01_13-00-00"
    session_dir = tmp_path / session_name
    session_dir.mkdir(parents=True)

    # conversation.md minimal
    (session_dir / "conversation.md").write_text(
        f"""# Conversation
_Dossier_: {session_name}
_Démarrée_: 2099-01-01 13:00:00

---
### 2099-01-01 13:01  
**[user]**

Reprise test
""",
        encoding="utf-8",
    )

    # summary.md factice
    summary_text = "## Résumé global\n\n- **Faits clés :** Test résumé\n"
    (session_dir / "summary.md").write_text(summary_text, encoding="utf-8")

    # ChatManager + redirection
    cm = ChatManager()
    cm.save_manager.save_root = tmp_path

    # Recharger session
    ok = cm.resume_session(session_name)
    assert ok, "Le chargement de session a échoué"

    # Vérifier que Summarizer pointe bien sur le bon summary.md
    assert cm.summarizer.summary_file.exists()
    assert "Test résumé" in cm.summarizer.load_summary()
