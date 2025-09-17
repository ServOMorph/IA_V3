import requests
import time

BASE = "http://127.0.0.1:8001"

# 1. Créer une session
r = requests.post(f"{BASE}/sessions/")
if r.status_code != 200:
    print("❌ Erreur création session:", r.text)
    exit(1)

old_name = r.json()["session"]
print("✅ Session créée :", old_name)

# 2. Renommer avec un nom unique basé sur timestamp
new_name = f"test_api_{int(time.time())}"
r2 = requests.put(f"{BASE}/sessions/{old_name}/rename", params={"new_name": new_name})

if r2.status_code == 200:
    print("✅ Session renommée :", r2.json())
else:
    print(f"❌ Erreur renommage (status {r2.status_code}):", r2.text)
    exit(1)

# 3. Vérifier la liste des sessions
r3 = requests.get(f"{BASE}/sessions/")
if r3.status_code == 200:
    sessions = r3.json()["sessions"]
    print("📂 Sessions existantes :", sessions)

    if new_name in sessions:
        print("✅ Le nouveau nom est bien présent :", new_name)
    else:
        print("❌ Le nouveau nom n'apparaît pas dans la liste !")

    if old_name not in sessions:
        print("✅ L'ancien nom a bien disparu :", old_name)
    else:
        print("❌ L'ancien nom est encore présent :", old_name)
else:
    print("❌ Erreur récupération sessions:", r3.text)
