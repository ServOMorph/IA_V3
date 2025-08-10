import logging
from pathlib import Path
from config import LOGS_DIR

def setup_conv_logger(session_name: str, log_dir=LOGS_DIR):
    """
    Configure un logger dédié à la conversation IA.
    Le fichier .log porte le même nom que la sauvegarde .txt.
    """
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    log_file = Path(log_dir) / f"{session_name}.log"

    conv_logger = logging.getLogger(f"conversation_{session_name}")
    conv_logger.setLevel(logging.INFO)
    conv_logger.propagate = False  # Pas de propagation vers le logger global

    # Évite les doublons de handlers
    if not conv_logger.handlers:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        fh.setFormatter(formatter)
        conv_logger.addHandler(fh)

    return conv_logger, log_file
