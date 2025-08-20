# 📘 DeepSeek Tests – Configuration optimisée

Ce dossier contient une configuration **Ollama Modelfile** pour exécuter **DeepSeek Coder 6.7B** en version optimisée vitesse, adaptée aux benchmarks de code Python courts.

---

## 📂 Contenu

* `Modelfile` : configuration Ollama (sans extension).

---

## ⚙️ Construction du modèle

Depuis ce dossier :

```bash
ollama create deepseek-tests -f Modelfile
```

Cela crée un nouveau modèle local nommé **`deepseek-tests`**.

---

## ▶️ Utilisation

Lancer le modèle optimisé :

```bash
ollama run deepseek-tests
```

Ou exécuter directement un benchmark :

```bash
python tools/benchmark/benchmark_deepseek.py
```

*(modifier le script pour utiliser `deepseek-tests` comme modèle si besoin)*

---

## 🔧 Paramètres choisis

* `FROM deepseek-coder:6.7b` → modèle de base utilisé.
* `num_predict 200` → suffisant pour générer une fonction Python complète.
* `temperature 0.2` → sortie stable et déterministe.
* `top_k 50` et `top_p 0.9` → équilibre entre précision et diversité.
* `num_ctx 512` → contexte réduit, accélère la génération.
* `repeat_penalty 1.1` → évite les répétitions inutiles.

---

## 📈 Objectif

Réduire le temps de réponse lors des benchmarks automatisés tout en conservant un code correct et testable.
