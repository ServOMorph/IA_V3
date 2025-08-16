# IA_V3 – Chat IA avec Ollama, gestion avancée des conversations et interface Kivy

## 📌 Description
Projet backend + UI pour interagir avec un modèle IA local via **Ollama** (par défaut `mistral`), avec gestion avancée des conversations et interface Kivy.

Fonctionnalités principales :
- Dialogue avec un modèle IA local.
- Sauvegarde des conversations dans un dossier par session (`/sav/<nom_session>/conversation.md`).
- Sauvegarde automatique des blocs de code Python extraits en `.py`.
- Chargement, renommage, suppression et organisation des sessions.
- Copie rapide des derniers messages dans le presse-papier (CLI).
- Conservation du contexte conversationnel.
- Logs techniques et conversationnels séparés (`/logs/<nom_session>.log`).
- Interface Kivy moderne avec zones distinctes : liste de conversations, chat, saisie, panneau info/config.
- Couleurs centralisées dans `ui/config_ui.py`.

---

## 🚀 Nouveautés et changements récents
- Séparation UI / logique :
  - Ajout d’un **client intermédiaire** `client/ia_client.py` pour découpler l’UI du backend.
  - `main_ui.py` devient un simple lanceur. UI scindée en `ui/app_main.py` (logique) et `ui/layout_builder.py` (construction visuelle).
  - `ui/` et `client/` sont des packages Python (fichiers `__init__.py`).

- Comportement des commandes `&` :
  - Les commandes `&...` restent disponibles **en CLI** (via `main.py`).
  - En **mode UI**, les commandes `&` ne sont pas exécutées. Elles sont réservées au mode CLI.

- UI / zone_chat :
  - Bulles adaptatives : largeur des bulles s’ajuste à la longueur du texte. Retour à la ligne activé correctement.
  - Couleurs des bulles et du texte prises depuis `ui/config_ui.py`.
  - Sélection de conversation colorée avec la même teinte utilisateur.
  - Curseur d’édition (`TextInput`) personnalisé : couleur et largeur contrôlées depuis `ui/config_ui.py`.

- Centralisation des couleurs :
  - `ui/config_ui.py` contient désormais les constantes :
    - `COLOR_USER_BUBBLE`, `COLOR_USER_TEXT`
    - `COLOR_IA_BUBBLE`, `COLOR_IA_TEXT`
    - `COLOR_CURSOR`
  - Ces constantes sont réutilisées par `zone_chat`, `zone_message` et `zone_liste_conv`.

- Sauvegarde / synthèse :
  - Sauvegardes MD/TXT et extraction de code gérées par le backend.  
  - (Rappel) Commande spéciale de clôture (CLI) génère synthèse textuelle et README mis à jour — production de contenu à fournir à l’appel de clôture.

---

## 📂 Structure du projet (mise à jour)
```
IA_V3/
│
├── client/
│   ├── __init__.py
│   └── ia_client.py          # wrapper entre UI et backend (possible remplacement HTTP)
│
├── core/                     # backend (chat_manager, ollama client, save_manager, commands, logs...)
│   ├── chat_manager.py
│   ├── ollama_client.py
│   ├── sav_manager.py
│   ├── commands.py
│   └── logging/
│
├── ui/
│   ├── __init__.py
│   ├── config_ui.py          # configuration UI + couleurs centralisées
│   ├── app_main.py           # MyApp + logique d'interaction UI ↔ client
│   ├── layout_builder.py     # construction visuelle (zones, BackgroundBox, ColoredBox)
│   ├── zones/
│   │   ├── __init__.py
│   │   ├── zone_chat.py
│   │   ├── zone_message.py
│   │   ├── zone_message.kv
│   │   ├── zone_liste_conv.py
│   │   └── zone_liste_conv.kv
│   └── behaviors/
│       └── hover_behavior.py
│
├── assets/
│   └── images/
│       ├── fond_window.png
│       ├── send_icon.png
│       └── Logo_IA.png
│
├── logs/
├── sav/
├── syntheses/                 # dossier centralisé pour synthèses (nouveau)
│
├── tools/
│   └── update_system_prompt.py
│
├── config.py                  # paramètres backend (system prompt, etc.)
├── main.py                    # CLI launcher
├── main_ui.py                 # wrapper pour lancer l'UI (exécute ui.app_main.MyApp)
└── README.md
```

---

## 🖥️ Lancer le projet

### Interface en ligne de commande (CLI)
```bash
python main.py
```
(ici les commandes `&` sont actives et exécutées par `core/commands.py`)

### Interface graphique (UI Kivy)
```bash
python main_ui.py
```
- UI utilise `client/ia_client.py` pour communiquer avec le backend.
- Les commandes `&` ne sont pas exécutées par l’UI.

---

## 📜 Commandes (CLI)
Liste des commandes utilisables en **mode CLI** (certaines sont implémentées dans `core/commands.py`) :
- `&q` / `&exit` : sauvegarder et quitter / quitter sans sauvegarder  
- `&help` : afficher la liste des commandes  
- `&rename NOM` : renommer la session active  
- `&load chemin/NOM` : charger une session  
- `&suppr chemin/NOM` : supprimer session + log (recrée une session vide si active)  
- `&new` : nouvelle session vide  
- `&copie_IA` / `&copie_user` : copier dernier message IA / utilisateur dans le presse-papier  
- `&createfolder NOM` : créer dossier d’organisation dans `/sav` et `/logs`  
- `&move NOM_CONV DOSSIER` : déplacer une session  
- `&savecode [base]` / `&savetxt [base]` : extraire et sauvegarder dernier code / texte  

> Remarque : l’UI affiche les commandes si elles sont tapées, mais **ne les exécute pas**. Utiliser la CLI pour actions de gestion en masse.

---

## 🗂️ Répertoires et fichiers importants
- `sav/` : sessions sauvegardées (par session : `conversation.md`, `conversation.txt`, extraits `.py`, etc.)  
- `logs/` : logs techniques et conversationnels (par session)  
- `syntheses/` : synthèses de sessions produites à la clôture  
- `ui/config_ui.py` : centralise toutes les couleurs et dimensions de l’UI  
- `client/ia_client.py` : point d’extension pour remplacer backend local par API HTTP si souhaité

---

## 🔧 Notes d’implémentation importantes
- `zone_chat.ChatBubble` s’ajuste automatiquement à la longueur du texte. Le wrapping utilise `Label.text_size=(width, None)` + `texture_update()` pour un rendu correct.
- `zone_message.kv` importe `ui.config_ui` pour utiliser `COLOR_CURSOR`.
- `zone_liste_conv.kv` utilise `COLOR_USER_BUBBLE` pour la mise en évidence de la sélection.
- Architecture orientée-objet pour faciliter l’ajout de nouvelles IA ou frontends.

---

## ✍️ Suggestions d’évolutions
- Exposer un backend HTTP (FastAPI) et fournir un `client/ia_client_http.py`.  
- Ajouter support d’images et pièces jointes dans les bulles.  
- Ajouter panneau de configuration dynamique dans l’UI (sélection modèle, température, historique à conserver).
