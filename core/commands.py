COMMANDS = {
    "/q": "Sauvegarder la conversation et quitter",
    "/exit": "Quitter sans sauvegarder",
    "/help": "Afficher la liste des commandes",
    "/rename": "Renommer la conversation actuelle (/rename NOM)",
    "/msg1": "Demander à l'IA : Quelle est la capitale de la France ?",
    "/msg2": "Demander à l'IA : Raconte moi une histoire en 20 caractères sur la ville dont tu viens de parler",
    "/load": "Charger une conversation depuis le dossier /sav (/load NOM)"
}

def show_commands():
    """Affiche toutes les commandes disponibles."""
    print("\n📜 Commandes disponibles :")
    for cmd, desc in COMMANDS.items():
        print(f"{cmd:<10} → {desc}")
    print()
