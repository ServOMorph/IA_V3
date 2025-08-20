# tools/benchmark/exercises.py
"""
Définition des exercices disponibles pour tester les IA
"""

EXERCISES = {
    "is_prime": {
        "prompt": (
            "Écris uniquement le code Python complet de la fonction suivante, sans explication, "
            "au format exact :\n"
            "```python\n"
            "def is_prime(n: int) -> bool:\n"
            "    # ton code ici\n"
            "```"
        ),
        "tests": {2: True, 4: False, 17: True, 18: False, 19: True, 1: False, 97: True}
    },
    "fibonacci": {
        "prompt": (
            "Écris uniquement le code Python complet de la fonction suivante, sans explication, "
            "au format exact :\n"
            "```python\n"
            "def fibonacci(n: int) -> int:\n"
            "    # ton code ici\n"
            "```"
        ),
        "tests": {0: 0, 1: 1, 2: 1, 5: 5, 7: 13, 10: 55}
    },
    "factorial": {
        "prompt": (
            "Écris uniquement le code Python complet de la fonction suivante, sans explication, "
            "au format exact :\n"
            "```python\n"
            "def factorial(n: int) -> int:\n"
            "    # ton code ici\n"
            "```"
        ),
        "tests": {0: 1, 1: 1, 3: 6, 5: 120, 7: 5040}
    },
    "long_code_test": {
        "prompt": (
            "Écris un programme Python complet d'environ 200 lignes qui implémente "
            "un petit jeu de rôle en mode console :\n"
            "- gestion de personnages (classe, points de vie, attaque, défense)\n"
            "- inventaire simple\n"
            "- combat contre des ennemis\n"
            "- boucle principale de jeu\n"
            "Le code doit être directement exécutable, sans explication, uniquement du code.\n"
            "Encapsule tout dans un bloc formaté ```python ... ```"
        ),
        "tests": {}  # pas de tests unitaires, évaluation manuelle
    },
}
