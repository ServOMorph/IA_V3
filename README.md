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
* Mode **DEV** :

  * Liste les modèles Ollama installés au démarrage.
  * Permet de choisir le modèle IA à utiliser.
  * Affiche et logge le temps de réponse pour chaque prompt.
  * Sauvegarde chaque essai et benchmark dans `data/dev_responses.log` et `data/dev_responses.jsonl`.

---

## 🚀 Nouveautés et changements récents

### Nouvelles fonctionnalités CLI :

* Ajout de la commande `&run` : exécute le dernier script Python sauvegardé de la conversation en cours.
  → Un nouveau terminal Windows (`cmd.exe`) s'ouvre et lance le script (`python <fichier>`).
* Amélioration de la saisie utilisateur en mode CLI :
  → Une ligne simple : taper Entrée envoie directement.
  → Texte multi-lignes : terminer par une ligne vide (Entrée deux fois).
* Ajout d’un script **`tools/benchmark_responses.py`** :

  * Choix du modèle IA au lancement (si DEV\_MODE activé).
  * Choix du prompt à envoyer.
  * Envoi automatique du même prompt plusieurs fois (benchmark).
  * Affichage du temps de réponse par essai et calcul de stats (moyenne/min/max).
  * Résultats sauvegardés dans `data/dev_responses.*`.

### Séparation UI / logique :

* Ajout d’un client intermédiaire `client/ia_client.py`.
* `main_ui.py` devient un simple lanceur.
* UI scindée en `ui/app_main.py` (logique) et `ui/layout_builder.py` (construction visuelle).
* `ui/` et `client/` sont des packages Python (`__init__.py`).

### UI / zone\_chat et zone\_message :

* Bulles adaptatives avec retour à la ligne.
* Couleurs centralisées (`ui/config_ui.py`).
* Boutons copier sous chaque bulle (copie presse-papier + coche temporaire).
* Création de nouvelle conversation via bouton `+`.
* Détection et exécution des commandes spéciales `&msg1`, `&msg2`, `&run`.

### Centralisation des couleurs et icônes :

* `COLOR_USER_BUBBLE`, `COLOR_IA_BUBBLE`, etc.
* Icônes copier et coche avec effet hover.

### Sauvegarde / synthèse :

* Sauvegardes MD/TXT et extraction de code gérées par le backend.
* Commande spéciale de clôture (CLI) génère synthèse et README mis à jour.

### Refactorisation sessions :

* Nouveau module `core/session_manager.py`.
* `commands.py` (CLI) et `IAClient` (UI) passent par ce module.
* `ChatManager` reste focalisé sur la logique de chat.

---

## 📂 Structure du projet (mise à jour)

```
📁 IA_V3/
    📄 arborescence.txt
    📄 config.py
    📄 debug.log
    📄 main.py
    📄 main_ui.py
    📄 README.md
    📁 assets/
        📁 images/
            📄 coche_icon.png
            📄 copier_icon.png
            📄 fond_window.png
            📄 Logo_IA.png
            📄 plus_icon.png
            📄 send_icon.png
            📄 send_icon2.png
    📁 client/
        📄 ia_client.py
        📄 __init__.py
    📁 core/
        📄 chat_manager.py
        📄 commands.py
        📄 ollama_client.py
        📄 sav_manager.py
        📄 session_manager.py
        📄 startup_utils.py
        📄 __init__.py
        📁 logging/
            📄 conv_logger.py
            📄 logger.py
            📄 __init__.py
    📁 data/
        📄 dev_responses.jsonl
        📄 dev_responses.log
        📄 models_list.txt
    📁 logs/
        📄 conversation.log
        📄 sav_conv_*.log
        📄 test11.log
        📄 test12.log
    📁 sav/
        📁 sav_conv_*/
            📄 conversation.md
        📁 test11/
            📄 code_*.py
            📄 conversation.md
        📁 test12/
            📄 code_*.py
            📄 conversation.md
    📁 tests/
        📄 test_ui_load.py
        📄 __init__.py
        📁 fenetre_kivy/
            📄 __init__.py
    📁 tools/
        📄 analyze_dev_logs.py
        📄 benchmark_responses.py
        📄 calc_fond_dims.py
        📄 init_conv_chatgpt.py
        📄 update_system_prompt.py
    📁 ui/
        📄 app_main.py
        📄 config_ui.py
        📄 layout_builder.py
        📄 __init__.py
        📁 behaviors/
            📄 hover_behavior.py
            📄 __init__.py
        📁 widgets/
            📄 buttons.py
        📁 zones/
            📄 zone_chat.py
            📄 zone_liste_conv.kv
            📄 zone_liste_conv.py
            📄 zone_message.kv
            📄 zone_message.py
            📄 __init__.py
```

---

## 🖥️ Commandes utiles Ollama (Windows / CMD)

* Lister les modèles installés :

```bash
ollama list
```

* Télécharger un modèle :

```bash
ollama pull mistral
ollama pull deepseek-coder:33b
```

* Supprimer un modèle :

```bash
ollama rm mistral
ollama rm deepseek-coder:33b
```

* Vérifier que le serveur Ollama tourne :

```bash
netstat -ano | findstr 11434
```

* Tester l’API Ollama :

```bash
curl http://127.0.0.1:11434/api/tags
```

* Démarrer manuellement le serveur (normalement inutile, Ollama tourne déjà en service) :

```bash
ollama serve
```

---

## 📊 Analyse des performances

Un script dédié (`tools/benchmark_responses.py`) permet :

* De choisir un modèle IA installé.
* De choisir un prompt personnalisé.
* De définir un nombre d’essais (par défaut 5).
* De mesurer le temps de réponse de l’IA pour chaque essai.
* De sauvegarder tous les résultats (bruts + résumé) dans `data/`.

Les résultats peuvent être analysés avec **Pandas** en important `data/dev_responses.jsonl`.
