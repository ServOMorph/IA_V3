# 📖 UI\_HTML – Prototype interface Web

## 📌 Description

Prototype en **HTML / CSS / JavaScript** de l’interface utilisateur du projet `IA_V3`.

Ce module est indépendant de l’UI Kivy et permet de tester une interface web moderne connectée à l’API FastAPI.

---

## 📂 Structure du dossier

```
ui_html/
├── index.html              # Structure principale de la page
├── css/
│   ├── config_ui_html.css  # Variables (couleurs, polices, arrondis…)
│   └── styles.css          # Styles globaux (layout, chat, boutons, animations…)
├── js/
│   └── script.js           # Logique d’affichage, connexion API, sauvegarde auto
└── assets/
    └── images/             # Logos et icônes utilisés (logo_vertia.png, logo_vertia_seul.png, logo_user.png, plus_icon.png)
```

---

## 🎨 Fonctionnalités UI

* **Sidebar** avec logo VertIA, bouton `plus_icon.png` pour créer une nouvelle conversation, et liste de conversations dynamiques (via API `/sessions`).
* **Zone de chat** avec historique des messages (via API `/sessions/{name}/history`).
* **Différenciation des messages** :

  * Utilisateur : bulle alignée à droite avec `logo_user.png`.
  * IA (bot) : bulle alignée à gauche avec `logo_vertia_seul.png`.
* **Zone de saisie** :

  * `textarea` extensible jusqu’à `--max-lines` lignes.
  * **Entrée** = envoi, **Shift+Entrée** = retour ligne.
  * Bouton Envoyer en forme de **rectangle arrondi** avec icône SVG.
* **Animations** : apparition des messages (slide gauche/droite + fade-in).
* **État d’écriture IA** : bulle `...` clignotante remplacée par la vraie réponse.
* **Défilement fluide** à l’ajout d’un message.
* **Sauvegarde automatique** : chaque message (utilisateur et IA) est transmis à l’API (`/sessions/{name}/message`) et écrit en temps réel dans `conversation.md`.
* **Bulles flexibles** : les bulles utilisateur et IA peuvent occuper toute la largeur de la zone de chat si nécessaire.

---

## 🛠️ Utilisation

1. Lancer l’API :

   ```bash
   uvicorn api.main_api:app --reload --port 8000
   ```
2. Lancer le serveur web :

   ```bash
   cd ui_html
   python -m http.server 8080
   ```
3. Accéder à [http://localhost:8080/index.html](http://localhost:8080/index.html).

---

## 🎨 Thème

* Palette basée sur le **vert foncé → vert clair** (dégradé vertical dans la sidebar).
* Couleurs, arrondis et tailles configurables dans `config_ui_html.css`.
* Exemple :

  ```css
  :root {
    --color-bg: #0d1f1a;
    --color-panel: #123227;
    --color-text: #e0f2e9;
    --color-accent: #27c48f;
    --radius: 12px;
    --max-lines: 6;
  }
  ```

---

## 🚧 Limitations

* Pas encore de mode clair/sombre.
* Pas encore de responsive avancé (mobile / tablette).
* Gestion des fichiers exportés non intégrée côté UI.

---

## 🔮 Évolutions possibles

* Ajout d’un **mode clair**.
* Options utilisateur (choix du modèle, réglages tokens/température).
* Gestion avancée des fichiers (upload/download via API `/files`).
* Amélioration responsive (mobile / tablette).
* Streaming des réponses IA caractère par caractère.
