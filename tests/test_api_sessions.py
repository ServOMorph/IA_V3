import requests
import time
import os
from pathlib import Path
import config

BASE = "http://127.0.0.1:8001"

def test_api_create_and_rename_session(tmp_path):
    # 1. Créer une nouvelle session
    r = requests.post(f"{BASE}/sessions/")
    assert r.status_code == 200
    session_name = r.json()["session"]
    session_dir = Path(config.SAVE_DIR) / session_name

    # Vérifier que le dossier a été créé
    assert session_dir.exists(), f"Dossier non trouvé: {session_dir}"
    assert (session_dir / "conversation.md").exists()

    # 2. Renommer avec un nom unique
    new_name = f"test_api_{int(time.time())}"
    r2 = requests.put(
        f"{BASE}/sessions/{session_name}/rename",
        params={"new_name": new_name}
    )
    assert r2.status_code == 200, f"Réponse API: {r2.text}"
    data = r2.json()
    assert data["old_name"] == session_name
    assert data["new_name"] == new_name

    # Vérifier que l'ancien dossier a disparu
    assert not session_dir.exists()
    # Vérifier que le nouveau dossier existe
    new_dir = Path(config.SAVE_DIR) / new_name
    assert new_dir.exists()
    assert (new_dir / "conversation.md").exists()

    # 3. Vérifier via l'API que le nouveau nom est bien listé
    r3 = requests.get(f"{BASE}/sessions/")
    assert r3.status_code == 200
    sessions = r3.json()["sessions"]
    assert new_name in sessions
    assert session_name not in sessions
