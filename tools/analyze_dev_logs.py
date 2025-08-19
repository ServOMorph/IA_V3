# analyze_dev_logs.py
import pandas as pd
from pathlib import Path

DATA_FILE = Path("data/dev_responses.jsonl")

def main():
    if not DATA_FILE.exists():
        print(f"❌ Fichier introuvable : {DATA_FILE}")
        return

    # Charger le JSONL
    df = pd.read_json(DATA_FILE, lines=True)

    if df.empty:
        print("⚠️ Le fichier est vide.")
        return

    print("\n=== Aperçu des données ===")
    print(df.head(), "\n")

    print("=== Statistiques globales ===")
    print(f"Nombre total d'essais : {len(df)}")
    print(f"Temps moyen de réponse : {df['elapsed_sec'].mean():.2f} sec")
    print(f"Temps minimum : {df['elapsed_sec'].min():.2f} sec")
    print(f"Temps maximum : {df['elapsed_sec'].max():.2f} sec\n")

    print("=== Temps moyen par modèle ===")
    print(df.groupby("model")["elapsed_sec"].mean().round(2), "\n")

    print("=== Nombre d'essais par modèle ===")
    print(df["model"].value_counts(), "\n")

    print("=== Derniers essais ===")
    print(df.tail(5))


if __name__ == "__main__":
    main()
