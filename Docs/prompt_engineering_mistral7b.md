# 📝 Prompt Engineering – Mistral 7B

## 1. Objectif principal

Maximiser la fiabilité des sorties de Mistral 7B dans un cadre **benchmark automatisé**, où l’IA doit fournir du **code exécutable** immédiatement, sans explications parasites.

---

## 2. Constats observés

* **Réponses par défaut** : Mistral a tendance à introduire du texte explicatif avant ou après le code.
* **Balises de code** : il respecte souvent les balises `python … `, mais pas systématiquement.
* **Signatures de fonctions** : si elles ne sont pas imposées, Mistral peut modifier légèrement le nom ou les paramètres.
* **Temps de réponse** : temps médian observé autour de 9–10 secondes (exercice simple, 1 run).
* **Fiabilité avec prompt renforcé** : quand on impose bloc ` ```python … ``` ` et signature exacte, le score aux tests atteint 100 %.

---

## 3. Bonnes pratiques de prompt

1. **Toujours imposer un format strict**
   Exemple :

   ````
   Écris uniquement le code Python complet de la fonction suivante, sans explication,
   au format exact :
   ```python
   def <nom_fonction>(...) -> ...:
       # ton code ici
   ````

   ```
   ```
2. **Fournir la signature exacte** (nom + types + retour) → réduit le risque de variations.
3. **Exiger l’absence d’explications** (« sans explication », « uniquement le code »).
4. **Inclure les balises markdown ` ```python … ``` `** pour que l’extracteur puisse isoler le code facilement.
5. **Limiter l’ambiguïté** : une seule consigne claire par prompt.

---

## 4. Anti-patterns (à éviter)

* Ne pas demander « Explique et donne le code » → réponse mixte, difficile à parser.
* Ne pas laisser libre le choix de la signature → risque de `isPrime` ou `prime_check`.
* Ne pas oublier de préciser le format de sortie → sinon bloc sans `python` ou simple pseudo-code.

---

## 5. Exemple de prompt optimisé

````text
Écris uniquement le code Python complet de la fonction suivante, sans explication,
au format exact :
```python
def factorial(n: int) -> int:
    # ton code ici
````

```

---

## 6. Points à surveiller (futurs tests)
- Cas où Mistral oublie les backticks → prévoir fallback dans l’extracteur.  
- Cas où Mistral ajoute plusieurs fonctions → vérifier si ça perturbe l’évaluation.  
- Sensibilité à la langue : vérifier si consignes en anglais donnent des résultats plus propres que français.  

```
