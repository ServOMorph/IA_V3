# core/session_manager.py
from pathlib import Path
import shutil
from config import SAVE_DIR, LOGS_DIR
from core.logging.conv_logger import setup_conv_logger


class SessionManager:
    @staticmethod
    def rename_session(chat_manager, new_name: str) -> bool:
        """
        Renomme la session active via ChatManager.
        Ferme le logger avant, puis réinitialise après.
        """
        try:
            # Fermer logger actif
            if hasattr(chat_manager.client, "conv_logger"):
                for handler in list(chat_manager.client.conv_logger.handlers):
                    handler.close()
                    chat_manager.client.conv_logger.removeHandler(handler)

            ok = chat_manager.save_manager.rename_session_file(new_name)

            if ok:
                chat_manager.client.conv_logger, chat_manager.client.conv_log_file = setup_conv_logger(new_name)

            return ok
        except Exception as e:
            print(f"[ERREUR RENAME] {e}")
            return False

    @staticmethod
    def delete_session(chat_manager, name: str) -> bool:
        """
        Supprime une session et son log.
        Si la session active est supprimée, recrée une session vide.
        """
        try:
            session_dir = Path(SAVE_DIR) / name
            log_file = Path(LOGS_DIR) / f"{name}.log"

            # Fermer logger si c'est la session active
            if chat_manager.save_manager.session_name == name and hasattr(chat_manager.client, "conv_logger"):
                for handler in list(chat_manager.client.conv_logger.handlers):
                    handler.close()
                    chat_manager.client.conv_logger.removeHandler(handler)

            # Supprimer le dossier
            if session_dir.exists():
                shutil.rmtree(session_dir)

            # Supprimer le log
            if log_file.exists():
                log_file.unlink()

            # Si c'était la session active → recréer une session vide
            if chat_manager.save_manager.session_name == name:
                chat_manager.__init__()  # reset complet

            return True
        except Exception as e:
            print(f"[ERREUR DELETE] {e}")
            return False

    @staticmethod
    def load_session(chat_manager, name: str) -> bool:
        """
        Recharge une session existante dans ChatManager.
        Met à jour save_manager, client.history, summarizer et logger.
        Réinjecte aussi les fichiers annexes (.py, .txt, .csv, .pdf, etc.)
        afin qu'ils soient accessibles dans l'historique.
        """
        from core.sav_manager import SaveManager
        from core.logging.conv_logger import setup_conv_logger
        from core.summarizer import Summarizer

        try:
            # Utiliser le save_root déjà configuré dans ChatManager
            save_root = chat_manager.save_manager.save_root
            session_dir = save_root / name
            md_file = session_dir / "conversation.md"

            if not md_file.exists():
                print(f"[ERREUR LOAD] conversation.md introuvable pour {name}")
                return False

            # Lire et parser conversation.md
            sm = SaveManager(save_dir=save_root)
            md_text = md_file.read_text(encoding="utf-8")
            history = sm.parse_md_to_history(md_text)

            # Réassigner ChatManager
            chat_manager.save_manager.session_dir = session_dir
            chat_manager.save_manager.session_md = md_file
            chat_manager.save_manager.session_name = name
            chat_manager.client.history = history

            # Résumé
            chat_manager.summarizer = Summarizer(session_dir)

            # Logger
            chat_manager.client.conv_logger, chat_manager.client.conv_log_file = setup_conv_logger(name)

            # Réinjecter les fichiers sauvegardés (code, txt, pdf, csv…)
            for file in session_dir.iterdir():
                if file.name in {"conversation.md", "summary.md"}:
                    continue
                if file.is_file() and file.suffix.lower() in {".py", ".txt", ".csv", ".pdf"}:
                    try:
                        content = file.read_text(encoding="utf-8", errors="ignore")
                        chat_manager.client.history.append({
                            "role": "assistant",
                            "content": f"[Fichier {file.name}]\n\n{content}"
                        })
                    except Exception as e:
                        print(f"[WARN] Impossible de réinjecter {file.name}: {e}")

            return True
        except Exception as e:
            print(f"[ERREUR LOAD] {e}")
            return False
