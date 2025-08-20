# tools/benchmark/config_benchmark.py
"""
Config spécifique au module benchmark
"""

from pathlib import Path

# Répertoire des données
DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Modèle par défaut
DEFAULT_MODEL = "mistral"
