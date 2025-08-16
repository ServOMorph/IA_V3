# IA_V3 – Chat IA avec Ollama, gestion avancée des conversations et interface Kivy

## 📌 Description
Ce projet permet d’interagir avec un modèle IA local via **Ollama** (par défaut `mistral`), tout en gérant automatiquement :  
- Sauvegarde des conversations dans un **dossier dédié par session** (`/sav/<nom_session>/conversation.md`)  
- Sauvegarde automatique des blocs de code Python en `.py` dans le même dossier de session  
- Chargement, renommage, suppression et déplacement des sessions  
- Copie des derniers messages (IA ou utilisateur) dans le presse-papier  
- Conservation du contexte conversationnel  
- Logs séparés par session (`/logs/<nom_session>.log`)  
- Vidage automatique de `debug.log` au démarrage  
- **Interface graphique (UI) avec Kivy** : fond personnalisé, zones de chat et saisie modernes  

---

## 🚀 Nouveautés récentes

### 💬 Commandes
- `&suppr chemin/NOM` → Supprime la conversation et son log ; recrée automatiquement une session vide si active  
- `&new` → Nouvelle conversation vide  
- `&copie_IA` → Copie la dernière réponse IA dans le presse-papier  
- `&copie_user` → Copie le dernier message utilisateur  
- `&createfolder NOM` → Crée un dossier d’organisation dans `/sav` et `/logs`  
- `&move NOM_CONV DOSSIER` → Déplace une conversation vers un dossier existant  
- `&savecode [base]` → Extrait le dernier code Python et le sauvegarde dans la session  
- `&savetxt [base]` → Extrait le dernier texte en bloc `txt` et le sauvegarde dans la session  

### 🖼️ Interface graphique Kivy
- **ZoneMessage** (saisie utilisateur) :
  - Design en **pilule arrondie**  
  - Placeholder + curseur clignotant personnalisé  
  - Bouton envoyer rond (`send_icon.png`)  
  - Effacement automatique après envoi  
  - Masquage du bouton pendant la génération de la réponse IA  
- **ZoneChat** :
  - Messages affichés sous forme de **bulles** :
    - Utilisateur → bulle bleue à droite  
    - IA → bulle grise à gauche avec logo (`Logo_IA.png`)  
  - ScrollView qui reste calé en bas  
  - Largeur max des bulles (≈420px)  
  - Espacement vertical uniforme  
- **Indication de réflexion** :
  - Texte `"Je suis en train de réfléchir..."` affiché entre la question de l’utilisateur et la réponse IA  
  - Prévu avec animation (points clignotants)  

---

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
│
├── ui/
│ ├── config_ui.py
│ └── zones/
│ ├── zone_message.py
│ ├── zone_message.kv
│ └── zone_chat.py
│
├── tools/
│ └── update_system_prompt.py
│
├── assets/
│ └── images/
│ ├── fond_window.png
│ ├── send_icon.png
│ └── Logo_IA.png
│
├── logs/
├── sav/
├── synthèses_chatgpt/
│
├── config.py
├── main.py # version CLI
├── main_ui.py # version UI Kivy
└── README.md


---

## 🖥️ Utilisation

### Interface en ligne de commande
```bash
python main.py

Interface graphique (UI Kivy)

python main_ui.py

Modifier le prompt système

python tools/update_system_prompt.py

    Saisir ou coller un texte multiligne, terminer par Ctrl+Z + Entrée (Windows) ou Ctrl+D (Linux/Mac).
    Le script met à jour DEFAULT_SYSTEM_PROMPT dans config.py.

📜 Commandes disponibles
Commande	Description
&q	Sauvegarder la conversation et quitter
&exit	Quitter sans sauvegarder
&help	Afficher la liste des commandes
&rename NOM	Renommer la session active
&msg1, &msg2	Messages pré-enregistrés
&load chemin/NOM	Charger une session
&suppr chemin/NOM	Supprimer session + log, recrée une session vide si active
&new	Nouvelle session vide
&copie_IA	Copier la dernière réponse IA
&copie_user	Copier le dernier message utilisateur
&createfolder NOM	Créer un dossier d’organisation
&move NOM_CONV DOSSIER	Déplacer une session
&savecode [base]	Sauvegarder le dernier code Python
&savetxt [base]	Sauvegarder le dernier texte (bloc txt)
🗂️ Répertoires

    Sessions sauvegardées : /sav/

    Logs conversationnels : /logs/

    Ressources graphiques : /assets/images/

    Scripts utilitaires : /tools/

    Synthèses ChatGPT : /synthèses_chatgpt/

