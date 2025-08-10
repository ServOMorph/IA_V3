import logging
from pathlib import Path
from config import DEBUG_LOG_FILE

def setup_logger(log_file=DEBUG_LOG_FILE):
    """
    Configure le logger :
    - Tous les logs (DEBUG, INFO, WARNING, ERROR) → debug.log à la racine
    - Seuls WARNING, ERROR, CRITICAL → console
    """
    log_path = Path(log_file)  # Fichier directement à la racine

    # Créer le logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture tout

    # Handler pour fichier (tout)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_format)

    # Handler pour console (juste WARNING et plus)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_format = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_format)

    # Nettoyer anciens handlers et ajouter les nouveaux
    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info(f"Logger initialisé, écriture dans : {log_path.resolve()}")
