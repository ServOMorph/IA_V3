import requests, time

BASE_URL = "http://127.0.0.1:8000"

def test_chat():
    print("=== Test /chat ===")
    r = requests.post(f"{BASE_URL}/chat/", json={"prompt": "2+2"})
    print("Response:", r.status_code, r.json())

def test_new_session():
    print("\n=== Test POST /sessions ===")
    r = requests.post(f"{BASE_URL}/sessions/")
    print("Response:", r.status_code, r.json())
    return r.json().get("session")

def test_list_sessions():
    print("\n=== Test GET /sessions ===")
    r = requests.get(f"{BASE_URL}/sessions/")
    print("Response:", r.status_code, r.json())
    return r.json().get("sessions", [])

def test_get_history(session):
    print(f"\n=== Test GET /sessions/{session}/history ===")
    r = requests.get(f"{BASE_URL}/sessions/{session}/history")
    print("Response:", r.status_code)
    print(r.json())

def test_rename_session(session):
    new_name = f"renamed-{int(time.time())}"  # nom unique basé sur timestamp
    print(f"\n=== Test PUT /sessions/{session}/rename ===")
    r = requests.put(f"{BASE_URL}/sessions/{session}/rename", params={"new_name": new_name})
    print("Response:", r.status_code, r.json())
    return new_name

def test_delete_session(session):
    print(f"\n=== Test DELETE /sessions/{session} ===")
    r = requests.delete(f"{BASE_URL}/sessions/{session}")
    print("Response:", r.status_code, r.json())

if __name__ == "__main__":
    test_chat()
    session_name = test_new_session()
    sessions = test_list_sessions()
    if session_name:
        test_get_history(session_name)
        renamed = test_rename_session(session_name)
        test_delete_session(renamed)
