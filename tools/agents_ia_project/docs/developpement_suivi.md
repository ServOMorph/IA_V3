# 📄 Document de développement et de suivi — agents_ia_project

## 📝 Introduction
Le projet **agents_ia_project** a pour but de créer un **écosystème d’agents IA coordonnés**, fonctionnant en local via **Ollama** et pilotés par une API **FastAPI**.  
L’agent central **GestIA** agit comme chef de projet virtuel : il reçoit les requêtes, distribue les tâches aux sous-agents (Chef_Agents_IA, DonIA, ArtIA, etc.) et centralise les réponses.  
Objectifs principaux :  
- Mettre en place une infrastructure robuste et modulaire.  
- Développer des agents spécialisés et interopérables.  
- Assurer la cohérence et le suivi continu du développement.  

## 📂 Organisation du projet
- **Backend (FastAPI)**  
  - Fichier principal : `main.py`  
  - Gestion des endpoints et de la communication avec le frontend.  
  - Intégration des modules agents et du client Ollama.  

- **Frontend (HTML/CSS/JS)**  
  - Dossier `templates/` : pages HTML pour l’interface utilisateur.  
  - Dossier `static/` : ressources CSS et scripts JS.  
  - Communication avec l’API via requêtes HTTP.  

- **Agents (dossier `agents/`)**  
  - **gestia.py** : cœur du système, gestion et orchestration.  
  - Agents spécialisés à développer :  
    - **Chef_Agents_IA** : superviseur des sous-agents.  
    - **DonIA** : gestion mémoire et stockage des données.  
    - **ArtIA** : génération de contenu créatif.  
    - **Autres** : ajoutés selon besoins spécifiques.  

- **Documentation (dossier `docs/`)**  
  - Référentiels, modèles et suivis de projet.  

- **Prompts (dossier `prompts/`)**  
  - Historique et suivi des interactions.  

## 🚀 Plan de développement
1. Mise en place de l’API FastAPI.  
2. Intégration d’Ollama en local.  
3. Création de l’UI (HTML/CSS/JS).  
4. Implémentation des agents principaux.  
5. Tests et suivi qualité.  

## 👥 Tâches par agent
- **GestIA** : gestion de projet, coordination des agents, supervision.  
- **Chef_Agents_IA** : organisation et orchestration des sous-agents.  
- **DonIA** : gestion mémoire et stockage des données.  
- **ArtIA** : génération de contenu créatif.  
- **Autres agents** : spécialisés selon contexte (analyse, génération technique, etc.).  

## 📊 Suivi d’avancement
| Étape | Description | Statut |
|-------|-------------|--------|
| 1 | API FastAPI opérationnelle | [ ] |
| 2 | Ollama intégré | [ ] |
| 3 | UI fonctionnelle | [ ] |
| 4 | Agents principaux implémentés | [ ] |
| 5 | Tests validés | [ ] |

## 📡 Protocole de communication
Chaque agent reçoit systématiquement :  
1. L’arborescence actuelle du projet.  
2. Le README global.  
3. Le README de la session ou dossier concerné.  
4. La liste des fichiers pertinents pour sa tâche.  
5. La description précise du livrable attendu.  

Ce protocole garantit un contexte complet et cohérent pour chaque action.  

## 📌 Prochaines étapes
- [ ] Définir les priorités du sprint actuel.  
- [ ] Assigner les premières tâches aux agents.  
- [ ] Mettre en place le suivi régulier.  
