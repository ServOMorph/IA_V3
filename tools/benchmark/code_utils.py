# tools/benchmark/code_utils.py
"""
Utilitaires pour extraire et évaluer le code Python généré par l'IA
"""
import tempfile
from pathlib import Path
import importlib.util


def extract_code_blocks(text: str) -> str:
    """
    Extrait le premier vrai bloc de code Python.
    - Cherche en priorité un bloc délimité par ```python ... ```.
    - Si aucun n'est trouvé, retourne une chaîne vide (plutôt que du texte hors code).
    """
    if not text or "```" not in text:
        return ""

    parts = text.split("```")
    for part in parts:
        stripped = part.strip()
        if stripped.startswith("python"):
            return stripped[len("python"):].strip()

    return ""


def evaluate_code(code: str, func_name: str, tests: dict) -> tuple[int, int]:
    """Exécute le code IA et teste la fonction demandée."""
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


def count_code_lines(code: str) -> int:
    """
    Compte le nombre de lignes dans un code Python généré.
    Utile pour évaluer la capacité des modèles à produire du code long (ex. ~200 lignes).
    """
    return len([line for line in code.splitlines() if line.strip()])
