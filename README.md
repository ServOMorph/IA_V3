# IA_V3 – Chat IA avec Ollama, gestion avancée des conversations et interface Kivy

## 📌 Description
Ce projet permet d’interagir avec un modèle IA local via **Ollama** (par défaut `mistral`), tout en gérant automatiquement :
- Sauvegarde des conversations dans un **dossier dédié par session** (`/sav/<nom_session>/conversation.md`)
- Sauvegarde automatique des blocs de code Python en `.py` dans le même dossier de session
- Chargement de sessions précédentes
- Renommage des sessions
- Suppression de sessions
- Déplacement de sessions dans des dossiers d’organisation
- Copie des derniers messages (IA ou utilisateur) dans le presse-papier
- Conservation du contexte à chaque échange
- Logs conversationnels séparés par session (`/logs/<nom_session>.log`)
- Démarrage propre avec vidage de `debug.log`
- **Interface graphique (UI) développée avec Kivy**, affichant un fond personnalisé

## 🚀 Nouveautés récentes
- **Commandes améliorées** :
  - `/suppr chemin/NOM` → Supprime la conversation et son log ; recrée automatiquement une session vide si c’était la session active.
  - `/new` → Démarre une nouvelle conversation vide.
  - `/copie_IA` → Copie la dernière réponse IA dans le presse-papier.
  - `/copie_user` → Copie le dernier message utilisateur dans le presse-papier.
  - `/createfolder NOM` → Crée un dossier d’organisation dans `/sav` et `/logs`.
  - `/move NOM_CONV DOSSIER` → Déplace une conversation vers un dossier existant (gestion des logs sur Windows incluse).
  - `/savecode [base]` → Extrait le code Python de la dernière réponse et le sauvegarde dans le dossier de session.
- **Sauvegarde par dossier** :
  - Chaque session possède son propre dossier contenant `conversation.md` et éventuellement des `.py`.
- **Démarrage amélioré** :
  - `debug.log` vidé au lancement avec horodatage.
- **Interface graphique Kivy** :
  - Fenêtre configurable en taille et position via `ui/config_ui.py`
  - Fond personnalisé depuis `assets/images/fond_window.png`
  - Nettoyage des logs Kivy en console
  - Structure séparée (`main_ui.py` pour le lancement)
  - Configuration centralisée (`ui/config_ui.py`)
  - Suppression des éléments par défaut pour un fond pur

## 📂 Structure du projet

IA_V3/
│
├── core/
│ ├── chat_manager.py
│ ├── ollama_client.py
│ ├── sav_manager.py
│ ├── commands.py
│ ├── startup_utils.py
│ └── logging/
│ ├── logger.py
│ └── conv_logger.py
├── ui/
│ ├── config_ui.py
│ └── zones/
│ ├── zone_message.py
│ └── zone_message.kv
├── tools/
│ └── update_system_prompt.py
├── assets/
│ └── images/
│ ├── fond_window.png
│ └── send_icon.png
├── logs/
├── sav/
├── synthèses_chatgpt/
├── config.py
├── main.py
├── main_ui.py
└── README.md


## 🖥️ Utilisation
### Interface en ligne de commande
```bash
python main.py

Interface graphique Kivy

python main_ui.py

Modifier le prompt système

python tools/update_system_prompt.py

    Coller ou saisir un texte multiligne, terminer par Ctrl+Z + Entrée (Windows) ou Ctrl+D (Linux/Mac).

    Le script met à jour DEFAULT_SYSTEM_PROMPT dans config.py.

📜 Commandes disponibles
Commande	Description
/q	Sauvegarder la conversation et quitter
/exit	Quitter sans sauvegarder
/help	Afficher la liste des commandes
/rename NOM	Renommer la session active
/msg1	Message pré-enregistré 1
/msg2	Message pré-enregistré 2
/load chemin/NOM	Charger une session
/suppr chemin/NOM	Supprimer une session et son log, recrée une session vide si active
/new	Créer une nouvelle session vide
/copie_IA	Copier la dernière réponse IA
/copie_user	Copier le dernier message utilisateur
/createfolder NOM	Créer un dossier d’organisation
/move NOM_CONV DOSSIER	Déplacer la session vers un dossier existant
/savecode [base]	Sauvegarder le code Python de la dernière réponse

🗂️ Répertoires

    Sessions sauvegardées : /sav/

    Logs conversationnels : /logs/

    Ressources graphiques : /assets/images/

    Scripts utilitaires : /tools/

    Synthèses de tests ChatGPT : /synthèses_chatgpt/

🎨 Évolutions UI récentes

    Nouvelle zone de message (ZoneMessage dans ui/zones/zone_message.py + zone_message.kv)

        Design type “pillule”

        Entrée → envoi message ; Shift+Entrée → saut de ligne

        Bouton envoyer rond avec icône

        Placeholder personnalisable

        Effacement automatique après envoi

    Personnalisation graphique

        Fond sombre, bords arrondis

        TextInput transparent avec padding interne

        Bouton envoyer couleur dynamique

        Icône send_icon.png