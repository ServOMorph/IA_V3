import requests, time

import os
BASE_URL = f"http://127.0.0.1:{os.getenv('API_PORT', '8001')}"


def test_chat():
    r = requests.post(f"{BASE_URL}/chat/", json={"prompt": "2+2"})
    assert r.status_code == 200
    assert "answer" in r.json()

def test_new_session():
    r = requests.post(f"{BASE_URL}/sessions/")
    assert r.status_code == 200
    assert "session" in r.json()
    global created_session
    created_session = r.json()["session"]

def test_list_sessions():
    r = requests.get(f"{BASE_URL}/sessions/")
    assert r.status_code == 200
    sessions = r.json().get("sessions", [])
    assert isinstance(sessions, list)
    assert created_session in sessions

def test_get_history():
    r = requests.get(f"{BASE_URL}/sessions/{created_session}/history")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)

def test_rename_session():
    global renamed_session
    renamed_session = f"renamed-{int(time.time())}"
    r = requests.put(f"{BASE_URL}/sessions/{created_session}/rename", params={"new_name": renamed_session})
    assert r.status_code == 200
    assert r.json().get("new") == renamed_session
    
def test_delete_session():
    r = requests.delete(f"{BASE_URL}/sessions/{renamed_session}")
    assert r.status_code == 200
    assert r.json().get("deleted") == renamed_session
