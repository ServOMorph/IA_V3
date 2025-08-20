# ⚙️ Guide des paramètres Ollama – Optimisation des modèles

Ce document explique les principaux paramètres configurables pour les modèles dans **Ollama**, utiles pour ajuster la **vitesse**, la **qualité** et la **cohérence** des générations.

---

## 1. Paramètres principaux

### `num_predict`

* **Définition** : nombre maximal de tokens que le modèle peut générer.
* **Impact** : plus la valeur est grande, plus la génération peut être longue.
* **Recommandation** : pour les tests courts (fonctions Python), 200 tokens suffisent largement.

### `temperature`

* **Définition** : contrôle l’aléatoire dans la génération (0 = déterministe, >1 = créatif).
* **Impact** : n’influence pas directement la vitesse, mais une valeur basse produit des réponses plus stables et rapides à parser.
* **Recommandation** : 0.1–0.3 pour benchmark de code.

### `top_k`

* **Définition** : limite le choix aux *k* tokens les plus probables.
* **Impact** : plus petit → réponses plus déterministes, parfois plus rapides.
* **Recommandation** : 40–50 pour le code.

### `top_p`

* **Définition** : probabilité cumulée (nucleus sampling). Le modèle ne choisit que parmi les tokens qui couvrent `p` % de la probabilité totale.
* **Impact** : plus bas → sorties plus stables, mais parfois moins variées.
* **Recommandation** : 0.8–0.9.

### `num_ctx`

* **Définition** : taille maximale du contexte (tokens mémoire du modèle).
* **Impact** : grand contexte = plus lent et consomme plus de RAM. Pour des prompts simples, valeur élevée est inutile.
* **Recommandation** : 512–1024 tokens pour nos tests de fonctions.

---

## 2. Paramètres avancés

### `repeat_penalty`

* **Définition** : pénalise la répétition de tokens.
* **Impact** : utile pour éviter que le modèle boucle ou répète du code.
* **Recommandation** : 1.1–1.2.

### `stop`

* **Définition** : séquences qui arrêtent la génération.
* **Exemple** : `stop=["```"]` pour couper après un bloc de code.

### `quantization`

* **Définition** : version compressée du modèle (`q4`, `q5`, `q8`).
* **Impact** : réduit la taille mémoire et accélère la génération, parfois au prix d’une légère perte de précision.
* **Recommandation** : `q4_K_M` pour vitesse + efficacité mémoire.

---

## 3. Exemple de configuration (Modelfile)

```Dockerfile
FROM mistral:7b-instruct-q4_K_M

PARAMETER num_predict 200
PARAMETER temperature 0.2
PARAMETER top_k 50
PARAMETER top_p 0.9
PARAMETER num_ctx 512
PARAMETER repeat_penalty 1.1
```

Commandes :

```bash
ollama create mistral-tests -f Modelfile
ollama run mistral-tests
```

---

## 4. Résumé recommandations (benchmarks de code)

* **num\_predict** : 200
* **temperature** : 0.2
* **top\_k** : 50
* **top\_p** : 0.9
* **num\_ctx** : 512
* **repeat\_penalty** : 1.1
* **quantization** : Q4 (`7b-instruct-q4_K_M`)
