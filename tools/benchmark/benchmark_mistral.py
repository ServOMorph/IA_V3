# tools/benchmark/benchmark_mistral2.py
"""
Script simplifié pour lancer directement un benchmark avec Mistral optimisé (mistral-tests).
"""
import sys
from pathlib import Path
import requests

# 🔹 Forcer la racine du projet dans le PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

from tools.benchmark.runner import benchmark
from tools.benchmark.exercises import EXERCISES


def check_ollama_running() -> bool:
    """Vérifie si Ollama est accessible en local"""
    try:
        r = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        if r.status_code == 200:
            print("✅ Ollama tourne (API accessible)")
            return True
    except Exception:
        pass
    print("❌ Ollama n'est pas lancé sur http://127.0.0.1:11434")
    return False


def main():
    if not check_ollama_running():
        sys.exit(1)

    model = "mistral-tests"  # modèle optimisé créé avec le Modelfile
    print(f"=== Benchmark Mistral optimisé ({model}) ===\n")

    # choix exercice
    print("=== Sélection de l'exercice ===")
    for i, ex in enumerate(EXERCISES.keys(), 1):
        print(f"{i}. {ex}")
    try:
        ex_choice = int(input(f"Sélectionnez un exercice (1-{len(EXERCISES)}) [1] : ").strip())
        exercise_key = list(EXERCISES.keys())[ex_choice - 1]
    except Exception:
        exercise_key = list(EXERCISES.keys())[0]

    # choix mode
    print("\n=== Sélection du mode ===")
    mode = input("Tapez 't' pour un test rapide (1 run), ou 'n' pour un benchmark normal : ").strip().lower()

    if mode == "t":
        runs = 1
        print("\n🚀 Mode test rapide (1 run)")
    else:
        runs = input("Combien d'essais voulez-vous faire ? [5] : ").strip()
        runs = int(runs) if runs.isdigit() else 5
        print(f"\n🚀 Mode benchmark normal ({runs} runs)")

    # lancement
    benchmark(exercise_key=exercise_key, runs=runs, model=model)


if __name__ == "__main__":
    main()
