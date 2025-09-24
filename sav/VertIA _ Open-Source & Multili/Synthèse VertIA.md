# 📘 Synthèse consolidée du projet VertIA

## 🎯 Vision et Objectifs

VertIA est une solution d’intelligence artificielle locale, éco-responsable et sécurisée, **soutenue par une formation pédagogique personnalisée**. Elle vise à offrir aux entreprises :

* Confidentialité et maîtrise totale des données.
* Réduction de l’empreinte carbone par rapport au cloud.
* Autonomie numérique et conformité RGPD.
* Une offre modulaire adaptée à différents secteurs (PME, administrations, associations).
* Une formation pédagogique personnalisée comme valeur différenciante.

**Positionnement retenu :** la pédagogie est un pilier central du projet, indissociable de l’offre technique.

---

## 🌍 Contexte de Marché et Tendances

* Croissance rapide des usages IA dans tous les secteurs (analyse de documents, copilotes, automatisation).
* Solutions cloud dominantes : coût récurrent, dépendance, risques de confidentialité.
* Attentes des entreprises : souveraineté numérique, réduction de l’empreinte carbone, contrôle budgétaire.
* Tendances clés : essor open-source (Mistral, Gemma, LLaMA), accessibilité GPU, soutien institutionnel, demande accrue PME et administrations【63】.

Potentiel de développement :

* Année 1 (2025) : finalisation développement, pilotes (20 installations prévues).
* Année 2 (2026) : extension aux PME sensibles (juridique, santé, comptabilité) + organismes publics.
* Année 3 (2027) : extension nationale (plusieurs dizaines d’installations/an).
* Année 4+ : consolidation et partenariats avec intégrateurs IT【63】.

---

## 🏗️ Architecture et Technologie

* **Backend** : Python avec API REST (FastAPI, Flask).
* **Frontend** : Application web simple (HTML/JS).
* **IA** : modèle open-source **Gemma**.
* **Matériel recommandé** :

  * CPU : AMD Ryzen 7 / Intel i7.
  * RAM : 32 Go (64 Go recommandé selon cas lourds).
  * GPU : NVIDIA RTX 4060.
  * Stockage : SSD NVMe rapide + disque externe sauvegarde.
  * Onduleur, batterie optionnelle (2h ≈ 400 €).
  * Routeur LAN ou Wi-Fi local dédié (≈ 50-100 €).
* **Sécurité** : chiffrement complet (LUKS, BitLocker), authentification 2FA locale (Google Authenticator), filtrage MAC, sauvegardes locales et hors site.
* **Logiciels** : Ubuntu Server, VM pour tests, IDE Visual Studio Code【62】【66】.

---

## 📦 Phases du Projet

### Phase 1 – Conception et Prototype (mois 1-3)

* Définir objectifs fonctionnels (types d’IA, cas d’usage, niveau de confidentialité).
* Développement technique IA.
* Tests sur installations pilotes.
* Tests unitaires et d’intégration.
* Optimisations (mémoire, temps de réponse).
* Formation initiale : 20h/mois par client.

### Phase 2 – Déploiement (mois 4-12)

* Installations clients : objectif 20 installations en année 1.
* Création de livrables marketing (présentation, fiche technique, argumentaire écologique, offre modulable).
* Packaging (image système, scripts d’installation, clé USB bootable).
* **Location du matériel** comme modèle économique.
* Accompagnement régulier : 15h présentiel + 5h distanciel par client.

### Phase 3 – Expansion (année 2 et +)

* Extension aux PME sensibles et organismes publics.
* Extension nationale prévue dès l’année 3.

### Phase 4 – Installation et Livraison finale

* Installation physique et configuration réseau local.
* Déploiement du modèle IA et paramétrage utilisateurs.
* Sécurité et sauvegarde (chiffrement, authentification, sauvegardes).
* Validation finale (tests sur machine cible, stabilité 48h).
* Livraison : manuel utilisateur, plan de maintenance, formation référent, signature de réception【62】.

---

## 💰 Modèle Économique

* **Location + Accompagnement** (modèle retenu) :

  * Loyer mensuel brut : 1 000 €.
  * Accompagnement : 70 €/h.
  * Rentabilité à partir de 3 installations (mois 3)【67】.

---

## 🌱 Impact Écologique

