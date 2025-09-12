# tests/test_command_export.py
import pytest
from pathlib import Path

from core.commands import CommandHandler


class DummyClient:
    """Simule un client IA avec un historique minimal."""
    def __init__(self, response):
        self.history = [{"response": response}]


class DummySaveManager:
    """Simule un save_manager avec un répertoire de session."""
    def __init__(self, tmp_path):
        self.session_dir = tmp_path / "session_test"
        self.session_dir.mkdir(parents=True, exist_ok=True)


@pytest.mark.parametrize("ext", ["txt", "py"])
def test_export_with_blocks(tmp_path, ext, monkeypatch):
    # Redirige SAVE_DIR vers tmp_path/sav
    monkeypatch.setattr("config.SAVE_DIR", tmp_path / "sav")

    # réponse IA avec deux blocs
    response = f"""
    Voici un exemple :
    ```{ext}
    ligne 1
    ```
    ```{ext}
    ligne 2
    ```
    """

    client = DummyClient(response)
    save_manager = DummySaveManager(tmp_path)

    class DummyChatManager:
        pass

    chat_manager = DummyChatManager()
    chat_manager.client = client
    chat_manager.save_manager = save_manager

    handler = CommandHandler(chat_manager)

    ok, stop = handler.handle(f"&export fichier {ext}")
    assert ok is True
    assert stop is False

    # vérifier que deux fichiers ont bien été créés
    files = list((tmp_path / "sav" / "session_test" / "files_out").rglob(f"*.{ext}"))
    assert len(files) == 2
    contents = [f.read_text(encoding="utf-8").strip() for f in files]
    assert any("ligne 1" in c for c in contents)
    assert any("ligne 2" in c for c in contents)


def test_export_without_blocks(tmp_path, monkeypatch):
    # Redirige SAVE_DIR vers tmp_path/sav
    monkeypatch.setattr("config.SAVE_DIR", tmp_path / "sav")

    response = "Ceci est une réponse brute."
    client = DummyClient(response)
    save_manager = DummySaveManager(tmp_path)

    class DummyChatManager:
        pass

    chat_manager = DummyChatManager()
    chat_manager.client = client
    chat_manager.save_manager = save_manager

    handler = CommandHandler(chat_manager)

    ok, stop = handler.handle("&export rapport txt")
    assert ok is True
    assert stop is False

    files = list((tmp_path / "sav" / "session_test" / "files_out").rglob("*.txt"))
    assert len(files) == 1
    assert files[0].read_text(encoding="utf-8").strip() == response
