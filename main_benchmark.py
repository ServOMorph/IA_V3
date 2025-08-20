# main_benchmark.py
"""
Point d'entrée pour exécuter le benchmark depuis la racine du projet :
    python main_benchmark.py
"""
import sys
from pathlib import Path

# 🔹 Ajouter la racine du projet au PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

from tools.benchmark.cli import main


if __name__ == "__main__":
    main()
