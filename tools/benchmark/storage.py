# tools/benchmark/storage.py
"""
Sauvegarde du code généré et des résultats
"""
import sys
from pathlib import Path

# 🔹 Forcer la racine du projet dans le PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

import re
import statistics
import json
from datetime import datetime
from tools.benchmark.config_benchmark import DATA_DIR

GENERATED_DIR = DATA_DIR / "generated"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_name(name: str) -> str:
    """Remplace les caractères interdits par underscore (Windows/Linux safe)."""
    return re.sub(r'[^A-Za-z0-9._-]', '_', name)


def persist_code(code: str, model: str, exercise: str, run_id: int) -> Path:
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
    return file_path


def persist_results(model: str, exercise_key: str, prompt: str, times: list[float], scores: list[float]) -> None:
    """Sauvegarde les résultats en log texte et JSONL"""
    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)
    avg_score = statistics.mean(scores) if scores else 0

    # Console
    print("\n=== Résultats ===")
    print(f"Modèle testé: {model}")
    print(f"Exercice: {exercise_key}")
    print(f"Prompt utilisé: {prompt}")
    print(f"Nombre d'essais: {len(times)}")
    print(f"Temps moyen: {avg_time:.2f} sec")
    print(f"Min: {min_time:.2f} sec")
    print(f"Max: {max_time:.2f} sec")
    print(f"Score moyen: {avg_score*100:.1f}%")

    # Fichier texte
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

    # JSONL
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
        "avg_score": round(avg_score, 3),
    }
    with json_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(summary, ensure_ascii=False) + "\n")
