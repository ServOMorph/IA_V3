# tools/benchmark/cli.py
"""
Interface CLI pour lancer les benchmarks
"""
import sys
from pathlib import Path

# 🔹 Forcer la racine du projet dans le PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

import requests
from tools.benchmark.config_benchmark import DEFAULT_MODEL
from core.ollama_client import list_installed_models
from tools.benchmark.exercises import EXERCISES
from tools.benchmark.runner import benchmark


def check_ollama_running() -> bool:
    try:
        r = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        if r.status_code == 200:
            print("✅ Ollama tourne (API accessible)")
            return True
    except Exception:
        pass
    print("❌ Ollama n'est pas lancé sur http://127.0.0.1:11434")
    return False


def get_models() -> list[str]:
    models_output = list_installed_models()
    if not models_output:
        return []
    lines = [line for line in models_output.splitlines() if line.strip()]
    return [line.split()[0] for line in lines if line.split()[0].lower() != "name"]


def main():
    if not check_ollama_running():
        sys.exit(1)

    models = get_models()
    if not models:
        print("⚠️ Aucun modèle Ollama détecté.")
        sys.exit(1)

    print("\n=== Sélection de l'exercice ===")
    for i, ex in enumerate(EXERCISES.keys(), 1):
        print(f"{i}. {ex}")
    try:
        ex_choice = int(input(f"Sélectionnez un exercice (1-{len(EXERCISES)}) [1] : ").strip())
        exercise_key = list(EXERCISES.keys())[ex_choice - 1]
    except Exception:
        exercise_key = list(EXERCISES.keys())[0]

    # Mode test à blanc
    print("\n=== Mode test ===")
    dry_run = input("Faire un test à blanc (aucune requête envoyée) ? (o/n) : ").strip().lower()
    if dry_run == "o":
        exercise = EXERCISES[exercise_key]
        print("\n--- TEST À BLANC ---")
        print(f"Modèle par défaut: {DEFAULT_MODEL}")
        print(f"Exercice: {exercise_key}")
        print(f"Prompt qui sera utilisé:\n{exercise['prompt']}\n")
        print(f"Les fichiers générés seront sauvegardés dans: data/generated/<model>/<exercise>/")
        sys.exit(0)

    print("\n=== Sélection du mode de test ===")
    choice_all = input("Lancer le test pour TOUS les modèles listés ? (o/n) : ").strip().lower()
    runs = input("Combien d'essais voulez-vous faire ? [5] : ").strip()
    runs = int(runs) if runs.isdigit() else 5

    if choice_all == "o":
        for model in models:
            print(f"\n🚀 Benchmark sur le modèle : {model}")
            benchmark(exercise_key=exercise_key, runs=runs, model=model)
    else:
        print("=== Sélection du modèle IA ===")
        for i, m in enumerate(models, 1):
            print(f"{i}. {m}")
        try:
            choice = int(input(f"Sélectionnez un modèle (1-{len(models)}) [par défaut {DEFAULT_MODEL}] : ").strip())
            if 1 <= choice <= len(models):
                selected_model = models[choice - 1]
            else:
                selected_model = DEFAULT_MODEL
        except Exception:
            selected_model = DEFAULT_MODEL
        benchmark(exercise_key=exercise_key, runs=runs, model=selected_model)


if __name__ == "__main__":
    main()
