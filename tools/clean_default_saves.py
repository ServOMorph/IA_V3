#!/usr/bin/env python3
"""
Efface toutes les sauvegardes par défaut dont le nom suit le format :
sav_conv_YYYY-MM-DD_HH-MM-SS

⚠ Attention : cette action est destructive.
"""

import re
import shutil
from pathlib import Path
import sys
# Ajouter la racine du projet IA_V3 au PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from config import SAVE_DIR


# Regex qui matche le format par défaut
DEFAULT_PATTERN = re.compile(r"^sav_conv_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$")

def clean_default_saves():
    save_root = Path(SAVE_DIR)
    if not save_root.exists():
        print(f"[INFO] Le dossier de sauvegarde {save_root} n'existe pas.")
        return

    deleted = 0
    for folder in save_root.iterdir():
        if folder.is_dir() and DEFAULT_PATTERN.match(folder.name):
            print(f"[SUPPRESSION] {folder}")
            shutil.rmtree(folder)
            deleted += 1

    if deleted == 0:
        print("[INFO] Aucune sauvegarde par défaut trouvée.")
    else:
        print(f"[INFO] {deleted} dossier(s) supprimé(s).")

if __name__ == "__main__":
    clean_default_saves()
