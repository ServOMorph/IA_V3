import logging
from pathlib import Path
from datetime import datetime
import shutil
from config import SAVE_DIR, SAVE_FILE_PREFIX, SAVE_FILE_DATETIME_FORMAT, LOGS_DIR

class SaveManager:
    """
    Sauvegarde les conversations dans un fichier dédié à la session.
    """
    def __init__(self, save_dir=SAVE_DIR):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.session_file = self.save_dir / f"{SAVE_FILE_PREFIX}{datetime.now().strftime(SAVE_FILE_DATETIME_FORMAT)}.txt"

    def save_txt(self, history):
        """Sauvegarde ou met à jour l'historique complet dans le fichier de session."""
        try:
            with open(self.session_file, "w", encoding="utf-8") as f:
                for exchange in history:
                    prompt = exchange.get("prompt", "")
                    response = exchange.get("response", "")
                    timestamp = exchange.get("timestamp", "")
                    f.write(f"--- {timestamp} ---\n")
                    f.write(f"👤 Vous : {prompt}\n")
                    f.write(f"🤖 Ollama : {response}\n\n")
            logging.info(f"Historique mis à jour : {self.session_file.resolve()}")
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde TXT : {e}")

    def rename_session_file(self, new_name):
        """
        Renomme le fichier de sauvegarde actuel (.txt) et son .log associé.
        Retourne True si réussi, False sinon.
        """
        try:
            new_txt_file = self.save_dir / f"{new_name}.txt"
            if new_txt_file.exists():
                logging.error(f"Le fichier '{new_txt_file.name}' existe déjà. Renommage annulé.")
                return False

            # Fermer le logger de conversation avant de renommer
            conv_logger = logging.getLogger(f"conversation_{self.session_file.stem}")
            for handler in conv_logger.handlers[:]:
                handler.close()
                conv_logger.removeHandler(handler)

            # Renommer le fichier .txt
            old_txt_file = self.session_file
            shutil.move(str(old_txt_file), str(new_txt_file))

            # Renommer le fichier .log correspondant s'il existe
            old_log_file = Path(LOGS_DIR) / f"{old_txt_file.stem}.log"
            if old_log_file.exists():
                new_log_file = Path(LOGS_DIR) / f"{new_name}.log"
                shutil.move(str(old_log_file), str(new_log_file))
                logging.info(f"Fichier log renommé : {new_log_file.resolve()}")

            # Mise à jour interne
            self.session_file = new_txt_file
            logging.info(f"Conversation renommée : {self.session_file.resolve()}")
            return True

        except Exception as e:
            logging.error(f"Erreur lors du renommage : {e}")
            return False

    def load_session_file(self, name):
        """Charge une conversation sauvegardée depuis un fichier TXT."""
        file_path = self.save_dir / f"{name}.txt"
        if not file_path.exists():
            logging.error(f"Le fichier '{file_path.name}' n'existe pas.")
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logging.error(f"Erreur lors du chargement : {e}")
            return None
