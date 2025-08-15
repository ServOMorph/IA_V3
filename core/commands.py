# core/commands.py
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path
from typing import Tuple, List

from config import (
    PRESET_MESSAGES,
    EXIT_SAVE_MESSAGE,
    EXIT_NO_SAVE_MESSAGE,
    SAVE_DIR,
    LOGS_DIR,
)
from core.logging.conv_logger import setup_conv_logger


COMMANDS = {
    "/q": "Sauvegarder et quitter",
    "/exit": "Quitter sans sauvegarder",
    "/help": "Liste des commandes",
    "/rename": "Renommer la session courante (/rename NOM)",
    "/msg1": "Demander : capitale de la France",
    "/msg2": "Demander : histoire 20 caractères",
    "/load": "Charger une session (/load chemin/nom)",
    "/suppr": "Supprimer une session et son log (/suppr chemin/nom)",
    "/new": "Démarrer une nouvelle session",
    "/copie_ia": "Copier la dernière réponse IA",
    "/copie_user": "Copier le dernier message utilisateur",
    "/createfolder": "Créer dossiers /sav et /logs (/createfolder NOM)",
    "/move": "Déplacer une session (/move NOM dossier_cible)",
    "/savecode": "Extraire le code de la dernière réponse IA (/savecode [base])",
}


def show_commands() -> None:
    print("\n📜 Commandes disponibles :")
    for cmd, desc in COMMANDS.items():
        print(f"{cmd:<15} → {desc}")
    print()


