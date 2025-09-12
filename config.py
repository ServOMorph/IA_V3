# config.py
# =============================
# Fichier centralisant toutes les constantes du projet
# =============================

from pathlib import Path

# Mode développeur
DEV_MODE = False  # ou False

# Répertoire des métadonnées (non lié aux conversations)
DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)



# Modèle IA par défaut
DEFAULT_MODEL = "gemma2-2b-it-q4"

# Répertoire de sauvegarde
SAVE_DIR = "sav"

# Messages pré-enregistrés
PRESET_MESSAGES = {
    "msg1": "Quelle est la capitale de la France ?",
    "msg2": "Raconte moi une histoire en 20 caractères sur la ville dont tu viens de parler"
}

# Messages système
WELCOME_MESSAGE = "💬 Session de chat démarrée (tapez /help pour voir les commandes)"
EXIT_SAVE_MESSAGE = "✅ Conversation sauvegardée et session terminée."
EXIT_NO_SAVE_MESSAGE = "🚪 Session terminée sans sauvegarde supplémentaire."
EMPTY_PROMPT_WARNING = "⚠️ Prompt vide, veuillez entrer un texte."

# Dossier de logs de conversation
LOGS_DIR = "logs"

# Fichier de log principal
DEBUG_LOG_FILE = "debug.log"


# Adresse du serveur Ollama
OLLAMA_BASE_URL = "http://localhost:11434"

# Timeout en secondes pour la requête à Ollama
OLLAMA_TIMEOUT = 3600

# Dossier des sauvegardes
SAVE_DIR = "sav"

# Modèle de nom de fichier de sauvegarde
SAVE_FILE_PREFIX = "sav_conv_"
SAVE_FILE_DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"

# Dossier des logs (pour renommage des fichiers associés)
LOGS_DIR = "logs"

DEFAULT_SYSTEM_PROMPT = """
Ecris en Français
"""

# Limite de tokens générés par l'IA
# Conseils :
# - CHAT_RAPIDE : 100 → réponses très courtes (1–2 phrases, ultra rapide)
# - CHAT_STANDARD : 200 → réponses moyennes (3–5 phrases, bon compromis)
# - RESUME : 300–400 → résumés structurés
# - REDACTION : 500–800 → texte long, plus lent
MAX_TOKENS = 200  # valeur par défaut

# Résumé automatique
MAX_HISTORY_MESSAGES = 3   # seuil d'anciens échanges avant résumé
USE_SUMMARY = True         # activer/désactiver le mécanisme de résumé
SUMMARY_MODEL = "gemma2:2b"  # modèle choisi pour résumer l'historique
SUMMARY_MAX_TOKENS = 150   # taille maximale du résumé généré


