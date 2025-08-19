# main.py
from core.chat_manager import ChatManager
from core.ollama_client import list_installed_models
from config import DEV_MODE, DEFAULT_MODEL


def select_model():
    """Affiche les modèles installés et demande à l'utilisateur lequel utiliser."""
    models_output = list_installed_models()
    if not models_output:
        return DEFAULT_MODEL

    # Split lignes, ignorer l'entête "NAME ..."
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


def main():
    # Mode dev : choisir un modèle au démarrage
    if DEV_MODE:
        model = select_model()
    else:
        model = DEFAULT_MODEL

    # Lancer le chat avec le modèle choisi
    chat = ChatManager(model=model)
    chat.start_chat()


if __name__ == "__main__":
    main()