* Consommation serveur : 300-350 W (≈ 8,4 kWh/jour → 50 €/mois électricité).
* Réduction d’empreinte carbone par absence de data centers distants.
* Valorisation dans les démarches RSE.
* Recyclage local des composants possible.
* Subventions possibles : PACTE Industrie, garanties vertes, transition écologique【66】.

---

## 🏢 Organisation et Ressources Humaines

* Dirigeant : supervision, accompagnement, administratif.
* Développeur (mois 1-3) : réécriture du code, sécurisation, modularité.
* Commercial (dès mois 4) : prospection, clients.
* Responsable administratif (dès mois 4).
* Communication (mois 4+) : site web, visuels, marketing, contenu.
* Veille stratégique (mois 4+) : innovation, positionnement.

**Vie d’entreprise** : mécénat de compétence (1 jour/mois), jeux coopératifs (2x/semaine), sieste et repos, analyse de pratiques mensuelle, outils collaboratifs (Trello, Discord, Google Drive)【67】.

---

## ✅ Identité de Marque

* Nom retenu : **VertIA**.
* Positionnement : solution locale, éthique, humaine.
* Différenciation : pédagogie et formation intégrées comme valeur forte.


# Budget prévisionnel sur 3 ans

## Année 1

* **Charges principales** :

  * Forfait téléphonique : 5 à 10 €/mois
  * ChatGPT : 30 à 60 €/mois
  * Site internet : 2 €/mois
  * Assurance : 150 à 800 €/mois
  * Salaires : direction (3300 €/mois), freelance développeur (2165 €/mois), autres postes progressifs
  * Achats matériels : serveur (2230 €), PC portable (1500 €), PC fixe (600 €), mobilier (3000 €)
  * Locaux : 1500 €/mois à partir du mois 4
  * Autres : communication, déplacements, mutuelle, charges patronales
* **Produits** :

  * Entreprise pilote puis contrats clients (jusqu’à 20 400 €/mois en fin d’année)
  * Subventions et financements divers (BPI, région, réseaux, etc.)
* **Résultat** : bénéfices variables, trésorerie disponible fin d’année \~8 800 €【8†Budget prévisionnel - année 1.pdf】

## Année 2

* **Charges principales** :

  * Téléphonie : 10 à 15 €/mois
  * ChatGPT : 23 €/mois
  * Assurance : 300 à 900 €/mois
  * Salaires : direction (3300 €/mois), développeur freelance (2165 → 4330 €/mois), assistant gestion (779 → 1559 €/mois), responsable pédagogique (3637 €/mois), chargé pédagogique ajouté (jusqu’à 3334 €/mois)
  * Locaux : 1500 €/mois
  * Achats : serveur (3000 € + 2230 €/mois), mobilier ponctuel (3000 €)
* **Produits** :

  * Contrats clients en croissance régulière (26 000 → 48 000 €/mois)
  * Financements : CIR (9000 €), dons (2000 €), remboursement prêt d’honneur (-400 €/mois)
* **Résultat** : bénéfices faibles ou négatifs certains mois, trésorerie disponible fin d’année \~21 200 €【9†Budget prévisionnel - année 2.pdf】

## Année 3

* **Charges principales** :

  * Téléphonie : 20 à 25 €/mois
  * ChatGPT : 23 €/mois
  * Assurance : 400 à 1000 €/mois
  * Salaires : direction (3400 → 4500 €/mois), développeur freelance (6062 €/mois), assistant gestion (2728 €/mois), chargé pédagogique 1 (3637 €/mois), ajout de chargé pédagogique 2 et 3 (jusqu’à 3334 €/mois chacun)
  * Locaux : 1500 €/mois
  * Communication : 4000 €/mois
  * Achats : serveur (3000 puis 6000 €/mois), PC portables ponctuels (1000 €), mobilier (3000 €)
* **Produits** :

  * Contrats clients en forte croissance (62 400 → 115 200 €/mois)
  * Financements : CIR (10 800 €), remboursement prêt d’honneur (-400 €/mois)
* **Résultat** : bénéfices nets positifs, trésorerie disponible fin d’année \~148 500 €【10†Budget prévisionnel - année 3.pdf】

---

## Synthèse

* **Année 1** : forte dépendance aux financements externes, bénéfices irréguliers.
* **Année 2** : montée en charge salariale, croissance clients, trésorerie renforcée mais profits limités.
* **Année 3** : structure complète, masse salariale lourde, mais revenus clients élevés permettant bénéfices solides et trésorerie en forte croissance.

