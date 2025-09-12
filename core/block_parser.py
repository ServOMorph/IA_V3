# core/block_parser.py
import re
from typing import List

def extract_code_blocks(text: str) -> List[str]:
    """
    Extrait tous les blocs délimités par ```...``` dans un texte.
    Retourne une liste de contenus nettoyés (sans balises).
    """
    if not text:
        return []
    pattern = re.compile(r"```[a-zA-Z0-9]*\s*([\s\S]*?)```", re.MULTILINE)
    blocks = [m.group(1).strip() for m in pattern.finditer(text)]
    return [b for b in blocks if b]
