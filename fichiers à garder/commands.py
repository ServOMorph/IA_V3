from __future__ import annotations

import re
from pathlib import Path
from typing import Tuple, List
from core import session_manager

from config import (
    PRESET_MESSAGES,
    EXIT_SAVE_MESSAGE,
    EXIT_NO_SAVE_MESSAGE,
)
from core.logging.conv_logger import setup_conv_logger
from core.session_manager import SessionManager

# --- Préfixe configurable ---
COMMAND_PREFIX = "&"

COMMANDS = {
    f"{COMMAND_PREFIX}q": "Sauvegarder et quitter",
    f"{COMMAND_PREFIX}exit": "Quitter sans sauvegarder",
    f"{COMMAND_PREFIX}help": "Liste des commandes",
    f"{COMMAND_PREFIX}rename": f"Renommer la session courante ({COMMAND_PREFIX}rename NOM)",
    f"{COMMAND_PREFIX}msg1": "Demander : capitale de la France",
    f"{COMMAND_PREFIX}msg2": "Demander : histoire 20 caractères",
    f"{COMMAND_PREFIX}load": f"Charger une session ({COMMAND_PREFIX}load chemin/nom)",
    f"{COMMAND_PREFIX}suppr": f"Supprimer une session et son log ({COMMAND_PREFIX}suppr chemin/nom)",
    f"{COMMAND_PREFIX}new": "Démarrer une nouvelle session",
    f"{COMMAND_PREFIX}copie_ia": "Copier la dernière réponse IA",
    f"{COMMAND_PREFIX}copie_user": "Copier le dernier message utilisateur",
    f"{COMMAND_PREFIX}createfolder": f"Créer dossiers /sav et /logs ({COMMAND_PREFIX}createfolder NOM)",
    f"{COMMAND_PREFIX}move": f"Déplacer une session ({COMMAND_PREFIX}move NOM dossier_cible)",
    f"{COMMAND_PREFIX}savecode": f"Extraire le code de la dernière réponse IA ({COMMAND_PREFIX}savecode [base])",
    f"{COMMAND_PREFIX}savetxt": f"Extraire le texte de la dernière réponse IA ({COMMAND_PREFIX}savetxt [base])",
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
        return text.startswith(COMMAND_PREFIX)

    def handle(self, user_input: str) -> Tuple[bool, bool]:
        raw = user_input.strip()
        lower = raw.lower()
        parts = raw.split(" ", 1)
        arg = parts[1].strip() if len(parts) == 2 else ""

        # --- Sessions (via session_manager) ---

        if lower.startswith(f"{COMMAND_PREFIX}rename"):
            if not arg:
                print("Usage: &rename NOUVEAU_NOM")
                return True, False
            ok = session_manager.rename_session(self.save_manager, arg)
            print("✅ Conversation renommée." if ok else "⚠️ Échec du renommage.")
            return True, False

        if lower.startswith(f"{COMMAND_PREFIX}suppr"):
            if not arg:
                print("Usage: &suppr NOM")
                return True, False
            ok, new_session = session_manager.delete_session(self.save_manager, arg)
            if ok:
                print("✅ Conversation supprimée.")
                if new_session:
                    # C'était la session active → rebind
                    self.chat_manager.save_manager = new_session
                    self.save_manager = new_session
                    self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(
                        new_session.session_dir.name
                    )
                    print("ℹ️ Nouvelle session vide créée.")
            else:
                print("⚠️ Échec de la suppression.")
            return True, False

        if lower.startswith(f"{COMMAND_PREFIX}load"):
            if not arg:
                print("Usage: &load NOM")
                return True, False
            sm = session_manager.load_session(arg)
            if sm is None:
                print("⚠️ Session introuvable.")
                return True, False
            # Rebind ChatManager sur le nouveau SaveManager
            self.chat_manager.save_manager = sm
            self.save_manager = sm
            # Reconfigurer le logger de conversation
            self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(sm.session_dir.name)
            print(f"✅ Session chargée: {arg}")
            return True, False

        if lower == f"{COMMAND_PREFIX}new":
            sm = session_manager.new_session()
            self.chat_manager.save_manager = sm
            self.save_manager = sm
            self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(sm.session_dir.name)
            print("✅ Nouvelle session créée.")
            return True, False

        if lower.startswith(f"{COMMAND_PREFIX}createfolder"):
            if not arg:
                print("Usage: &createfolder NOM_DOSSIER")
                return True, False
            ok = session_manager.create_folder(arg)
            print("✅ Dossier créé." if ok else "⚠️ Échec de création.")
            return True, False

        if lower.startswith(f"{COMMAND_PREFIX}move"):
            parts2 = arg.split()
            if len(parts2) != 2:
                print("Usage: &move NOM_CONV DOSSIER")
                return True, False
            conv_name, folder = parts2
            ok = session_manager.move_session(conv_name, folder)
            print("✅ Conversation déplacée." if ok else "⚠️ Échec du déplacement.")
            return True, False

        # --- Sortie ---

        if lower == f"{COMMAND_PREFIX}q":
            try:
                self.save_manager.save_md(self.client.history)
            except Exception:
                pass
            print(EXIT_SAVE_MESSAGE)
            return True, True

        if lower in {f"{COMMAND_PREFIX}exit", "exit", "quit"}:
            print(EXIT_NO_SAVE_MESSAGE)
            return True, True

        # --- Aide ---

        if lower == f"{COMMAND_PREFIX}help":
            show_commands()
            return True, False

<<<<<<< HEAD
        # 3) Renommer la session courante
        if lower.startswith(f"{COMMAND_PREFIX}rename"):
            if not arg:
                print(f"⚠️ Usage : {COMMAND_PREFIX}rename NOM")
                return True, False
            new_name = arg.replace(" ", "_")
            ok = SessionManager.rename_session(self.chat_manager, new_name)
            if ok:
                print(f"✅ Conversation renommée en : {new_name}")
            else:
                print("⚠️ Impossible de renommer la conversation.")
            return True, False
=======
        # --- Messages pré-enregistrés ---
>>>>>>> 5116532caa83a3349b98419997f4dcd8736fca1b

        if lower == f"{COMMAND_PREFIX}msg1":
            answer = self.client.send_prompt(PRESET_MESSAGES["msg1"])
            print(f"🤖 Ollama : {answer}")
            self.save_manager.save_md(self.client.history)
            self.save_manager.save_python_from_response(answer)
            return True, False

        if lower == f"{COMMAND_PREFIX}msg2":
            answer = self.client.send_prompt(PRESET_MESSAGES["msg2"])
            print(f"🤖 Ollama : {answer}")
            self.save_manager.save_md(self.client.history)
            self.save_manager.save_python_from_response(answer)
            return True, False

        # --- Copier presse-papier ---

<<<<<<< HEAD
        # 6) Supprimer une session
        if lower.startswith(f"{COMMAND_PREFIX}suppr"):
            if not arg:
                print(f"⚠️ Usage : {COMMAND_PREFIX}suppr chemin/nom")
                return True, False
            ok = SessionManager.delete_session(self.chat_manager, arg)
            if ok:
                print(f"🗑️ Session '{arg}' supprimée.")
            else:
                print("⚠️ Rien à supprimer ou erreur.")
            return True, False

        # 7) Nouvelle session
        if lower == f"{COMMAND_PREFIX}new":
            if getattr(self.client, "conv_logger", None):
                for h in list(self.client.conv_logger.handlers):
                    try:
                        h.flush()
                        h.close()
                    except Exception:
                        pass
                    self.client.conv_logger.removeHandler(h)
            self.chat_manager.save_manager = self.save_manager.__class__(save_dir=Path(SAVE_DIR))
            self.chat_manager.client = self.client.__class__(model=self.client.model, session_file=self.chat_manager.save_manager.session_md)
            self.save_manager = self.chat_manager.save_manager
            self.client = self.chat_manager.client
            self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(self.save_manager.session_dir.name)
            if not self.save_manager.session_md.exists():
                self.save_manager.session_md.write_text("", encoding="utf-8")
            print(f"🆕 Nouvelle session : {self.save_manager.session_dir.name}")
            return True, False

        # 8) Copier presse-papier
=======
>>>>>>> 5116532caa83a3349b98419997f4dcd8736fca1b
        if lower == f"{COMMAND_PREFIX}copie_ia":
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

        if lower == f"{COMMAND_PREFIX}copie_user":
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

        # --- Sauvegarde code ---

<<<<<<< HEAD
        # 10) Déplacer une session
        if lower.startswith(f"{COMMAND_PREFIX}move"):
            if not arg:
                print(f"⚠️ Usage : {COMMAND_PREFIX}move NOM dossier_cible")
                return True, False
            try:
                conv_name, folder_name = arg.split(maxsplit=1)
            except ValueError:
                print(f"⚠️ Usage : {COMMAND_PREFIX}move NOM dossier_cible")
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
            is_current = getattr(self.save_manager, "session_dir", None) and self.save_manager.session_dir.resolve() == src_sav_dir.resolve()
            if is_current and getattr(self.client, "conv_logger", None):
                for h in list(self.client.conv_logger.handlers):
                    try:
                        h.flush()
                        h.close()
                    except Exception:
                        pass
                    self.client.conv_logger.removeHandler(h)
            try:
                import shutil
                shutil.move(str(src_sav_dir), str(dst_sav_dir))
            except Exception as e:
                print(f"❌ Erreur déplacement dossier : {e}")
                return True, False
            if src_log.exists():
                try:
                    shutil.move(str(src_log), str(dst_log))
                except Exception as e:
                    print(f"❌ Erreur déplacement log : {e}")
            if is_current:
                self.save_manager.session_dir = dst_sav_dir
                self.save_manager.session_md = dst_sav_dir / "conversation.md"
                self.save_manager.session_name = dst_sav_dir.name
                session_key = f"{safe_folder}/{conv_name}"
                self.client.conv_logger, self.client.conv_log_file = setup_conv_logger(session_key)
            print(f"✅ Conversation '{conv_name}' déplacée vers '{safe_folder}'")
            return True, False

        # 11) Sauvegarde code
=======
>>>>>>> 5116532caa83a3349b98419997f4dcd8736fca1b
        if lower.startswith(f"{COMMAND_PREFIX}savecode"):
            base = arg.replace(" ", "_") if arg else ""
            if not self.client.history:
                print("⚠️ Aucune réponse IA.")
                return True, False
            answer = self.client.history[-1].get("response", "")
            blocks = self._extract_python_blocks(answer)
            if not blocks:
                print("ℹ️ Aucun bloc python détecté.")
                return True, False
            created: List[Path] = []
            session_dir: Path = self.save_manager.session_dir
            session_dir.mkdir(parents=True, exist_ok=True)
            if base:
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

        # --- Sauvegarde texte ---

        if lower.startswith(f"{COMMAND_PREFIX}savetxt"):
            base = arg.replace(" ", "_") if arg else ""
            if not self.client.history:
                print("⚠️ Aucune réponse IA.")
                return True, False
            answer = self.client.history[-1].get("response", "")
            from datetime import datetime
            pat_txt = re.compile(r"```txt\s+?(.*?)```", re.DOTALL | re.IGNORECASE)
            blocks = [m.strip() for m in pat_txt.findall(answer)]
            if not blocks:
                print("ℹ️ Aucun bloc txt détecté.")
                return True, False
            created: List[Path] = []
            session_dir: Path = self.save_manager.session_dir
            session_dir.mkdir(parents=True, exist_ok=True)
            if base:
                for idx, doc in enumerate(blocks, start=1):
                    name = f"{base}.txt" if len(blocks) == 1 else f"{base}_{idx}.txt"
                    out = session_dir / name
                    out.write_text(doc, encoding="utf-8")
                    created.append(out)
            else:
                for idx, doc in enumerate(blocks, start=1):
                    ts = datetime.now().strftime("%H-%M-%S")
                    name = f"doc_{ts}.txt" if len(blocks) == 1 else f"doc_{ts}_{idx}.txt"
                    out = session_dir / name
                    out.write_text(doc, encoding="utf-8")
                    created.append(out)
            print("✅ Fichier(s) TXT créé(s) :")
            for p in created:
                print(f" - {p.as_posix()}")
            return True, False

        # --- Si aucune commande reconnue ---
        return False, False

    # --- Utils ---
    @staticmethod
    def _extract_python_blocks(text: str) -> List[str]:
        if not text:
            return []
        pat_py = re.compile(r"```python\s+?(.*?)```", re.DOTALL | re.IGNORECASE)
        pat_any = re.compile(r"```\s*?(.*?)```", re.DOTALL)
        blocks = [m.group(1).strip() for m in pat_py.finditer(text)]
        if not blocks:
            blocks = [m.group(1).strip() for m in pat_any.finditer(text)]
        return [b.replace("\r\n", "\n").strip() for b in blocks if b.strip()]
