# config.py
# =============================
# Fichier centralisant toutes les constantes du projet
# =============================

# Modèle IA par défaut
DEFAULT_MODEL = "mistral"

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

DEFAULT_SYSTEM_PROMPT = """\
Explique en une phrase ce qu’est un itérateur en Python. Ne fournis aucun code."""



