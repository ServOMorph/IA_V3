# 📝 Prompt Engineering – DeepSeek Coder 6.7B

## 1. Objectif principal

Maximiser la fiabilité des sorties de DeepSeek Coder 6.7B dans un cadre **benchmark automatisé**, où l’IA doit fournir du **code exécutable** immédiatement, sans explications parasites.

---

## 2. Constats observés

* **Respect du format** : DeepSeek suit correctement la consigne avec balises `python … ` quand elles sont imposées.
* **Réponses** : produit directement du code, peu d’explications hors bloc si le prompt est strict.
* **Signatures de fonctions** : respecte la signature imposée sans variation.
* **Temps de réponse** : \~15 secondes sur l’exercice `is_prime` (plus lent que Mistral \~9 sec, mais plus rapide qu’un premier test à \~20 sec).
* **Fiabilité** : score 100 % aux tests unitaires dès le premier run.
* **Stabilité** : comportement stable entre runs, code bien formaté.

---

## 3. Bonnes pratiques de prompt

1. **Imposer le bloc formaté** ` ```python … ``` `.
2. **Donner la signature exacte** (DeepSeek la respecte sans modification).
3. **Exiger l’absence d’explications** (« uniquement le code », « sans commentaire ni texte additionnel » si besoin).
4. **Anticiper la latence** : DeepSeek est plus lent que Mistral, prévoir un temps d’attente plus long.

---

## 4. Anti-patterns (à éviter)

* Ne pas laisser de liberté dans la signature → même si DeepSeek est discipliné, cela évite toute variation.
* Ne pas demander d’explication en plus du code → pour garantir une sortie directement exploitable.

---

## 5. Exemple de prompt optimisé

````text
Écris uniquement le code Python complet de la fonction suivante, sans explication, 
au format exact :
```python
def is_prime(n: int) -> bool:
    # ton code ici
````

```

---

## 6. Points à surveiller (futurs tests)
- Vérifier le comportement sur des exercices plus complexes (récursifs, structures de données).  
- Évaluer si DeepSeek ajoute parfois des commentaires internes dans le code.  
- Comparer cohérence et vitesse entre prompts en français et en anglais.  
- Mesurer la régularité des temps de réponse sur plusieurs runs.

```
