import logging
from pathlib import Path
from config import DEBUG_LOG_FILE, ENABLE_LOGS

from config import DEBUG_LOG_FILE, ENABLE_LOGS

def setup_logger(log_file=DEBUG_LOG_FILE):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Nettoyer anciens handlers
    logger.handlers.clear()

    if ENABLE_LOGS:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_format = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    if ENABLE_LOGS:
        logging.info(f"Logger initialisé, écriture dans : {Path(log_file).resolve()}")
    else:
        logging.warning("Logger fichier désactivé (ENABLE_LOGS=False)")
