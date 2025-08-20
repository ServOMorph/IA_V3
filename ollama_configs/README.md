# 📘 Dossier `ollama_configs`

Ce dossier contient les **configurations personnalisées (Modelfile)** pour créer des variantes optimisées des modèles via **Ollama**.

---

## 📂 Structure

```
ollama_configs/
 ├── mistral_tests/
 │    ├── Modelfile   # Config optimisée pour Mistral
 │    └── README.md   # Explications et usage
 ├── deepseek_tests/
 │    ├── Modelfile   # Config optimisée pour DeepSeek
 │    └── README.md   # Explications et usage
```

---

## ▶️ Utilisation

### Créer un modèle optimisé

Depuis le dossier correspondant :

```bash
ollama create <nom-modele> -f Modelfile
```

Exemples :

```bash
cd ollama_configs/mistral_tests
ollama create mistral-tests -f Modelfile

cd ollama_configs/deepseek_tests
ollama create deepseek-tests -f Modelfile
```

### Vérifier l’installation

```bash
ollama list
```

Exemple de sortie :

```
mistral:latest
mistral-tests
deepseek-coder:6.7b
deepseek-tests
```

### Lancer un modèle optimisé

```bash
ollama run mistral-tests
ollama run deepseek-tests
```

---

## 🔧 Paramètres courants dans les Modelfile

* `num_predict` → limite le nombre de tokens générés (200 pour fonctions Python).
* `temperature` → contrôle la variabilité (0.2 pour code stable).
* `top_k` et `top_p` → contrôlent l’échantillonnage (valeurs équilibrées : 50 / 0.9).
* `num_ctx` → taille du contexte (512 tokens pour plus de vitesse).
* `repeat_penalty` → évite les répétitions (1.1 recommandé).

---

## 🎯 Objectif

Créer des variantes optimisées des modèles pour réduire la **latence** et améliorer la **stabilité** dans les benchmarks de code.
