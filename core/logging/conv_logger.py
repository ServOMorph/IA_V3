import logging
from pathlib import Path
from config import LOGS_DIR, ENABLE_LOGS

def setup_conv_logger(session_name: str, log_dir=LOGS_DIR):
    conv_logger = logging.getLogger(f"conversation_{session_name}")
    conv_logger.setLevel(logging.INFO)
    conv_logger.propagate = False

    if not conv_logger.handlers and ENABLE_LOGS:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        log_file = Path(log_dir) / f"{session_name}.log"
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        fh.setFormatter(formatter)
        conv_logger.addHandler(fh)
        return conv_logger, log_file

    return conv_logger, None