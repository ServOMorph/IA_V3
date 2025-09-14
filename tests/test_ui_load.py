from client.ia_client import IAClient
from pathlib import Path
from config import SAVE_DIR
import shutil

def test_session_load_and_switch():
    client = IAClient()

    # Session 1
    client.send_message("Bonjour, test session 1")
    default_session = client.backend.save_manager.session_name
    assert (Path(SAVE_DIR) / default_session / "conversation.md").exists()

    # Préparer Session 2
    test2_session = Path(SAVE_DIR) / "test2"
    if test2_session.exists():
        shutil.rmtree(test2_session)
    test2_session.mkdir(parents=True, exist_ok=True)
    (test2_session / "conversation.md").write_text("# Conversation test2\n", encoding="utf-8")

    # Charger Session 2
    client.load_session("test2")
    assert client.backend.save_manager.session_name == "test2"
    assert (test2_session / "conversation.md").exists()
