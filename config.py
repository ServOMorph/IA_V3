# config.py
# =============================
# Fichier centralisant toutes les constantes du projet
# =============================

from pathlib import Path

# Mode développeur
DEV_MODE = False  # ou False

# Répertoire racine du projet (IA_V3)
BASE_DIR = Path(__file__).resolve().parent

# Répertoire des métadonnées (data)
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Répertoire de sauvegarde
SAVE_DIR = BASE_DIR / "sav"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# Répertoire des logs
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Fichier de log principal
DEBUG_LOG_FILE = BASE_DIR / "debug.log"


# Modèle IA par défaut
DEFAULT_MODEL = "gemma2-2b-it-q4"

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

# Paramètres de génération
TEMPERATURE = 0.2   # 0.0 = très déterministe, 1.0 = créatif
TOP_P = 0.9         # nucleus sampling
TOP_K = 40          # alternative sampling

# Résumé automatique
MAX_HISTORY_MESSAGES = 3   # au lieu de 3
USE_SUMMARY = True         # activer/désactiver le mécanisme de résumé
SUMMARY_MODEL = "gemma2:2b"  # modèle choisi pour résumer l'historique
SUMMARY_MAX_TOKENS = 150   # taille maximale du résumé généré

ALLOWED_FILE_TYPES_OUT = ["py", "txt", "md", "json", "csv", "docx", "pdf", "xlsx"]