class CommandHandler:
    """Gère l'exécution des commandes côté chat."""

    def __init__(self, chat_manager):
        self.chat_manager = chat_manager
        self.save_manager = chat_manager.save_manager
        self.client = chat_manager.client

    @staticmethod
    def is_command(text: str) -> bool:
        return text.startswith("/")

    def handle(self, user_input: str) -> Tuple[bool, bool]:
        raw = user_input.strip()
        lower = raw.lower()
        parts = raw.split(" ", 1)
        arg = parts[1].strip() if len(parts) == 2 else ""

        # 1) Sortie
        if lower == "/q":
            try:
                self.save_manager.save_md(self.client.history)
            except Exception:
                pass
            print(EXIT_SAVE_MESSAGE)
            return True, True

        if lower in {"/exit", "exit", "quit"}:
            print(EXIT_NO_SAVE_MESSAGE)
            return True, True

        # 2) Aide
        if lower == "/help":
            show_commands()
            return True, False

        # 3) Renommer la session courante
        if lower.startswith("/rename"):
            if not arg:
                print("⚠️ Usage : /rename NOM")
                return True, False

            new_name = arg.replace(" ", "_")

            # Libérer le .log sous Windows
            try:
                if getattr(self.client, "conv_logger", None):
                    for h in list(self.client.conv_logger.handlers):
                        try:
                            h.flush()
                            h.close()
                        except Exception:
                            pass
                        self.client.conv_logger.removeHandler(h)
            except Exception:
                pass

            ok = self.save_manager.rename_session_file(new_name)
            if ok:
                # Reconfigurer le logger
                self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(new_name)
                print(f"✅ Conversation renommée en : {new_name}")
            else:
                print("⚠️ Impossible de renommer la conversation.")
            return True, False

        # 4) Messages pré-enregistrés
        if lower == "/msg1":
            answer = self.client.send_prompt(PRESET_MESSAGES["msg1"])
            print(f"🤖 Ollama : {answer}")
            self.save_manager.save_md(self.client.history)
            self.save_manager.save_python_from_response(answer)
            return True, False

        if lower == "/msg2":
            answer = self.client.send_prompt(PRESET_MESSAGES["msg2"])
            print(f"🤖 Ollama : {answer}")
            self.save_manager.save_md(self.client.history)
            self.save_manager.save_python_from_response(answer)
            return True, False

        # 5) Charger une session
        if lower.startswith("/load"):
            if not arg:
                print("⚠️ Usage : /load chemin/nom")
                return True, False

            target_dir = Path(SAVE_DIR) / arg
            md_path = target_dir / "conversation.md"
            if not md_path.exists():
                print(f"⚠️ Introuvable : {md_path}")
                return True, False

            # Repointer le SaveManager
            self.save_manager.session_dir = target_dir
            self.save_manager.session_md = md_path
            self.save_manager.session_name = target_dir.name

            # Reconfigurer le logger (supporte sous-dossiers)
            session_key = str(Path(arg))  # ex: "audit/test_cli"
            self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(session_key)

            try:
                print("\n📂 Conversation chargée :\n")
                print(md_path.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"⚠️ Erreur de lecture : {e}")
            return True, False

        # 6) Supprimer une session
        if lower.startswith("/suppr"):
            if not arg:
                print("⚠️ Usage : /suppr chemin/nom")
                return True, False

            target_dir = Path(SAVE_DIR) / arg
            log_file = Path(LOGS_DIR) / f"{arg}.log"

            # Déterminer si c'est la session active
            is_current = getattr(self.save_manager, "session_dir", None) and self.save_manager.session_dir.resolve() == target_dir.resolve()

            # Fermer le logger si c'est la session active
            if is_current and getattr(self.client, "conv_logger", None):
                for h in list(self.client.conv_logger.handlers):
                    try:
                        h.flush()
                        h.close()
                    except Exception:
                        pass
                    self.client.conv_logger.removeHandler(h)

            deleted = False
            if target_dir.exists():
                try:
                    shutil.rmtree(target_dir)
                    deleted = True
                except Exception as e:
                    print(f"⚠️ Impossible de supprimer le dossier : {e}")

            if log_file.exists():
                try:
                    log_file.unlink()
                    deleted = True
                except Exception as e:
                    print(f"⚠️ Impossible de supprimer le log : {e}")

            if deleted:
                print(f"🗑️ Session '{arg}' supprimée.")

                # Si c'était la session active, réinitialiser vers une nouvelle session vide
                if is_current:
                    from core.sav_manager import SaveManager
                    from core.ollama_client import OllamaClient
                    self.chat_manager.save_manager = SaveManager(save_dir=Path(SAVE_DIR))
                    self.save_manager = self.chat_manager.save_manager
                    self.chat_manager.client = OllamaClient(model=self.client.model, session_file=self.save_manager.session_md)
                    self.client = self.chat_manager.client
                    self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(self.save_manager.session_dir.name)
                    print("ℹ️ Nouvelle session vide créée car la session active a été supprimée.")

            else:
                print("⚠️ Rien à supprimer.")
            return True, False

        # 7) Nouvelle session
        if lower == "/new":
            # Fermer le logger courant
            if getattr(self.client, "conv_logger", None):
                for h in list(self.client.conv_logger.handlers):
                    try:
                        h.flush()
                        h.close()
                    except Exception:
                        pass
                    self.client.conv_logger.removeHandler(h)

            # Réinitialiser via ChatManager (nouveau dossier)
            self.chat_manager.save_manager = self.save_manager.__class__(save_dir=Path(SAVE_DIR))
            self.chat_manager.client = self.client.__class__(
                model=self.client.model,
                session_file=self.chat_manager.save_manager.session_md
            )
            # Rebind locaux
            self.save_manager = self.chat_manager.save_manager
            self.client = self.chat_manager.client

            # Logger
            self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(self.save_manager.session_dir.name)

            # Créer conversation.md
            if not self.save_manager.session_md.exists():
                self.save_manager.session_md.write_text("", encoding="utf-8")

            print(f"🆕 Nouvelle session : {self.save_manager.session_dir.name}")
            return True, False

        # 8) Copier presse-papier
        if lower == "/copie_ia":
            import pyperclip
            if not self.client.history:
                print("⚠️ Aucune réponse IA.")
                return True, False
            content = self.client.history[-1].get("response", "").strip()
            if not content:
                print("⚠️ Réponse IA vide.")
                return True, False
            pyperclip.copy(content)
            print("📋 Dernière réponse IA copiée.")
            return True, False

        if lower == "/copie_user":
            import pyperclip
            if not self.client.history:
                print("⚠️ Aucun message utilisateur.")
                return True, False
            content = self.client.history[-1].get("prompt", "").strip()
            if not content:
                print("⚠️ Message utilisateur vide.")
                return True, False
            pyperclip.copy(content)
            print("📋 Dernier message utilisateur copié.")
            return True, False

        # 9) Créer un dossier d’organisation
        if lower.startswith("/createfolder"):
            if not arg:
                print("⚠️ Usage : /createfolder NOM")
                return True, False
            safe = arg.replace(" ", "_")
            (Path(SAVE_DIR) / safe).mkdir(parents=True, exist_ok=True)
            (Path(LOGS_DIR) / safe).mkdir(parents=True, exist_ok=True)
            print(f"✅ Dossier '{safe}' créé dans /sav et /logs")
            return True, False

        # 10) Déplacer une session vers un dossier
        if lower.startswith("/move"):
            if not arg:
                print("⚠️ Usage : /move NOM dossier_cible")
                return True, False
            try:
                conv_name, folder_name = arg.split(maxsplit=1)
            except ValueError:
                print("⚠️ Usage : /move NOM dossier_cible")
                return True, False

            safe_folder = folder_name.strip().replace(" ", "_")
            src_sav_dir = Path(SAVE_DIR) / conv_name
            dst_sav_parent = Path(SAVE_DIR) / safe_folder
            dst_sav_parent.mkdir(parents=True, exist_ok=True)
            dst_sav_dir = dst_sav_parent / conv_name

            src_log = Path(LOGS_DIR) / f"{conv_name}.log"
            dst_logs_parent = Path(LOGS_DIR) / safe_folder
            dst_logs_parent.mkdir(parents=True, exist_ok=True)
            dst_log = dst_logs_parent / f"{conv_name}.log"

            if not src_sav_dir.exists():
                print(f"⚠️ Introuvable : {src_sav_dir}")
                return True, False

            # Si c'est la session courante, fermer le logger
            is_current = getattr(self.save_manager, "session_dir", None) and self.save_manager.session_dir.resolve() == src_sav_dir.resolve()
            if is_current and getattr(self.client, "conv_logger", None):
                for h in list(self.client.conv_logger.handlers):
                    try:
                        h.flush()
                        h.close()
                    except Exception:
                        pass
                    self.client.conv_logger.removeHandler(h)

            # Déplacer dossier sav
            try:
                shutil.move(str(src_sav_dir), str(dst_sav_dir))
            except Exception as e:
                print(f"❌ Erreur déplacement dossier : {e}")
                return True, False

            # Déplacer log si présent
            if src_log.exists():
                try:
                    shutil.move(str(src_log), str(dst_log))
                except Exception as e:
                    print(f"❌ Erreur déplacement log : {e}")

            # Mettre à jour pointeurs si courant
            if is_current:
                self.save_manager.session_dir = dst_sav_dir
                self.save_manager.session_md = dst_sav_dir / "conversation.md"
                self.save_manager.session_name = dst_sav_dir.name
                # Logger sur logs/<folder>/<conv>.log
                session_key = f"{safe_folder}/{conv_name}"
                self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(session_key)

            print(f"✅ Conversation '{conv_name}' déplacée vers '{safe_folder}'")
            return True, False

        # 11) Extraire code depuis la dernière réponse IA
        if lower.startswith("/savecode"):
            base = arg.replace(" ", "_") if arg else ""
            if not self.client.history:
                print("⚠️ Aucune réponse IA disponible.")
                return True, False
            answer = self.client.history[-1].get("response", "")
            blocks = self._extract_python_blocks(answer)
            if not blocks:
                print("ℹ️ Aucun bloc ```python``` détecté.")
                return True, False

            created: List[Path] = []
            session_dir: Path = self.save_manager.session_dir
            session_dir.mkdir(parents=True, exist_ok=True)

            if base:
                # si plusieurs blocs, suffix _1, _2...
                for idx, code in enumerate(blocks, start=1):
                    name = f"{base}.py" if len(blocks) == 1 else f"{base}_{idx}.py"
                    out = session_dir / name
                    out.write_text(code, encoding="utf-8")
                    created.append(out)
            else:
                from datetime import datetime
                for idx, code in enumerate(blocks, start=1):
                    ts = datetime.now().strftime("%H-%M-%S")
                    name = f"code_{ts}.py" if len(blocks) == 1 else f"code_{ts}_{idx}.py"
                    out = session_dir / name
                    out.write_text(code, encoding="utf-8")
                    created.append(out)

            print("✅ Fichier(s) créé(s) :")
            for p in created:
                print(f" - {p.as_posix()}")
            return True, False

        # Rien traité
        return False, False

    # --- Utils ---

    @staticmethod
    def _extract_python_blocks(text: str) -> List[str]:
        """
        Extrait les blocs ```python ... ``` ou ``` ... ``` du texte.
        Retourne une liste de codes Python.
        """
        if not text:
            return []
        # blocs marqués python
        pat_py = re.compile(r"```python\s+?(.*?)```", re.DOTALL | re.IGNORECASE)
        # blocs génériques
        pat_any = re.compile(r"```\s*?(.*?)```", re.DOTALL)

        blocks = [m.group(1).strip() for m in pat_py.finditer(text)]
        if not blocks:
            # fallback: blocs non typés
            blocks = [m.group(1).strip() for m in pat_any.finditer(text)]
        # nettoyer éventuels ``` résiduels
        return [b.replace("\r\n", "\n").strip() for b in blocks if b.strip()]
