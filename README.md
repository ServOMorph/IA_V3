# IA_V3 – Chat IA avec Ollama, gestion avancée des conversations et interface avec API

## 📌 Description

Projet backend + UI pour interagir avec un modèle IA local via **Ollama**, avec gestion avancée des conversations.

### Fonctionnalités principales :

* Dialogue avec un modèle IA local.
* Sauvegarde des conversations dans un **dossier par session** (`/sav/<nom_session>/conversation.md`).
* **Export manuel des fichiers** via la commande `&export <nom> <ext>` (formats supportés : `.py`, `.txt`, `.md`, `.json`, `.csv`, `.docx`, `.pdf`, `.xlsx`).
  * Support du parsing : si la réponse IA contient des blocs de code/texte (`python`, `txt`, etc.), ils sont extraits et exportés séparément (`nom_1.ext`, `nom_2.ext`).
  * Si aucun bloc n'est détecté, l’intégralité du message IA est exportée.
* Commande **`&getfile <nom>`** pour relire directement un fichier généré dans la session.
* Chargement, renommage, suppression et organisation des sessions (via CLI, UI et API).
  * ⚠️ Particularité API : le renommage d’une session (`PUT /sessions/{name}/rename`) réussit même si le fichier `.log` est verrouillé par un logger. Dans ce cas, seul le dossier est renommé et un avertissement est affiché côté serveur.
* Copie rapide des derniers messages dans le presse-papier (CLI).
* Conservation du contexte conversationnel avec possibilité de tronquer l'historique pour accélérer les réponses.
* **Système de résumé avancé** :
  * Résumé **glissant** par tranches de messages.
  * Résumés **partiels numérotés** conservés dans `summary.md`.
  * Résumés **globaux périodiques** consolidant les partiels.
  * Format structuré en 4 sections : Faits clés, Intentions utilisateur, Réponses IA, Points en suspens.
* Logs techniques et conversationnels séparés (`/logs/<nom_session>.log`).
* **Interface Kivy moderne** avec zones distinctes : liste de conversations, chat, saisie, panneau info/config.
* Couleurs centralisées dans `ui/config_ui.py`.
* **Mode DEV** :
  * Liste les modèles Ollama installés au démarrage.
  * Permet de choisir le modèle IA à utiliser.
  * Affiche et logge le temps de réponse pour chaque prompt.
  * Sauvegarde des résultats (code généré + stats) dans `data/generated/` et `data/dev_responses.*`.
  * Documentation associée dans `docs/` (prompt engineering et comparatifs).

## 🖥️ Commandes utiles Ollama (Windows / CMD)

* Lister les modèles installés :

```bash
ollama list
```

* Télécharger un modèle :

```bash
ollama pull mistral:7b
```

* Supprimer un modèle :

```bash
ollama rm mistral:7b
```

* Vérifier que le serveur Ollama tourne :

```bash
curl http://127.0.0.1:11434/api/tags
```

* Démarrer manuellement le serveur :

```bash
ollama serve
```

## ⚡ Conseils d’optimisation des performances

* **Quantisation** : utiliser les variantes Q4/Q5 (`-q4_K_M`) pour réduire la VRAM et accélérer l’inférence. Exemple : `gemma2-2b-it-q4`.
* **Limite de génération** : définir `MAX_TOKENS` dans `config.py` (ex. 100, 200, 400) pour contrôler la longueur des réponses et réduire la latence.
* **Troncature de l’historique** : limiter le nombre d’échanges conservés dans la mémoire du client pour éviter un contexte trop long.
* **Context length** : rester à 4k ou 8k tokens pour garder l’exécution GPU. Au-delà, bascule CPU → ralentissements.
* **Choix des modèles adaptés à la RTX 4060 (8 Go VRAM)** :
  * Général : `gemma2:2b`, `gemma2-2b-it-q4`, `mistral:7b`, `llama3.1:8b-q4`, `phi4-mini:3.8b`
  * Code : `deepseek-coder:6.7b`, `qwen2.5-coder:7b`
  * Multimodal : `llava:7b`
  * Raisonnement : `starling-lm:7b`, `phi4:latest`
* **Batch size** : réduire si la VRAM est saturée.
* **Threads CPU** : utiliser 16 threads sur Ryzen 7 5700X pour compenser en mode CPU fallback.
* **Préchargement** : lancer `ollama serve` pour éviter les temps de rechargement du modèle à chaque requête.

---

## 🔮 Améliorations prévues

* Nouveaux benchmarks pour Phi-4, Starling-LM et LLaVA.
* Automatisation des tests multimodaux (texte + image).
* Export automatique en CSV/Excel.
* Dashboard de visualisation (Grafana/Streamlit).
* Optimisation GPU/paramètres supplémentaires pour les modèles lourds.
* Intégration d’un gestionnaire de profils (configurations par modèle).
* Ajout d’un export JSON structuré des résumés (pour mémoire sélective et réinjection ciblée).
* Commandes utilisateur pour contrôler les résumés (`/resumeshow`, `/resumerefresh`, `/resumeclear`).
* **Gestion avancée des fichiers** : possibilité de partager des fichiers avec l’IA et de les exporter manuellement avec `&export` dans plusieurs formats (`.py`, `.txt`, `.md`, `.json`, `.csv`, `.docx`, `.pdf`, `.xlsx`).
