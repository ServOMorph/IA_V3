import sys
from pathlib import Path
import shutil

# Ajouter la racine du projet au path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from core.chat_manager import ChatManager
from config import SAVE_DIR, MAX_HISTORY_MESSAGES


def run_complex_summary_test():
    """
    Test complexe : enchaîne 20 questions avec logique et dépendances
    pour vérifier la cohérence et la persistance dans les résumés.
    """
    # Nettoyer dossier de sauvegarde pour repartir propre
    if Path(SAVE_DIR).exists():
        shutil.rmtree(SAVE_DIR)
    Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)

    chat = ChatManager()

    # Suite de 20 questions complexes avec logique
    questions = [
        # Bloc 1 – Physique quantique
        "Explique-moi les bases de la physique quantique en 3 phrases.",
        "Résume cette explication en une seule phrase.",
        "Donne un exemple concret d’application de la physique quantique.",
        "Garde cet exemple en mémoire, on y reviendra plus tard.",

        # Bloc 2 – Logique mathématique
        "Écris un petit code Python qui calcule si un nombre est premier.",
        "Ajoute une explication ligne par ligne de ton code.",
        "Corrige ton code si j’entre le nombre 1 (cas limite).",
        "Résume en une phrase l’évolution de ton code depuis la version initiale.",

        # Bloc 3 – Enchaînement narratif
        "Raconte une courte histoire de science-fiction où la physique quantique est utilisée.",
        "Résume cette histoire en 2 phrases.",
        "Ajoute un nouveau personnage à cette histoire.",
        "Résume l’histoire en incluant ce nouveau personnage.",

        # Bloc 4 – Persistance mémoire
        "Rappelle-moi l’exemple concret de physique quantique que tu avais donné plus tôt.",
        "Intègre cet exemple dans l’histoire précédente.",
        "Fais un résumé de l’histoire avec le personnage et l’exemple intégré.",

        # Bloc 5 – Consolidation logique
        "Donne une liste des thèmes qu’on a abordés depuis le début de cette conversation.",
        "Organise cette liste par catégories (science, code, fiction).",
        "Mets en évidence les points en suspens qu’on pourrait explorer plus tard.",
        "Propose une conclusion qui relie toutes ces parties.",
        "Résume toute cette conversation en un seul paragraphe."
    ]

    print("=== Lancement du test complexe de résumé ===\n")

    for i, q in enumerate(questions, start=1):
        print(f"[{i}] Vous : {q}")
        answer = chat.client.send_prompt(q)
        print(f"[{i}] IA : {answer[:120]}...\n")  # affiche seulement 120 premiers caractères

        # --- Déclenche résumé glissant + global ---
        if len(chat.client.history) > MAX_HISTORY_MESSAGES:
            old_chunk = chat.client.history[:2]
            remaining = chat.client.history[2:]
            summary, idx = chat.summarizer.generate_summary(old_chunk)
            chat.client.history = (
                [{"role": "system", "content": f"[Résumé partiel #{idx}] {summary}"}]
                + remaining
            )
            if idx % 3 == 0:  # GLOBAL_TRIGGER = 3
                global_summary, _ = chat.summarizer.generate_global_summary()
                chat.client.history = (
                    [{"role": "system", "content": f"[Résumé global] {global_summary}"}]
                    + chat.client.history[-MAX_HISTORY_MESSAGES:]
                )

        # --- Sauvegarde conversation et fichiers ---
        chat.save_manager.save_md(chat.client.history)
        chat.save_manager.save_python_from_response(answer)
        chat.save_manager.save_txt_from_response(answer)

    # Afficher chemins de sortie
    session_dir = Path(chat.save_manager.session_dir)
    print("\n=== Test terminé ===")
    print(f"Conversation enregistrée dans : {session_dir / 'conversation.md'}")
    print(f"Résumés enregistrés dans : {session_dir / 'summary.md'}")


if __name__ == "__main__":
    run_complex_summary_test()
