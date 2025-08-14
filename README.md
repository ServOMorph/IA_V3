# IA_V3 – Chat IA avec Ollama, gestion avancée des conversations et interface Kivy

## 📌 Description
Ce projet permet d’interagir avec un modèle IA local via **Ollama** (par défaut `mistral`), tout en gérant automatiquement :
- La sauvegarde des conversations (`/sav`)
- Le chargement de sessions précédentes
- Le renommage des conversations
- La suppression de conversations
- La copie des derniers messages (IA ou utilisateur) dans le presse-papier
- La conservation du contexte à chaque échange
- Des logs détaillés dans des fichiers séparés
- Un démarrage propre avec vidage de `debug.log`
- **Une interface graphique (UI) développée avec Kivy**, affichant un fond personnalisé

## 🚀 Nouveautés
- **Commandes ajoutées** :
  - `/suppr NOM` → Supprime la conversation et son log.
  - `/new` → Démarre une nouvelle conversation vide.
  - `/copie_IA` → Copie la dernière réponse IA dans le presse-papier.
  - `/copie_user` → Copie le dernier message utilisateur dans le presse-papier.
  - `/createfolder NOM` → Crée un dossier dans /sav et /logs pour organiser les conversations.
  - `/move NOM_CIBLE DOSSIER` → Déplace une conversation vers un dossier existant.
- **Démarrage amélioré** :
  - `debug.log` vidé au lancement, avec trace interne de la date/heure.
- **Interface graphique Kivy** :
  - Fenêtre configurable en taille et position via `ui/config_ui.py`
  - Fond personnalisé depuis `assets/images/fond_window.png` (chemin absolu pour éviter les erreurs)
  - Nettoyage des logs Kivy dans la console
  - Structure du code séparée (`main_ui.py` pour le lancement, `ui/interface_main.py` pour l’interface)
  - Configuration centralisée (`ui/config_ui.py`)
  - Suppression du label et du bouton par défaut pour un fond pur

## 📂 Structure du projet
```
IA_V3/
│
├── core/
│   ├── chat_manager.py
│   ├── ollama_client.py
│   ├── sav_manager.py
│   ├── commands.py
│   ├── startup_utils.py
│   └── logging/
│       ├── logger.py
│       └── conv_logger.py
├── ui/
│   └── config_ui.py         # constantes et paramètres UI
├── assets/
│   └── images/
│       └── fond_window.png  # image de fond
├── logs/
├── sav/
├── config.py
├── main.py
├── main_ui.py               # classe MainUI (interface Kivy)
└── README.md
```

## 🖥️ Utilisation
### Interface en ligne de commande
```bash
python main.py
```
### Interface graphique Kivy
```bash
python main_ui.py
```

📜 **Commandes disponibles**  
| Commande       | Description |
|----------------|-------------|
| /q             | Sauvegarder la conversation et quitter |
| /exit          | Quitter sans sauvegarder |
| /help          | Afficher la liste des commandes |
| /rename NOM    | Renommer la conversation actuelle |
| /msg1          | Demande pré-enregistrée 1 |
| /msg2          | Demande pré-enregistrée 2 |
| /load NOM      | Charger une conversation sauvegardée |
| /suppr NOM     | Supprimer une conversation et son log |
| /new           | Créer une nouvelle conversation vide |
| /copie_IA      | Copier la dernière réponse IA |
| /copie_user    | Copier le dernier message utilisateur |
| /createfolder NOM | Crée un dossier dans /sav et /logs |
| /move NOM DOSSIER | Déplace la conversation NOM dans le dossier existant |

🗂️ **Répertoires**
- Conversations sauvegardées : `/sav/`
- Logs techniques : `debug.log`
- Logs conversationnels : `/logs/`
- Ressources graphiques : `/assets/images/`
