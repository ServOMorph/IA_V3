# tools/benchmark_responses.py
import sys
from pathlib import Path

# 🔹 Ajouter la racine du projet au PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import statistics
import json
import requests
from core.ollama_client import OllamaClient, list_installed_models
from config import DEFAULT_MODEL, DATA_DIR


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


def select_model():
    """Affiche les modèles installés et demande à l'utilisateur lequel utiliser."""
    models_output = list_installed_models()
    if not models_output:
        return DEFAULT_MODEL

    lines = [line for line in models_output.splitlines() if line.strip()]
    models = []
    for line in lines:
        parts = line.split()
        if parts[0].lower() == "name":  # ignorer l'entête
            continue
        models.append(parts[0])

    if not models:
        print(f"Aucun modèle trouvé, utilisation du modèle par défaut : {DEFAULT_MODEL}")
        return DEFAULT_MODEL

    print("=== Sélection du modèle IA ===")
    for i, m in enumerate(models, 1):
        print(f"{i}. {m}")

    try:
        choice = int(input(f"Sélectionnez un modèle (1-{len(models)}) [par défaut {DEFAULT_MODEL}] : ").strip())
        if 1 <= choice <= len(models):
            return models[choice - 1]
    except Exception:
        pass

    print(f"→ Aucun choix valide, utilisation du modèle par défaut : {DEFAULT_MODEL}")
    return DEFAULT_MODEL


def benchmark(prompt, runs=5, model=None):
    client = OllamaClient(model=model if model else DEFAULT_MODEL)

    times = []
    for i in range(runs):
        print(f"\n--- Essai {i+1}/{runs} ---")
        response = client.send_prompt(prompt)
        if client.history:
            elapsed = client.history[-1]["elapsed"]
            times.append(elapsed)
            print(f"⏱ Temps mesuré: {elapsed:.2f} sec")
        else:
            print("❌ Pas de réponse.")

    if times:
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)

        print("\n=== Résultats ===")
        print(f"Modèle testé: {model}")
        print(f"Prompt utilisé: {prompt}")
        print(f"Nombre d'essais: {len(times)}")
        print(f"Temps moyen: {avg_time:.2f} sec")
        print(f"Min: {min_time:.2f} sec")
        print(f"Max: {max_time:.2f} sec")

        # 🔹 Sauvegarde aussi dans data/
        txt_file = DATA_DIR / "dev_responses.log"
        with txt_file.open("a", encoding="utf-8") as f:
            f.write("=== RÉSUMÉ BENCHMARK ===\n")
            f.write(f"Modèle: {model}\n")
            f.write(f"Prompt: {prompt}\n")
            f.write(f"Essais: {len(times)}\n")
            f.write(f"Temps moyen: {avg_time:.2f} sec\n")
            f.write(f"Min: {min_time:.2f} sec\n")
            f.write(f"Max: {max_time:.2f} sec\n")
            f.write("========================\n")

        json_file = DATA_DIR / "dev_responses.jsonl"
        summary = {
            "summary": True,
            "model": model,
            "prompt": prompt,
            "runs": len(times),
            "avg_time": round(avg_time, 3),
            "min_time": round(min_time, 3),
            "max_time": round(max_time, 3)
        }
        with json_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(summary, ensure_ascii=False) + "\n")

    else:
        print("❌ Aucun temps mesuré.")


if __name__ == "__main__":
    if not check_ollama_running():
        sys.exit(1)  # Arrêter le script si Ollama ne tourne pas

    model = select_model()
    prompt = input("Entrez le prompt à envoyer : ").strip() or "Coucou"
    runs = input("Combien d'essais voulez-vous faire ? [5] : ").strip()
    runs = int(runs) if runs.isdigit() else 5

    benchmark(prompt=prompt, runs=runs, model=model)
