# IA\_V3 – Chat IA avec Ollama, gestion avancée des conversations et interface Kivy

## 📌 Description

Projet backend + UI pour interagir avec un modèle IA local via **Ollama**, avec gestion avancée des conversations, interface Kivy et **module de benchmark intégré**.

### Fonctionnalités principales :

* Dialogue avec un modèle IA local.
* Sauvegarde des conversations dans un **dossier par session** (`/sav/<nom_session>/conversation.md`).
* Sauvegarde automatique des blocs de code Python extraits en `.py`.
* Chargement, renommage, suppression et organisation des sessions.
* Copie rapide des derniers messages dans le presse-papier (CLI).
* Conservation du contexte conversationnel.
* Logs techniques et conversationnels séparés (`/logs/<nom_session>.log`).
* **Interface Kivy moderne** avec zones distinctes : liste de conversations, chat, saisie, panneau info/config.
* Couleurs centralisées dans `ui/config_ui.py`.
* **Mode DEV** :

  * Liste les modèles Ollama installés au démarrage.
  * Permet de choisir le modèle IA à utiliser.
  * Affiche et logge le temps de réponse pour chaque prompt.
  * Sauvegarde chaque essai et benchmark dans `data/dev_responses.log` et `data/dev_responses.jsonl`.
* **Module Benchmark IA** :

  * Exécution de tests unitaires automatiques (ex. `is_prime`, `fibonacci`, `factorial`).
  * Scripts dédiés pour lancer rapidement des benchmarks ciblés :

    * `benchmark_mistral.py` (Mistral standard)
    * `benchmark_mistral2.py` (Mistral optimisé : `mistral-tests`)
    * `benchmark_deepseek.py` (DeepSeek optimisé : `deepseek-tests`)
    * `benchmark_phi.py` (Phi-4 et Phi-4 Mini)
    * `benchmark_starling.py` (Starling-LM)
    * `benchmark_llava.py` (LLaVA multimodal)
  * Sauvegarde des résultats (code généré + stats) dans `data/generated/` et `data/dev_responses.*`.
  * Documentation associée dans `docs/` (prompt engineering et comparatifs).

---

## 📂 Arborescence complète

```
📁 IA_V3/
    📄 arborescence.txt
    📄 config.py
    📄 debug.log
    📄 main.py
    📄 main_benchmark.py
    📄 main_ui.py
    📄 README.md
    📁 .pytest_cache/
    📁 .ruff_cache/
    📁 assets/
        📁 images/
            📄 coche_icon.png
            📄 copier_icon.png
            📄 fond_window.png
            📄 Logo_IA.png
            📄 plus_icon.png
            📄 send_icon.png
            📄 send_icon2.png
    📁 client/
        📄 ia_client.py
        📄 __init__.py
    📁 core/
        📄 chat_manager.py
        📄 commands.py
        📄 ollama_client.py
        📄 sav_manager.py
        📄 session_manager.py
        📄 startup_utils.py
        📄 __init__.py
        📁 logging/
            📄 conv_logger.py
            📄 logger.py
            📄 __init__.py
    📁 data/
        📄 dev_responses.jsonl
        📄 dev_responses.log
        📄 models_list.txt
        📁 generated/
            📁 deepseek-coder_6.7b/
            📁 deepseek-tests/
            📁 mistral-tests/
            📁 mistral_latest/
    📁 Docs/
        📄 comparatif_mistral_vs_deepseek.md
        📄 ollama_models_readme.md
        📄 prompt_engineering_deepseek.md
        📄 prompt_engineering_mistral7b.md
        📄 prompt_engineering_phi.md
        📄 prompt_engineering_starling.md
        📄 prompt_engineering_llava.md
    📁 logs/
        📄 conversation.log
        📄 sav_conv_*.log
        📄 test11.log
        📄 test12.log
    📁 ollama_configs/
        📄 README.md
        📁 deepseek_tests/
            📄 Modelfile
            📄 README.md
        📁 mistral_tests/
            📄 Modelfile
            📄 README.md
        📁 phi_tests/
            📄 Modelfile
            📄 README.md
        📁 starling_tests/
            📄 Modelfile
            📄 README.md
        📁 llava_tests/
            📄 Modelfile
            📄 README.md
    📁 sav/
        📁 sav_conv_*/
            📄 conversation.md
        📁 test11/
            📄 code_*.py
            📄 conversation.md
        📁 test12/
            📄 code_*.py
            📄 conversation.md
    📁 tests/
        📄 test_ui_load.py
        📄 __init__.py
        📁 fenetre_kivy/
            📄 __init__.py
    📁 tools/
        📄 analyze_dev_logs.py
        📄 benchmark_responses.py
        📄 calc_fond_dims.py
        📄 init_conv_chatgpt.py
        📄 update_system_prompt.py
        📁 benchmark/
            📄 benchmark_deepseek.py
            📄 benchmark_mistral.py
            📄 benchmark_phi.py
            📄 benchmark_starling.py
            📄 benchmark_llava.py
            📄 cli.py
            📄 code_utils.py
            📄 config_benchmark.py
            📄 exercises.py
            📄 readme.md
            📄 runner.py
            📄 storage.py
            📄 __init__.py
    📁 ui/
        📄 app_main.py
        📄 config_ui.py
        📄 layout_builder.py
        📄 __init__.py
        📁 behaviors/
            📄 hover_behavior.py
            📄 __init__.py
        📁 widgets/
            📄 buttons.py
        📁 zones/
            📄 zone_chat.py
            📄 zone_liste_conv.kv
            📄 zone_liste_conv.py
            📄 zone_message.kv
            📄 zone_message.py
            📄 __init__.py
```

