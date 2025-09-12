# perf_tests/test_summary_long.py
import shutil
from pathlib import Path
from core.chat_manager import ChatManager
from config import SAVE_DIR

def run_auto_test():
    # Nom de la session de test
    test_session = "test_summary_long"
    session_path = Path(SAVE_DIR) / test_session

    # Supprimer la session précédente si elle existe
    if session_path.exists():
        shutil.rmtree(session_path)
        print(f"✅ Ancienne session '{test_session}' supprimée.")

    # Créer un ChatManager
    chat = ChatManager()
    chat.save_manager.session_dir = session_path
    chat.save_manager.session_dir.mkdir(parents=True, exist_ok=True)

    # Séquence de prompts pour forcer plusieurs résumés
    prompts = [
        "Bonjour",
        "Explique-moi un proverbe français",
        "Donne un exemple",
        "Résume en 3 mots",
        "Continue",
        "Ajoute un autre proverbe",
        "Encore un autre",
        "Donne une citation célèbre",
        "Explique cette citation",
        "Fais une analogie avec la nature",
        "Donne un synonyme de 'rapide'",
        "Écris une phrase avec ce synonyme",
        "Explique une règle de grammaire française",
        "Propose un exercice pratique",
        "Corrige cette phrase : 'Je aller au marché hier'",
    ]

    for i, p in enumerate(prompts, 1):
        print(f"\n=== Prompt {i} : {p} ===")
        answer = chat.client.send_prompt(p)
        print(f"🤖 Réponse : {answer[:300]}{'...' if len(answer) > 300 else ''}")

        # Déclenche résumé si dépasse seuil (exemple : 5)
        if len(chat.client.history) > 5:
            old_messages = chat.client.history[:-5]
            summary = chat.summarizer.generate_summary(old_messages)
            chat.client.history = (
                [{"role": "system", "content": summary}]
                + chat.client.history[-5:]
            )
            print("\n--- Résumé généré ---")
            print(summary[:400], "..." if len(summary) > 400 else "")

        # Sauvegardes
        chat.save_manager.save_md(chat.client.history)
        chat.save_manager.save_python_from_response(answer)
        chat.save_manager.save_txt_from_response(answer)

    # Afficher le résumé final
    print("\n=== Contenu final de summary.md ===")
    try:
        print(chat.summarizer.load_summary())
    except Exception as e:
        print("Pas de résumé généré :", e)

if __name__ == "__main__":
    run_auto_test()
