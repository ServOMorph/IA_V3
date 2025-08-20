# 📁 agents\_ia\_project

## 🎯 Rôle du projet

Ce projet met en place un **système d’agents IA coordonnés** reposant sur **Ollama en local** et une **API FastAPI** centralisée.
L’agent **GestIA** joue le rôle de **chef de projet et orchestrateur** :

* Il reçoit les requêtes, distribue les tâches aux autres agents et centralise les réponses.
* Il est le **seul responsable** de la mise à jour des fichiers globaux du projet (arborescence, README, documents de suivi).

Chaque agent secondaire (BackIA, DonIA, ArtIA, etc.) produit ses livrables dans un **fichier unique Markdown autoportant** stocké dans `/responses/`.
GestIA extrait ensuite les informations et met à jour les fichiers concernés.

---

## 📂 Contenu du projet

* **`main.py`** → point d’entrée FastAPI.
* **`agents/`** → contient tous les agents IA spécialisés (GestIA, DonIA, ArtIA, BackIA, etc.).
* **`templates/`** → interface web utilisateur (HTML).
* **`static/`** → ressources statiques (CSS, JS).
* **`requirements.txt`** → dépendances Python.
* **`docs/`** → documentation (suivi, conventions, modèles, READMEs spécifiques).
* **`prompts/`** → prompts envoyés aux agents.
* **`responses/`** → réponses autoportantes des agents.

---

## 📡 Protocole de communication

À chaque fois qu’un agent est sollicité, il reçoit systématiquement :

1. **L’arborescence actuelle du projet.**
2. **Le README global du projet (ce fichier).**
3. **Le README de la partie concernée** (ex. API, frontend, Ollama, agents, tests, docs).
4. **La liste des fichiers nécessaires** pour accomplir sa mission.
5. **La description précise du livrable attendu.**

⚠️ Chaque réponse d’agent doit être fournie sous forme d’un **fichier Markdown unique et autoportant**, incluant :

* Résumé du README global (même si inchangé).
* Code produit.
* Documentation spécifique.
* Arborescence mise à jour.
* Liste des fichiers créés/modifiés.

---

## ✅ Statut

* [x] Structure initiale définie
* [x] API initiale (route `/ping`) créée
* [ ] Intégration d’Ollama
* [ ] Interface frontend
* [ ] Implémentation des agents principaux
* [ ] Tests et suivi qualité
* [ ] Documentation pédagogique

---

📌 Ce projet est la **fondation d’un écosystème d’agents IA collaboratifs** orchestrés par GestIA.
