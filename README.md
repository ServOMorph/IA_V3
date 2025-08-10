# IA_V3 – Chat IA avec Ollama et gestion avancée des conversations

## 📌 Description
Ce projet permet d’interagir avec un modèle IA local via **Ollama** (par défaut `mistral`), tout en gérant automatiquement :
- La sauvegarde des conversations (`/sav`)
- Le chargement de sessions précédentes
- Le renommage des conversations
- La conservation du contexte à chaque échange
- Des logs détaillés dans des fichiers séparés

## 🚀 Nouveautés
- **Centralisation des constantes** dans `config.py` :
  - Paramètres Ollama (`OLLAMA_BASE_URL`, `DEFAULT_MODEL`, `OLLAMA_TIMEOUT`)
  - Répertoires (`SAVE_DIR`, `LOGS_DIR`)
  - Formats de fichiers de sauvegarde
  - Messages système et pré-enregistrés
- **Réorganisation des loggers** :
  - `core/logging/logger.py` → Logger global (`debug.log`)
  - `core/logging/conv_logger.py` → Logger conversationnel (par session)

## 📂 Structure du projet
IA_V3/
│
├── core/
│ ├── chat_manager.py
│ ├── ollama_client.py
│ ├── sav_manager.py
│ ├── commands.py
│ ├── logging/
│ │ ├── logger.py
│ │ └── conv_logger.py
│
├── logs/
├── sav/
├── config.py
├── main.py
└── README.md


## 🖥️ Utilisation
```bash
python main.py

📜 Commandes disponibles
Commande	Description
/q	Sauvegarder la conversation et quitter
/exit	Quitter sans sauvegarder
/help	Afficher la liste des commandes
/rename NOM	Renommer la conversation actuelle
/msg1	Demande pré-enregistrée 1
/msg2	Demande pré-enregistrée 2
/load NOM	Charger une conversation sauvegardée
🗂️ Sauvegardes & Logs

    Conversations : sav/

    Logs techniques : debug.log

    Logs conversationnels : logs/


