# 📐 Convention de nommage et gestion des livrables — agents\_ia\_project

## 📝 Objectif

Définir des règles strictes de nommage et de stockage des fichiers produits par les agents afin d’assurer une traçabilité claire et un suivi rigoureux.

---

## 1. Structure des livrables

### 1.1 Prompts (demandes de GestIA → autres agents)

* **Emplacement** : `/prompts/`
* **Format du nom de fichier** :

  ```
  <étape>-<fichier_cible>-de_GestIA_pour_<Agent>-<heure>-<date>.md
  ```

### 1.2 Réponses (retours des agents → GestIA)

* **Emplacement** : `/responses/`
* **Format du nom de fichier** :

  ```
  <étape>-<fichier_cible>-de_<Agent>_pour_GestIA-<heure>-<date>.md
  ```
* ⚠️ Interdiction des doubles extensions (`.md.md`).

---

## 2. Contenu minimal attendu

Chaque **réponse** doit être contenue dans **un seul fichier Markdown** autoportant.
Il doit inclure :

1. Code produit (encadré entre balises \`\`\` pour extraction).
2. Documentation rédigée.
3. Arborescence mise à jour (sans fichiers parasites).
4. README spécifique de la partie travaillée (nouveau ou mis à jour).
5. Résumé du README global (même si inchangé).
6. Liste des fichiers créés/modifiés.
7. Titre complet du fichier livrable en **première ligne** du document.

---

## 3. Rôle de GestIA

* Les agents secondaires (BackIA, DonIA, etc.) **ne modifient jamais directement** les fichiers globaux du projet.
* Ils produisent uniquement leur réponse complète dans `/responses/`.
* **GestIA** est l’unique responsable pour :

  * Extraire les parties pertinentes de chaque réponse.
  * Mettre à jour les fichiers du projet (ex. `main.py`, `docs/README_api.md`, `arborescence.txt`).
  * Maintenir la cohérence des documents de suivi (`docs/developpement_suivi.md` et `docs/developpement_suivi_complet.md`).
  * Corriger les éventuelles incohérences (fichiers parasites, erreurs de nommage).

---

## 4. Règles complémentaires

* Chaque mission doit préciser les **livrables attendus (noms imposés)** dans le prompt.
* Les README spécifiques (API, Ollama, Frontend, Agents, Tests, Docs) doivent être fournis par l’agent dans sa réponse, puis extraits et validés par GestIA.
* L’arborescence (`arborescence.txt`) doit toujours être mise à jour et intégrée par GestIA.
* Toute réponse doit être **ouverte dans Canevas** pour permettre son édition, sa vérification et son export.

---

## 5. Exemple concret

### Prompt

```
/prompts/1.1-main.py-de_GestIA_pour_BackIA-19h55-2025-08-20.md
```

### Réponse

```
/responses/1.1-main.py-de_BackIA_pour_GestIA-20h10-2025-08-20.md
```

### Livrables intégrés par GestIA

* `/main.py`
* `/docs/api_initialisation.md`
* `/docs/README_api.md`
* `/arborescence.txt`
* Mise à jour de `/docs/developpement_suivi_complet.md`
