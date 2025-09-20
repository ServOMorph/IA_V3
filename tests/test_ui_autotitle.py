# tests/test_ui_autotitle.py
import sys
import importlib
from pathlib import Path
import pytest

# Ajouter le dossier racine IA_V3 dans le PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from api.routes import sessions, chat
import config

@pytest.fixture
def temp_sessions(tmp_path, monkeypatch):
    # Rediriger SAVE_DIR vers un dossier temporaire
    new_sav = tmp_path / "sav"
    monkeypatch.setattr("config.SAVE_DIR", new_sav)
    new_sav.mkdir(parents=True, exist_ok=True)

    # Recharger config lui-même
    import importlib, config
    importlib.reload(config)

    # Recharger les modules qui importent SAVE_DIR
    import core.sav_manager
    import core.session_manager
    import core.chat_manager
    importlib.reload(core.sav_manager)
    importlib.reload(core.session_manager)
    importlib.reload(core.chat_manager)

    # Vider le dict global
    from api.routes import sessions
    sessions.chat_managers.clear()

    yield tmp_path

def test_auto_rename_in_ui_flow(temp_sessions):
    # 1. Créer une nouvelle session via l'API
    resp = sessions.new_session()
    old_name = resp["session"]
    cm = sessions.chat_managers[old_name]

    # Forcer un historique minimal : 1 user + 1 assistant
    cm.client.history.append({"role": "user", "content": "Bonjour"})
    cm.client.history.append({"role": "assistant", "content": "Salut, je suis VertIA"})

    # Monkeypatch AutoTitler pour qu'il renvoie un titre fixe
    cm.auto_titler.done = False
    def fake_title(_):
        return "TitreCourt"
    cm.auto_titler.maybe_generate_title = fake_title

    # 2. Appeler l'endpoint /chat comme ferait l'UI
    from api.routes.chat import chat_endpoint, PromptRequest
    result = chat_endpoint(old_name, PromptRequest(prompt="Test UI"))
    assert "answer" in result
    assert "session" in result
    new_name = result["session"]

    # 3. Vérifier que le dossier a été renommé
    new_dir = Path(config.SAVE_DIR) / new_name
    assert new_dir.exists(), f"Le dossier n'a pas été renommé : {new_dir}"

    # 4. Vérifier que chat_managers a été mis à jour
    assert new_name in sessions.chat_managers
    assert old_name not in sessions.chat_managers
