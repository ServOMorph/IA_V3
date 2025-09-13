# 📊 Comparatif Mistral vs DeepSeek

Ce document présente un comparatif des performances entre **Mistral** et **DeepSeek Coder 6.7B**, en version standard et optimisée pour les benchmarks de code Python.

---

## 1. Résultats mesurés

### 🔹 Exercice : `is_prime`

| Modèle           | Temps moyen | Score tests | Observations                                                                         |
| ---------------- | ----------- | ----------- | ------------------------------------------------------------------------------------ |
| Mistral (latest) | \~9 sec     | 100 %       | Code correct, format respecté                                                        |
| Mistral-tests    | \~9 sec     | 100 %       | Paramètres optimisés (`num_predict=200`, `num_ctx=512`) → même score, latence stable |
| DeepSeek (6.7B)  | \~15–20 sec | 100 %       | Plus lent, mais fiable, code propre                                                  |
| DeepSeek-tests   | \~11,6 sec  | 100 %       | Optimisation réduit la latence, code toujours correct                                |

---

## 2. Analyse

* **Performance** : Mistral est le plus rapide (\~9 sec), DeepSeek optimisé se rapproche (\~11,6 sec) mais reste plus lent.
* **Fiabilité** : tous les modèles (vanilla et optimisés) passent les tests à 100 %.
* **Impact optimisation** : réduction nette du temps de réponse pour DeepSeek (de \~20 à \~11,6 sec). Mistral n’a pas beaucoup gagné car il était déjà rapide.
* **Consommation mémoire** : Mistral optimisé utilise la variante quantisée Q4 (\~4.4 GB). DeepSeek reste léger (\~3.8 GB).

---

## 3. Conclusion

* **Pour rapidité** → Mistral-tests reste le meilleur choix.
* **Pour stabilité et légèreté** → DeepSeek-tests est une bonne alternative, mais plus lent.
* **Optimisation utile surtout pour DeepSeek** qui passe de \~20 sec à \~11,6 sec avec nos réglages.

---

## 4. Prochaines étapes

* Étendre le benchmark à d’autres exercices (`fibonacci`, `factorial`, etc.).
* Ajouter des prompts plus complexes (ex. algorithmes de tri, manipulations de chaînes).
* Mesurer la stabilité sur plusieurs runs (moyenne, min, max).
