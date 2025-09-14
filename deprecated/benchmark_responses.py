# tools/benchmark_responses.py
import sys
from pathlib import Path

# 🔹 Ajouter la racine du projet au PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import statistics
import json
import requests
import tempfile
import importlib.util
from datetime import datetime
import re
from core.ollama_client import OllamaClient, list_installed_models
from config import DEFAULT_MODEL, DATA_DIR

# ==============================
# 🔹 Exercices disponibles
# ==============================
EXERCISES = {
    "is_prime": {
        "prompt": "Écris une fonction Python 'is_prime(n: int) -> bool' qui retourne True si n est premier, False sinon.",
        "tests": {2: True, 4: False, 17: True, 18: False, 19: True, 1: False, 97: True}
    },
    "fibonacci": {
        "prompt": "Écris une fonction Python 'fibonacci(n: int) -> int' qui retourne le n-ième terme de la suite de Fibonacci (0-indexée).",
        "tests": {0: 0, 1: 1, 2: 1, 5: 5, 7: 13, 10: 55}
    },
    "factorial": {
        "prompt": "Écris une fonction Python 'factorial(n: int) -> int' qui retourne la factorielle de n.",
        "tests": {0: 1, 1: 1, 3: 6, 5: 120, 7: 5040}
    },
}

# Répertoire de sauvegarde du code généré
GENERATED_DIR = DATA_DIR / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def check_ollama_running():
    """Teste si Ollama tourne sur 127.0.0.1:11434"""
    try:
        r = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        if r.status_code == 200:
            print("✅ Ollama tourne (API accessible)")
            return True
    except Exception:
        pass
    print("❌ Ollama n'est pas lancé sur http://127.0.0.1:11434")
    return False


def get_models():
    """Retourne la liste des modèles installés (hors en-tête)."""
    models_output = list_installed_models()
    if not models_output:
        return []

    lines = [line for line in models_output.splitlines() if line.strip()]
    models = []
    for line in lines:
        parts = line.split()
        if parts[0].lower() == "name":  # ignorer l'entête
            continue
        models.append(parts[0])
    return models


# =========================
# 🔹 Partie "tests de code"
# =========================
def extract_code_blocks(text: str) -> str:
    """Extrait le premier bloc de code Python ```...``` si présent."""
    if "```" not in text:
        return text
    parts = text.split("```")
    for part in parts:
        if part.strip().startswith("python"):
            return part.replace("python", "", 1).strip()
        if part.strip():
            return part.strip()
    return text


def run_code_tests(code: str, func_name: str, tests: dict) -> tuple[int, int]:
    """
    Exécute le code IA et teste la fonction demandée.
    Retourne (nb_tests_ok, nb_tests_total).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        file = Path(tmpdir) / "solution.py"
        file.write_text(code, encoding="utf-8")

        spec = importlib.util.spec_from_file_location("solution", file)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution du code : {e}")
            return 0, len(tests)

        func = getattr(module, func_name, None)
        if not func:
            print(f"❌ Fonction '{func_name}' introuvable dans la réponse.")
            return 0, len(tests)

        ok = 0
        for inp, expected in tests.items():
            try:
                if func(inp) == expected:
                    ok += 1
            except Exception:
                pass

        return ok, len(tests)


# =========================
# 🔹 Sauvegarde du code
# =========================
def sanitize_name(name: str) -> str:
    """Remplace les caractères interdits par underscore (Windows/Linux safe)."""
    return re.sub(r'[^A-Za-z0-9._-]', '_', name)


def save_generated_code(code: str, model: str, exercise: str, run_id: int) -> None:
    """Sauvegarde le code généré dans data/generated/<model>/<exercise>/"""
    safe_model = sanitize_name(model)
    safe_exercise = sanitize_name(exercise)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = GENERATED_DIR / safe_model / safe_exercise
    folder.mkdir(parents=True, exist_ok=True)
    filename = f"solution_{safe_model}_{safe_exercise}_run{run_id}_{timestamp}.py"
    file_path = folder / filename
    file_path.write_text(code, encoding="utf-8")
    print(f"💾 Code sauvegardé dans {file_path}")


# =========================
# 🔹 Benchmark principal
# =========================
def benchmark(exercise_key: str, runs=5, model=None):
    """Exécute un benchmark sur un modèle donné et un exercice donné."""
    exercise = EXERCISES[exercise_key]
    prompt = exercise["prompt"]
    tests = exercise["tests"]
    func_name = exercise_key if exercise_key != "is_prime" else "is_prime"

    client = OllamaClient(model=model if model else DEFAULT_MODEL)

    times = []
    scores = []
    for i in range(runs):
        print(f"\n--- Essai {i+1}/{runs} [{model}] ---")
        response = client.send_prompt(prompt)
        if not response:
            print("❌ Pas de réponse.")
            continue

        # Mesure du temps
        if client.history:
            elapsed = client.history[-1]["elapsed"]
            times.append(elapsed)
            print(f"⏱ Temps mesuré: {elapsed:.2f} sec")

        # 🔹 Test de la qualité du code
        code = extract_code_blocks(response)
        save_generated_code(code, model, exercise_key, i + 1)  # sauvegarde permanente
        ok, total = run_code_tests(code, func_name, tests)
        score = ok / total if total > 0 else 0
        scores.append(score)
        print(f"📊 Score de tests: {ok}/{total} ({score*100:.1f}%)")

    if times:
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        avg_score = statistics.mean(scores) if scores else 0

        print("\n=== Résultats ===")
        print(f"Modèle testé: {model}")
        print(f"Exercice: {exercise_key}")
        print(f"Prompt utilisé: {prompt}")
        print(f"Nombre d'essais: {len(times)}")
        print(f"Temps moyen: {avg_time:.2f} sec")
        print(f"Min: {min_time:.2f} sec")
        print(f"Max: {max_time:.2f} sec")
        print(f"Score moyen: {avg_score*100:.1f}%")

        # 🔹 Sauvegarde dans data/
        txt_file = DATA_DIR / "dev_responses.log"
        with txt_file.open("a", encoding="utf-8") as f:
            f.write("=== RÉSUMÉ BENCHMARK ===\n")
            f.write(f"Modèle: {model}\n")
            f.write(f"Exercice: {exercise_key}\n")
            f.write(f"Prompt: {prompt}\n")
            f.write(f"Essais: {len(times)}\n")
            f.write(f"Temps moyen: {avg_time:.2f} sec\n")
            f.write(f"Min: {min_time:.2f} sec\n")
            f.write(f"Max: {max_time:.2f} sec\n")
            f.write(f"Score moyen: {avg_score*100:.1f}%\n")
            f.write("========================\n")

        json_file = DATA_DIR / "dev_responses.jsonl"
        summary = {
            "summary": True,
            "model": model,
            "exercise": exercise_key,
            "prompt": prompt,
            "runs": len(times),
            "avg_time": round(avg_time, 3),
            "min_time": round(min_time, 3),
            "max_time": round(max_time, 3),
            "avg_score": round(avg_score, 3)
        }
        with json_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(summary, ensure_ascii=False) + "\n")

    else:
        print("❌ Aucun temps mesuré.")


# =========================
# 🔹 CLI
# =========================
if __name__ == "__main__":
    if not check_ollama_running():
        sys.exit(1)  # Arrêter le script si Ollama ne tourne pas

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

    # 🔹 Mode test à blanc
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
