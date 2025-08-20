# 📄 Document de développement et de suivi complet — agents_ia_project

## 📝 Introduction
Le projet **agents_ia_project** vise à mettre en place un **programme Python** permettant la **communication coordonnée entre différents agents IA**.  
L’objectif final est une architecture claire où chaque agent (GestIA, DonIA, ArtIA, BackIA, etc.) peut être sollicité via une API centralisée, avec gestion mémoire, suivi et documentation.  

Tous les livrables incluent systématiquement :  
- l’arborescence complète mise à jour (`arborescence.txt`),  
- le README de la partie concernée (`docs/README_<partie>.md`).  

---

## 🚀 Étapes de développement numérotées

### 1. Mise en place de l’API FastAPI
**Agents responsables : GestIA, BackIA, DevIA - Python**

1.1 **BackIA → Création structure API**  
- Créer `main.py` avec FastAPI de base.  
- Ajouter route `/ping` de test.  
- **Livrables** :  
  - `main.py`  
  - `docs/api_initialisation.md` (section 1 : structure API)  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_api.md`  

1.2 **DevIA - Python → Endpoints initiaux**  
- Ajouter endpoint `/agents` (liste des agents).  
- Ajouter endpoint `/task` (exécution tâche simple).  
- **Livrables** :  
  - `main.py` (mis à jour)  
  - `docs/api_initialisation.md` (section 2 : endpoints)  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_api.md` (mis à jour)  

1.3 **GestIA → Vérification et orchestration**  
- Vérifier cohérence avec l’architecture globale.  
- Documenter conventions d’appel.  
- **Livrables** :  
  - `docs/api_initialisation.md` (section 3 : conventions d’appel)  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_api.md` (finalisé)  

---

### 2. Intégration d’Ollama en local
**Agents responsables : GestIA, DonIA, ServIA**

2.1 **ServIA → Développement module Ollama**  
- Créer `ollama_client.py` avec fonctions `run_model()` et `list_models()`.  
- **Livrables** :  
  - `ollama_client.py`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_ollama.md`  

2.2 **DonIA → Configuration mémoire Ollama**  
- Créer `data/ollama_config.json` (modèles, paramètres).  
- **Livrables** :  
  - `data/ollama_config.json`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_ollama.md` (mis à jour)  

2.3 **GestIA → Documentation intégration**  
- Vérifier appels depuis FastAPI.  
- Décrire procédure d’utilisation.  
- **Livrables** :  
  - `docs/ollama_integration.md`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_ollama.md` (finalisé)  

---

### 3. Création de l’interface utilisateur (Frontend)
**Agents responsables : ArtIA, DevIA - Html**

3.1 **ArtIA → Conception UI/UX**  
- Produire wireframe et style guide.  
- **Livrables** :  
  - `docs/ui_wireframe.png`  
  - `docs/ui_design.md` (section 1 : design et maquettes)  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_frontend.md`  

3.2 **DevIA - Html → Structure HTML**  
- Créer `templates/layout.html` (structure globale).  
- Créer `templates/index.html` (page principale).  
- **Livrables** :  
  - `templates/layout.html`  
  - `templates/index.html`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_frontend.md` (mis à jour)  

3.3 **ArtIA → Création CSS**  
- Développer `static/css/style.css`.  
- Définir règles typographiques, couleurs, feedback.  
- **Livrables** :  
  - `static/css/style.css`  
  - `docs/ui_design.md` (section 2 : règles CSS)  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_frontend.md` (mis à jour)  

3.4 **DevIA - Html → Développement JS**  
- Créer `static/js/app.js` : gestion inputs, appels API, affichage résultats.  
- Gérer erreurs de connexion.  
- **Livrables** :  
  - `static/js/app.js`  
  - `docs/ui_design.md` (section 3 : logique front-end)  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_frontend.md` (mis à jour)  

3.5 **ArtIA → Validation UI**  
- Vérifier cohérence visuelle, ajouter icônes/logo.  
- **Livrables** :  
  - `static/img/logo.png`  
  - `docs/ui_design.md` (section finale : aperçu complet)  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_frontend.md` (finalisé)  

---

### 4. Implémentation des agents principaux
**Agents responsables : GestIA, DonIA, ArtIA, BackIA, DevIA - Python, RefactoIA, DebugIA, ServIA**

4.1 **GestIA → Orchestration**  
- Implémenter `agents/gestia.py`.  
- **Livrables** :  
  - `agents/gestia.py`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_agents.md`  

