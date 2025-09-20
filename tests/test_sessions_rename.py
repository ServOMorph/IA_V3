import sys
from pathlib import Path

# Ajouter le dossier racine du projet dans sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from fastapi.testclient import TestClient

from api.main_api import app
from api.routes.sessions import chat_managers
from config import SAVE_DIR

client = TestClient(app)

def test_rename_session(tmp_path, monkeypatch):
    # Patcher SAVE_DIR utilisé dans SaveManager
    monkeypatch.setattr("config.SAVE_DIR", tmp_path)
    monkeypatch.setattr("core.save_manager.SAVE_DIR", tmp_path)

    from api.main_api import app
    client = TestClient(app)

    # Créer une session via API
    res = client.post("/sessions/")
    assert res.status_code == 200
    name = res.json()["session"]

    old_dir = tmp_path / name
    assert old_dir.exists()
    assert (old_dir / "conversation.md").exists()

    # Renommer via API
    new_name = "test_session"
    res = client.put(f"/sessions/{name}/rename?new_name={new_name}")
    assert res.status_code == 200

    new_dir = tmp_path / new_name
    assert new_dir.exists()
    assert not old_dir.exists()
