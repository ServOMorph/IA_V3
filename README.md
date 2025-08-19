# IA\_V3 – Chat IA avec Ollama, gestion avancée des conversations et interface Kivy

## 📌 Description

Projet backend + UI pour interagir avec un modèle IA local via **Ollama** (par défaut `mistral`), avec gestion avancée des conversations et interface Kivy.

### Fonctionnalités principales :

* Dialogue avec un modèle IA local.
* Sauvegarde des conversations dans un **dossier par session** (`/sav/<nom_session>/conversation.md`).
* Sauvegarde automatique des blocs de code Python extraits en `.py`.
* Chargement, renommage, suppression et organisation des sessions.
* Copie rapide des derniers messages dans le presse-papier (CLI).
* Conservation du contexte conversationnel.
* Logs techniques et conversationnels séparés (`/logs/<nom_session>.log`).
* **Interface Kivy moderne** avec zones distinctes : liste de conversations, chat, saisie, panneau info/config.
* Couleurs centralisées dans `ui/config_ui.py`.

---

## 🚀 Nouveautés et changements récents

### Nouvelles fonctionnalités CLI :

* Ajout de la commande `&run` : exécute le dernier script Python sauvegardé de la conversation en cours.
  → Un nouveau terminal Windows (`cmd.exe`) s'ouvre et lance le script (`python <fichier>`), permettant d'exécuter aussi bien des petits scripts que de gros programmes interactifs (jeux, Pygame, etc.).
* Amélioration de la saisie utilisateur en mode CLI :
  → Une ligne simple : taper Entrée envoie directement.
  → Texte multi-lignes (ex. copier-coller de résultats de console) : terminer par une ligne vide (Entrée deux fois).

### Séparation UI / logique :

* Ajout d’un client intermédiaire `client/ia_client.py` pour découpler l’UI du backend.
* `main_ui.py` devient un simple lanceur.
* UI scindée en `ui/app_main.py` (logique) et `ui/layout_builder.py` (construction visuelle).
* `ui/` et `client/` sont des packages Python (`__init__.py`).

### Comportement des commandes `&` :

* Les commandes `&...` restent disponibles en CLI (via `main.py`).
* En mode UI, elles ne sont pas exécutées. Elles sont réservées au mode CLI.

### UI / zone\_chat et zone\_message :

* Bulles adaptatives : largeur ajustée au texte, retour à la ligne activé.
* Couleurs des bulles et du texte centralisées (`ui/config_ui.py`).
* Sélection de conversation colorée avec la même teinte utilisateur.
* Curseur (TextInput) personnalisé : couleur et largeur configurables.
* **Ajout de commandes spéciales en UI** : `&msg1` et `&msg2` détectées et exécutées correctement côté client.
* **Bouton "+" ajouté en haut de la liste des conversations**, avec effet hover (icône éclaircie au survol).
* **Création de nouvelle conversation** depuis l’UI :

  * Un clic sur le bouton `+` crée un nouveau dossier de sauvegarde (`sav_conv_<horodatage>`).
  * La liste des conversations est rafraîchie automatiquement et sélectionne la nouvelle entrée.
  * La zone de chat est vidée pour démarrer proprement.
* **Filtrage du prompt système** : le message système initial (`role: system`) est conservé côté backend mais n’est plus affiché dans l’UI.

### Centralisation des couleurs :

`ui/config_ui.py` contient :

* `COLOR_USER_BUBBLE`, `COLOR_USER_TEXT`
* `COLOR_IA_BUBBLE`, `COLOR_IA_TEXT`
* `COLOR_CURSOR`

### Sauvegarde / synthèse :

* Sauvegardes MD/TXT et extraction de code gérées par le backend.
* Commande spéciale de clôture (CLI) génère synthèse textuelle et README mis à jour.

### Refactorisation sessions :

* Nouveau module `core/session_manager.py` pour gérer les sessions :

  * `rename_session(chat_manager, new_name)`
  * `delete_session(chat_manager, name)`
* `commands.py` (CLI) et `IAClient` (UI) passent par ce module.
* `ChatManager` reste focalisé sur la logique de chat, sans gérer les fichiers/sessions.

---

## 📂 Structure du projet (mise à jour)

```
.
├── main.py                         # Point d'entrée CLI
├── main_ui.py                      # Lanceur interface Kivy
├── client/
│   ├── __init__.py
│   └── ia_client.py                # Client intermédiaire UI ↔ backend
├── core/
│   ├── __init__.py
│   ├── chat_manager.py             # Gestion du chat (mode CLI)
│   ├── commands.py                 # Commandes CLI (&...)
│   ├── session_manager.py          # Gestion des sessions (rename, delete)
│   ├── ollama_client.py            # Client Ollama (modèle IA local)
│   ├── sav_manager.py              # Sauvegardes .md / .py / .txt
│   └── logging/
│       ├── __init__.py
│       └── conv_logger.py          # Logs conversationnels
├── ui/
│   ├── __init__.py
│   ├── app_main.py                 # Logique principale UI
│   ├── layout_builder.py           # Construction visuelle UI
│   ├── config_ui.py                # Couleurs, textes et constantes UI
│   └── zones/
│       ├── zone_chat.py
│       ├── zone_message.py
│       ├── zone_liste_conv.py      # Liste conv + bouton + avec hover & création conv
│       ├── zone_param.py
│       └── zone_info.py
├── sav/                            # Dossiers de sauvegarde des conversations
│   └── <nom_session>/conversation.md
├── logs/                           # Journaux conversationnels
│   └── <nom_session>.log
└── README.md
```
