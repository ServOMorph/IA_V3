# IA_V3 – Chat IA avec Ollama et gestion avancée des conversations

## 📌 Description
Ce projet permet d’interagir avec un modèle IA local via **Ollama** (par défaut `mistral`), tout en gérant automatiquement :
- La sauvegarde des conversations (`/sav`)
- Le chargement de sessions précédentes
- Le renommage des conversations
- La conservation du contexte à chaque échange
- Des logs détaillés dans des fichiers séparés

Le but est d’offrir une expérience de chat cohérente et persistante.

---

## 📂 Structure du projet
```
IA_V3/
│
├── core/                   # Modules principaux
│   ├── chat_manager.py     # Gestion de la boucle principale du chat
│   ├── ollama_client.py    # Communication avec Ollama + gestion du contexte
│   ├── sav_manager.py      # Sauvegarde et chargement des conversations
│   ├── commands.py         # Commandes disponibles
│   ├── logger.py           # Logger global (debug.log)
│   └── conv_logger.py      # Logger des prompts/réponses
│
├── logs/                   # Logs de conversation (.log)
├── sav/                    # Sauvegardes de conversations (.txt)
├── docs/                   # Documentation et synthèses
│
├── tests/                  # Tests automatisés
│
├── main.py                 # Point d’entrée de l’application
└── README.md               # Ce fichier
```

---

## 🚀 Installation

### 1️⃣ Installer Ollama
Télécharge et installe Ollama selon ton OS :  
👉 [https://ollama.ai/download](https://ollama.ai/download)

### 2️⃣ Installer Python et les dépendances
```bash
pip install requests
```

---

## 🖥️ Utilisation

Lancer le programme :
```bash
python main.py
```

---

## 📜 Commandes disponibles

| Commande         | Description |
|------------------|-------------|
| `/q`             | Sauvegarder la conversation et quitter |
| `/exit`          | Quitter sans sauvegarder |
| `/help`          | Afficher la liste des commandes |
| `/rename NOM`    | Renommer la conversation actuelle |
| `/msg1`          | Demande pré-enregistrée : "Quelle est la capitale de la France ?" |
| `/msg2`          | Demande pré-enregistrée : "Raconte-moi une histoire en 20 caractères sur la ville dont tu viens de parler" |
| `/load NOM`      | Charger une conversation sauvegardée depuis `/sav` |

---

## 🗂️ Sauvegardes & Logs

- Les **conversations** sont sauvegardées dans `sav/` sous la forme :
  ```
  sav_conv_YYYY-MM-DD_HH-MM-SS.txt
  ```
- Les **logs de debug** sont enregistrés dans :
  ```
  debug.log
  ```
- Les **logs de conversation** (prompts/réponses envoyés à l’IA) sont enregistrés dans `logs/` :
  ```
  sav_conv_YYYY-MM-DD_HH-MM-SS.log
  ```

---

## 🧪 Tests
Les tests sont situés dans `tests/`.

Exécuter un test :
```bash
python -m tests.test_full_flow
```

---

## 📌 Auteurs
Développé avec ❤️ par **Raphaël** et **ChatGPT**.
