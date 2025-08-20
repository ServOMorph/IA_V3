# 📊 Module Benchmark IA

Ce module permet d'exécuter des benchmarks sur différents modèles IA (via Ollama) afin de mesurer :

* le **temps de réponse moyen**,
* la **qualité du code généré** (via des exercices et des tests unitaires automatiques),
* la **complétude fonctionnelle** (par ex. boucles de jeu, inventaire, système de combat pour l'exercice RPG).

## 📂 Structure du dossier

```
tools/benchmark/
 ├── __init__.py
 ├── cli.py                 # Interface CLI principale (point d'entrée)
 ├── runner.py              # Logique de benchmark (exécution des tests)
 ├── exercises.py           # Définition des exercices (prompt + tests attendus)
 ├── code_utils.py          # Extraction et évaluation du code généré
 ├── storage.py             # Sauvegarde du code et des résultats
 ├── config_benchmark.py    # Configuration spécifique au benchmark
 ├── benchmark_mistral.py   # Script dédié Mistral (mistral:latest)
 ├── benchmark_deepseek.py  # Script dédié DeepSeek (deepseek-tests)
```

Un alias pratique est disponible à la racine :

```
main_benchmark.py  # Point d'entrée depuis la racine du projet
```

## 🚀 Utilisation

### Lancer le benchmark interactif

Depuis la racine du projet :

```bash
python main_benchmark.py
```

ou :

```bash
python -m tools.benchmark
```

### Lancer un benchmark direct (scripts dédiés)

* **Mistral standard** :

```bash
python tools/benchmark/benchmark_mistral.py
```

* **Mistral optimisé (mistral-tests)** :

```bash
python tools/benchmark/benchmark_mistral2.py
```

* **DeepSeek optimisé (deepseek-tests)** :

```bash
python tools/benchmark/benchmark_deepseek.py
```

### Étapes interactives

1. **Sélection de l'exercice** (par ex. `is_prime`, `fibonacci`, `factorial`, `long_code_test`).
2. **Mode test à blanc** : permet de vérifier le prompt et les chemins de sauvegarde sans exécuter.
3. **Sélection du mode de test** :

   * `o` → exécute sur **tous les modèles installés**,
   * `n` → permet de choisir un modèle spécifique.
4. **Nombre de runs** : nombre d’essais pour calculer les moyennes.

### Résultats produits

* **Code généré** : sauvegardé dans

  ```
  data/generated/<model>/<exercise>/solution_<model>_<exercise>_runX_<timestamp>.py
  ```
* **Logs texte** : `data/dev_responses.log`
* **Logs JSONL** : `data/dev_responses.jsonl` (facilement exploitable pour analyse).
* **Rapport PDF** (optionnel) : synthèse graphique et qualitative des performances.

## ⚙️ Exercices disponibles

Définis dans `exercises.py` :

* `is_prime(n: int) -> bool`
* `fibonacci(n: int) -> int`
* `factorial(n: int) -> int`
* `long_code_test` → programme plus complexe (\~200 lignes, ex. RPG console)

Chaque exercice contient :

* un **prompt** donné au modèle,
* une **suite de tests** validant la fonction générée.

## 📈 Analyse des résultats

Un script d’analyse peut agréger les résultats JSONL :

```bash
python tools/analyze_results.py
```

Il affiche un tableau récapitulatif (temps moyen, score moyen, taux de complétion) par modèle et par exercice.

Les codes longs (RPG) peuvent être évalués aussi sur :

* **complétude fonctionnelle** (combat, inventaire, boucle de jeu),
* **robustesse du code** (absence de bugs bloquants),
* **taille effective** (proche de la cible demandée).

## ✅ Exemple de session (CLI standard)

```
=== Sélection de l'exercice ===
1. is_prime
2. fibonacci
3. factorial
4. long_code_test
Sélectionnez un exercice (1-4) [1] : 4
```

## 📚 Documentation associée

* `docs/prompt_engineering_mistral7b.md` → bonnes pratiques de prompt pour Mistral.
* `docs/prompt_engineering_deepseek.md` → bonnes pratiques de prompt pour DeepSeek.
* `docs/comparatif_mistral_vs_deepseek.md` → comparatif de performance.
* `docs/ollama_models_readme.md` → explication des paramètres Ollama.
* `docs/analyse_rpg_benchmark.pdf` → exemple de rapport d’analyse avec graphiques.

## 🔮 Améliorations prévues

* Extraction plus robuste du code généré (ignorer les phrases hors bloc de code).
* Ajout de nouveaux exercices (par ex. `palindrome`, `tri rapide`, `simulateur`).
* Export automatique des résultats en CSV/Excel et PDF.
* Dashboard de visualisation (Grafana/Streamlit).
* Intégration d'une évaluation qualitative (complétude fonctionnelle, jouabilité).
