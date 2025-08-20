# 📑 Modèle de prompt parfait pour BackIA

## 📝 Objectif

Ce document définit la structure et les règles à respecter pour rédiger un **prompt destiné à BackIA**. Il sert de modèle générique, réutilisable et modifiable facilement pour toutes les missions confiées à cet agent.

---

## 1. Structure générale du prompt

Un prompt parfait pour BackIA doit être organisé ainsi :

1. **Titre clair** avec le nom de la mission et le numéro d’étape.
   Exemple :

   ```
   ### 🎯 Mission BackIA — Étape 1.1 : Création structure API
   ```

2. **Contexte fourni** : toujours lister les fichiers et documents déjà disponibles.
   Exemple :

   * Arborescence actuelle du projet (`arborescence.txt`)
   * README global du projet (`README.md`)
   * Document de suivi (`docs/developpement_suivi_complet.md`)
   * Convention de nommage (`docs/CONVENTION_LIVRABLES.md`)

3. **Objectif** : décrire la finalité de la tâche en une ou deux phrases claires.

4. **Tâches précises** : liste numérotée, détaillée mais concise.

   * Inclure ce qu’il faut coder.
   * Ce qu’il faut documenter.
   * Les tests à prévoir.
   * Les vérifications spécifiques.

5. **Livrable attendu** :

   * Toujours **un seul fichier Markdown autoportant**.
   * Nom imposé (`<étape>-<fichier>-de_BackIA_pour_GestIA-<heure>-<date>.md`).
   * Liste claire du contenu obligatoire à inclure :

     * Code produit.
     * Documentation spécifique.
     * Résumé du README global.
     * Arborescence mise à jour (sans fichiers parasites).
     * Liste des fichiers créés/modifiés.
     * Titre complet du fichier en première ligne.

6. **Protocole** : règles fixes à rappeler à chaque fois.

   * Arborescence mise à jour (sans fichiers parasites, pas de `.md.md`).
   * README global résumé.
   * README spécifique rappelant le rôle du fichier principal.
   * Liste des fichiers modifiés/créés.
   * Livrable final autoportant.
   * Titre du fichier livrable en première ligne de la réponse.

7. **Instruction spéciale** : rappeler que la réponse doit être **ouverte et livrée dans Canevas**.

---

## 2. Points d’attention pour BackIA

* Ne jamais inclure de fichiers parasites dans l’arborescence.
* Toujours rappeler le rôle du fichier principal dans le README spécifique.
* Vérifier le nommage exact des fichiers (pas de double extension `.md.md`).
* Ajouter des docstrings et du typage si pertinent.
* Mentionner les tests futurs quand ils sont prévus dans les étapes suivantes.

---

## 3. Exemple minimal de prompt conforme

```markdown
### 🎯 Mission BackIA — Étape X.X : [Nom de la mission]

**Contexte fourni :**
- Arborescence actuelle du projet (`arborescence.txt`).
- README global du projet (`README.md`).
- Document de suivi (`docs/developpement_suivi_complet.md`).
- Convention de nommage (`docs/CONVENTION_LIVRABLES.md`).

**Objectif :**
Décrire ici l’objectif clair de la mission.

**Tâches précises :**
1. Première tâche.
2. Deuxième tâche.
3. …

**Livrable attendu (un seul fichier Markdown autoportant) :**
- À déposer dans `/responses/` sous le nom :
```

<étape>-<fichier>-de\_BackIA\_pour\_GestIA-<heure>-<date>.md

```
- Ce fichier doit contenir :
- Code complet.
- Documentation spécifique (incluant rappel du rôle du fichier principal).
- Résumé du README global.
- Arborescence mise à jour (sans fichiers parasites).
- Liste des fichiers créés/modifiés.
- Titre complet du fichier en première ligne.

**Protocole :**
Toujours fournir :
1. Arborescence mise à jour (sans fichiers parasites, sans `.md.md`).
2. README global (résumé obligatoire).
3. README spécifique (avec rôle du fichier principal).
4. Liste des fichiers créés/modifiés.
5. Livrable final autoportant avec le titre du fichier en première ligne.

**⚠️ Instruction supplémentaire :**
Le fichier réponse doit être **ouvert et livré dans Canevas**.
```

---

## 4. Maintenance du modèle

Ce document doit être :

* **Mis à jour régulièrement** après chaque mission pour intégrer les nouvelles bonnes pratiques.
* Conservé dans `/docs/modele/` sous le nom `MODELE_PROMPT_BackIA.md`.
* Utilisé comme référence pour générer automatiquement les prompts destinés à BackIA.