---

## 🖥️ Commandes utiles Ollama (Windows / CMD)

* Lister les modèles installés :

```bash
ollama list
```

* Télécharger un modèle :

```bash
ollama pull mistral:7b
ollama pull deepseek-coder:6.7b
ollama pull phi4:latest
ollama pull phi4-mini:latest
ollama pull starling-lm:7b
ollama pull llava:7b
```

* Supprimer un modèle :

```bash
ollama rm mistral:7b
ollama rm phi4-mini:latest
```

* Vérifier que le serveur Ollama tourne :

```bash
curl http://127.0.0.1:11434/api/tags
```

* Démarrer manuellement le serveur :

```bash
ollama serve
```

---

## 📊 Analyse des performances

* Benchmarks automatisés via `tools/benchmark/`.
* Résultats sauvegardés dans `data/dev_responses.*`.
* Analyse possible via :

```bash
python tools/analyze_results.py
```

* Comparatifs disponibles :

  * `docs/comparatif_mistral_vs_deepseek.md`
  * `docs/prompt_engineering_phi.md`
  * `docs/prompt_engineering_starling.md`
  * `docs/prompt_engineering_llava.md`

---

## ⚡ Conseils d’optimisation des performances

* **Quantisation** : utiliser les variantes Q4/Q5 (`-q4_K_M`) pour réduire la VRAM et accélérer l’inférence.
* **Context length** : rester à 4k ou 8k tokens pour garder l’exécution GPU. Au-delà, bascule CPU → ralentissements.
* **Choix des modèles adaptés à la RTX 4060 (8 Go VRAM)** :

  * Général : `mistral:7b`, `llama3.1:8b-q4`, `gemma:7b`, `phi4-mini:3.8b`
  * Code : `deepseek-coder:6.7b`, `qwen2.5-coder:7b`
  * Multimodal : `llava:7b`
  * Raisonnement : `starling-lm:7b`, `phi4:latest`
* **Batch size** : réduire si la VRAM est saturée.
* **Threads CPU** : utiliser 16 threads sur Ryzen 7 5700X pour compenser en mode CPU fallback.

---

## 🌟 Modèles recommandés (Top 5)

* **Mistral 7B** → usage général rapide, polyvalent.
* **Qwen2.5-Coder 7B** → spécialisé code.
* **LLaVA 7B Q4** → multimodal texte+image.
* **Starling-LM 7B** → raisonnement/débat.
* **Phi-4 Mini 3.8B** → compact, fluide pour tâches rapides.

---

## 🔮 Améliorations prévues

* Nouveaux benchmarks pour Phi-4, Starling-LM et LLaVA.
* Automatisation des tests multimodaux (texte + image).
* Export automatique en CSV/Excel.
* Dashboard de visualisation (Grafana/Streamlit).
* Optimisation GPU/paramètres supplémentaires pour les modèles lourds.
* Intégration d’un gestionnaire de profils (configurations par modèle).