4.2 **DonIA → Mémoire**  
- Implémenter `agents/donia.py` et `data/memory.json`.  
- **Livrables** :  
  - `agents/donia.py`  
  - `data/memory.json`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_agents.md` (mis à jour)  

4.3 **ArtIA → Génération créative**  
- Implémenter `agents/artia.py`.  
- **Livrables** :  
  - `agents/artia.py`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_agents.md` (mis à jour)  

4.4 **BackIA + DevIA - Python → Backend utilitaire**  
- Créer `agents/common_utils.py` pour factoriser appels.  
- **Livrables** :  
  - `agents/common_utils.py`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_agents.md` (mis à jour)  

4.5 **RefactoIA → Amélioration continue**  
- Vérifier organisation des modules.  
- Factoriser si redondance.  
- **Livrables** :  
  - `docs/refactor_report.md`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_agents.md` (mis à jour)  

4.6 **DebugIA → Débogage initial**  
- Corriger erreurs d’intégration.  
- **Livrables** :  
  - `docs/debug_report.md`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_agents.md` (mis à jour)  

4.7 **ServIA → Services externes**  
- Préparer intégrations si API tierces nécessaires.  
- **Livrables** :  
  - `agents/servia.py`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_agents.md` (mis à jour)  

---

### 5. Tests et suivi qualité
**Agents responsables : DebugIA, RefactoIA, GestIA**

5.1 **DebugIA → Écriture des tests**  
- Créer `tests/test_api.py` et `tests/test_agents.py`.  
- **Livrables** :  
  - `tests/test_api.py`  
  - `tests/test_agents.py`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_tests.md`  

5.2 **RefactoIA → Analyse qualité**  
- Vérifier couverture et proposer améliorations.  
- **Livrables** :  
  - `docs/test_report.md`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_tests.md` (mis à jour)  

5.3 **GestIA → Validation finale**  
- Centraliser résultats.  
- **Livrables** :  
  - `docs/test_report.md` (finalisé)  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_tests.md` (finalisé)  

---

### 6. Pédagogie et documentation
**Agents responsables : PédagoIA, ServOMorphIA**

6.1 **PédagoIA → Guide utilisateur**  
- Vulgariser le fonctionnement.  
- **Livrables** :  
  - `docs/guide_utilisateur.md`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_docs.md`  

6.2 **ServOMorphIA → Guide technique**  
- Centraliser process technique.  
- **Livrables** :  
  - `docs/dev_guide.md`  
  - `arborescence.txt` (mise à jour)  
  - `docs/README_docs.md` (finalisé)  

---

## 📊 Suivi d’avancement
| Étape | Description | Agent(s) | Livrables | Statut |
|-------|-------------|----------|-----------|--------|
| 1 | API FastAPI opérationnelle | GestIA, BackIA, DevIA - Python | `main.py`, `docs/api_initialisation.md`, `docs/README_api.md`, `arborescence.txt` | [ ] |
| 2 | Ollama intégré | GestIA, DonIA, ServIA | `ollama_client.py`, `data/ollama_config.json`, `docs/ollama_integration.md`, `docs/README_ollama.md`, `arborescence.txt` | [ ] |
| 3 | UI fonctionnelle | ArtIA, DevIA - Html | `templates/`, `static/`, `docs/ui_design.md`, `docs/README_frontend.md`, `arborescence.txt` | [ ] |
| 4 | Agents principaux implémentés | GestIA, DonIA, ArtIA, BackIA, DevIA - Python, RefactoIA, DebugIA, ServIA | `agents/*.py`, `data/memory.json`, `docs/README_agents.md`, `arborescence.txt` | [ ] |
| 5 | Tests validés | DebugIA, RefactoIA, GestIA | `tests/*.py`, `docs/test_report.md`, `docs/README_tests.md`, `arborescence.txt` | [ ] |
| 6 | Documentation pédagogique | PédagoIA, ServOMorphIA | `docs/guide_utilisateur.md`, `docs/dev_guide.md`, `docs/README_docs.md`, `arborescence.txt` | [ ] |
