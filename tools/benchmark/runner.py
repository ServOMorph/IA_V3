# tools/benchmark/runner.py
"""
Logique principale du benchmark
"""
import sys
from pathlib import Path

# 🔹 Forcer la racine du projet dans le PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

from core.ollama_client import OllamaClient
from tools.benchmark.config_benchmark import DEFAULT_MODEL
from tools.benchmark.exercises import EXERCISES
from tools.benchmark.code_utils import extract_code_blocks, evaluate_code, count_code_lines
from tools.benchmark.storage import persist_code, persist_results


def benchmark(exercise_key: str, runs=5, model=None):
    """Exécute un benchmark sur un modèle donné et un exercice donné."""
    exercise = EXERCISES[exercise_key]
    prompt = exercise["prompt"]
    tests = exercise["tests"]
    func_name = "is_prime" if exercise_key == "is_prime" else exercise_key

    client = OllamaClient(model=model if model else DEFAULT_MODEL)

    times, scores = [], []
    for i in range(runs):
        print(f"\n--- Essai {i+1}/{runs} [{model}] ---")
        response = client.send_prompt(prompt)
        if not response:
            print("❌ Pas de réponse.")
            continue

        # Temps
        if client.history:
            elapsed = client.history[-1]["elapsed"]
            times.append(elapsed)
            print(f"⏱ Temps mesuré: {elapsed:.2f} sec")

        # Code
        code = extract_code_blocks(response)
        persist_code(code, model, exercise_key, i + 1)

        # Cas spécial : exercice long_code_test -> compter lignes
        if exercise_key == "long_code_test":
            line_count = count_code_lines(code)
            print(f"📏 Nombre de lignes générées: {line_count}")

        # Évaluation standard si tests définis
        if tests:
            ok, total = evaluate_code(code, func_name, tests)
            score = ok / total if total > 0 else 0
            scores.append(score)
            print(f"📊 Score de tests: {ok}/{total} ({score*100:.1f}%)")

    if times:
        persist_results(model, exercise_key, prompt, times, scores)
    else:
        print("❌ Aucun temps mesuré.")
