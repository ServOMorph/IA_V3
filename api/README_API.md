# 📡 API – IA_V3

API HTTP (FastAPI) pour exposer les fonctionnalités du backend IA_V3.
Elle permet de connecter un frontend (Kivy, Web, etc.) sans dépendre de l’UI console.

---

## 🚀 Lancement

Depuis la racine du projet :

```bash
uvicorn api.main_api:app --reload --port 8000
```

Par défaut l’API sera accessible sur :  
`http://127.0.0.1:8000`

---

## 🔗 Endpoints

### 💬 Chat

* **POST /chat**  
  Envoyer un prompt à l’IA et recevoir une réponse.

  ```json
  { "prompt": "Quelle est la capitale de la France ?" }
  ```

  Réponse :

  ```json
  { "answer": "Paris" }
  ```

### 📂 Sessions

* **POST /sessions** → créer une nouvelle session.  
* **GET /sessions** → lister les sessions existantes.  
* **PUT /sessions/{name}/rename** → renommer une session.  
  - ⚠️ Particularité : si le fichier `.log` de la session est encore verrouillé par un logger, l’API renomme quand même le dossier et renvoie `200 OK`. Un avertissement est affiché côté serveur.
* **DELETE /sessions/{name}** → supprimer une session.  
* **GET /sessions/{name}/history** → récupérer l’historique complet.

### 📄 Fichiers

* **GET /files/{session}/{filename}**  
  Télécharger un fichier généré par l’IA (ex: `.py`, `.txt`, `.pdf`, etc.).

---

## 📁 Organisation

```
api/
 ├── main_api.py     # Point d'entrée FastAPI
 ├── deps.py         # Gestion des dépendances (ChatManager par session)
 ├── routes/
 │    ├── chat.py    # Routes chat
 │    ├── sessions.py# Routes sessions
 │    └── files.py   # Routes fichiers
 └── README_API.md   # Documentation
```

---

## 🖥️ Tests rapides (PowerShell)

Sous Windows PowerShell, utilisez `Invoke-RestMethod` :

```powershell
# Lister les sessions
Invoke-RestMethod -Uri "http://127.0.0.1:8000/sessions/" -Method Get

# Créer une session
Invoke-RestMethod -Uri "http://127.0.0.1:8000/sessions/" -Method Post

# Renommer une session
Invoke-RestMethod -Uri "http://127.0.0.1:8000/sessions/sav_conv_2025-09-13_23-42-53/rename?new_name=test-session" -Method Put

# Supprimer une session
Invoke-RestMethod -Uri "http://127.0.0.1:8000/sessions/test-session" -Method Delete
```

Ces commandes évitent les problèmes de compatibilité de `curl` sous PowerShell.
