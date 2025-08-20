# 📡 Documentation API — agents\_ia\_project

## 🎯 Objectif

Fournir une **API centralisée avec FastAPI** pour coordonner les agents IA (GestIA, DonIA, ArtIA, BackIA, etc.).
`main.py` est le **point d’entrée du backend API**.

---

## 🚀 Lancement

1. Installer les dépendances :

   ```bash
   pip install -r requirements.txt
   ```
2. Lancer le serveur API :

   ```bash
   uvicorn main:app --reload
   ```
3. Vérifier l’endpoint de test :

   ```bash
   curl http://127.0.0.1:8000/ping
   ```

   Résultat attendu :

   ```json
   {"status": "ok"}
   ```

---

## 📌 Structure actuelle

* **`main.py`** : serveur FastAPI, route `/ping`.
* **`docs/api_initialisation.md`** : détail de la mise en place initiale.

---

## 📡 Conventions d’appel prévues

* Chaque futur endpoint suivra un schéma REST clair (GET, POST, etc.).
* Les routes seront documentées dans `docs/api_initialisation.md`.
* Les tests unitaires seront centralisés dans `tests/test_api.py`.

---

## ✅ Statut actuel

* API initialisée avec route `/ping`.
* Étapes à venir : ajout des endpoints `/agents` et `/task`, intégration d’Ollama, gestion complète des agents.
