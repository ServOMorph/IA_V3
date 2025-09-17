import pytest
from core.chat_manager import ChatManager
from core.commands import CommandHandler

@pytest.fixture
def chat_manager(tmp_path, monkeypatch):
    # Redirige SAVE_DIR et LOGS_DIR vers un dossier temporaire
    monkeypatch.setattr("config.SAVE_DIR", tmp_path / "sav")
    monkeypatch.setattr("config.LOGS_DIR", tmp_path / "logs")

    cm = ChatManager()
    cm.save_manager.save_root = tmp_path / "sav"
    cm.save_manager.session_dir = cm.save_manager.save_root / cm.save_manager.session_name
    cm.save_manager.session_dir.mkdir(parents=True, exist_ok=True)
    cm.save_manager.session_md = cm.save_manager.session_dir / "conversation.md"
    cm.save_manager.session_md.write_text("# Conversation\n", encoding="utf-8")
    return cm

class TestRenameSession:
    def test_rename_active_session(self, chat_manager):
        handler = CommandHandler(chat_manager)
        old_name = chat_manager.save_manager.session_name
        new_name = "renamed_active"

        handled, _ = handler.handle(f"&rename {new_name}")
        assert handled

        new_dir = chat_manager.save_manager.save_root / new_name
        assert new_dir.exists()
        assert chat_manager.save_manager.session_name == new_name

    def test_rename_other_session(self, chat_manager):
        other_name = "other_session"
        other_dir = chat_manager.save_manager.save_root / other_name
        other_dir.mkdir(parents=True, exist_ok=True)
        (other_dir / "conversation.md").write_text("# Conversation autre\n", encoding="utf-8")

        handler = CommandHandler(chat_manager)
        new_name = "renamed_other"

        handled, _ = handler.handle(f"&rename {other_name} {new_name}")
        assert handled

        new_dir = chat_manager.save_manager.save_root / new_name
        assert new_dir.exists()
        assert not (chat_manager.save_manager.save_root / other_name).exists()

    def test_rename_conflict(self, chat_manager):
        handler = CommandHandler(chat_manager)
        old_name = chat_manager.save_manager.session_name

        conflict_name = "existing_session"
        conflict_dir = chat_manager.save_manager.save_root / conflict_name
        conflict_dir.mkdir(parents=True, exist_ok=True)
        (conflict_dir / "conversation.md").write_text("# Conversation existante\n", encoding="utf-8")

        handled, _ = handler.handle(f"&rename {conflict_name}")
        assert handled

        old_dir = chat_manager.save_manager.save_root / old_name
        assert old_dir.exists()
        assert conflict_dir.exists()
        assert chat_manager.save_manager.session_name == old_name

    def test_rename_no_argument(self, chat_manager, capsys):
        handler = CommandHandler(chat_manager)

        handled, _ = handler.handle("&rename")
        captured = capsys.readouterr()

        assert handled
        assert "Usage" in captured.out  # le message d'usage doit s'afficher
        # Le nom de session reste inchangé
        assert chat_manager.save_manager.session_dir.exists()
