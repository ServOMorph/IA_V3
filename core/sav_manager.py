print(">>> DEBUG: core/sav_manager.py chargé depuis", __file__)

import logging
import re
from pathlib import Path
from datetime import datetime
import shutil
from config import SAVE_DIR, SAVE_FILE_PREFIX, SAVE_FILE_DATETIME_FORMAT, LOGS_DIR

_MD_HEADER = """# Conversation
_Dossier_: {folder}
_Démarrée_: {started_at}

---
"""

class SaveManager:
    """
    Sauvegarde par dossier. Chaque session a:
      - conversation.md
      - 0..n fichiers .py extraits des réponses IA
    """
    def __init__(self, save_dir=SAVE_DIR):
        self.save_root = Path(save_dir)
        # DEBUG
        print(f"[DEBUG SaveManager] save_dir param = {save_dir}")
        print(f"[DEBUG SaveManager] self.save_root = {self.save_root.resolve()}")
        self.save_root.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime(SAVE_FILE_DATETIME_FORMAT)
        self.session_name = f"{SAVE_FILE_PREFIX}{stamp}"
        self.session_dir = self.save_root / self.session_name
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.session_md = self.session_dir / "conversation.md"

    # rétro-compat (appelé depuis ChatManager)
    def save_txt(self, history):
        self.save_md(history)

    def save_md(self, history):
        """Écrit l'historique complet en Markdown."""
        try:
            lines = [_MD_HEADER.format(
                folder=self.session_dir.name,
                started_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )]

            for ex in history:
                if not isinstance(ex, dict):
                    logging.error(f"[save_md] Entrée inattendue dans history: {repr(ex)}")
                    continue

                ts = ex.get("timestamp", "")

                # Cas role/content
                if "role" in ex and "content" in ex:
                    lines.append(f"### {ts or ''}  \n**[{ex['role']}]**\n\n{ex['content']}\n")
                    continue

                # Cas prompt/response
                if "prompt" in ex or "response" in ex:
                    user = ex.get("prompt", "")
                    ans = ex.get("response", "")
                    lines.append(f"---\n**{ts}**\n\n**Vous**:\n\n{user}\n\n**IA**:\n\n{ans}\n")
                    continue

                logging.error(f"[save_md] Format non reconnu: {repr(ex)}")

            self.session_md.write_text("\n".join(lines), encoding="utf-8")
            logging.info(f"Historique MD écrit: {self.session_md.resolve()}")

        except Exception as e:
            logging.error(f"Erreur sauvegarde MD: {e}")

    def extract_python_blocks(self, text: str):
        """Retourne la liste des blocs de code Python ```python ... ```."""
        if not text:
            return []
        pattern = r"```python\s+(.*?)```"
        return re.findall(pattern, text, flags=re.S | re.I)

    def save_python_from_response(self, response_text: str, base_name: str | None = None):
        """
        Extrait et sauvegarde tous les blocs Python de la réponse.
        Retourne la liste des chemins créés.
        """
        blocks = self.extract_python_blocks(response_text)
        if not blocks:
            logging.info("Aucun bloc Python détecté.")
            return []

        created = []
        ts = datetime.now().strftime("%H-%M-%S")
        for idx, code in enumerate(blocks, start=1):
            stem = base_name or f"code_{ts}"
            path = self.session_dir / f"{stem}_{idx}.py" if len(blocks) > 1 else self.session_dir / f"{stem}.py"
            path.write_text(code.strip() + "\n", encoding="utf-8")
            created.append(path)
            logging.info(f"Code sauvegardé: {path.resolve()}")
        return created

    def rename_session_file(self, new_name):
        try:
            print("========== DEBUG rename_session_file ==========")
            print(f"session_name: {self.session_name}")
            print(f"session_dir (raw): {self.session_dir}")
            print(f"session_dir (absolute): {self.session_dir.resolve()}")
            print(f"session_dir.exists(): {self.session_dir.exists()}")
            print("==============================================")

            old_dir = self.session_dir
            print(f"[DEBUG rename_session_file] self.session_dir = {self.session_dir}")
            print(f"[DEBUG rename_session_file] absolute = {self.session_dir.resolve()}")
            print(f"[DEBUG rename_session_file] exists = {self.session_dir.exists()}")

            if not old_dir.exists():
                logging.error(f"Dossier source introuvable: {old_dir}")
                return False

            new_dir = self.save_root / new_name
            if new_dir.exists():
                logging.error(f"Le dossier '{new_dir.name}' existe déjà.")
                return False

            # DEBUG : afficher les chemins pour comprendre un éventuel échec
            logging.info(f"[DEBUG] rename_session_file old_dir={old_dir} exists={old_dir.exists()}")
            logging.info(f"[DEBUG] rename_session_file new_dir={new_dir}")

            # Renommer le dossier de session
            shutil.move(str(old_dir), str(new_dir))

            # Renommer le .log correspondant s'il existe
            old_log_file = Path(LOGS_DIR) / f"{old_dir.name}.log"
            if old_log_file.exists():
                new_log_file = Path(LOGS_DIR) / f"{new_name}.log"
                shutil.move(str(old_log_file), str(new_log_file))
                logging.info(f"Fichier log renommé : {new_log_file.resolve()}")
            else:
                logging.info(f"Aucun log à renommer pour {old_dir.name}")

            # MAJ internes
            self.session_dir = new_dir
            self.session_md = self.session_dir / "conversation.md"
            self.session_name = new_name
            return True
        except Exception as e:
            logging.error(f"Erreur lors du renommage: {e}")
            return False

    def load_session_file(self, name):
        """
        Compat: renvoie le contenu de conversation.md dans le dossier 'name'.
        """
        file_path = self.save_root / name / "conversation.md"
        if not file_path.exists():
            logging.error(f"'{file_path}' introuvable.")
            return None
        try:
            return file_path.read_text(encoding="utf-8")
        except Exception as e:
            logging.error(f"Erreur de chargement: {e}")
            return 
        
    def save_txt_from_response(self, response_text: str, base_name: str | None = None):
        """
        Extrait et sauvegarde tous les blocs ```txt ... ``` de la réponse.
        Retourne la liste des chemins créés.
        """
        import re
        if not response_text:
            return []

        # Détecter les blocs TXT
        pattern = r"```txt\s+(.*?)```"
        blocks = re.findall(pattern, response_text, flags=re.S | re.I)
        if not blocks:
            return []

        created = []
        from datetime import datetime
        ts = datetime.now().strftime("%H-%M-%S")
        for idx, block in enumerate(blocks, start=1):
            stem = base_name or f"doc_{ts}"
            path = self.session_dir / f"{stem}_{idx}.txt" if len(blocks) > 1 else self.session_dir / f"{stem}.txt"
            path.write_text(block.strip() + "\n", encoding="utf-8")
            created.append(path)
            logging.info(f"Document TXT sauvegardé : {path.resolve()}")
        return created

    def parse_md_to_history(self, md_text: str):
        """
        Transforme le contenu de conversation.md en une liste de dicts
        [{role: ..., content: ...}].
        Supporte deux formats :
          - ### timestamp + ligne suivante **[role]**
          - **Vous** / **IA**
        """
        history = []
        if not md_text:
            return history

        import re
        lines = md_text.splitlines()
        buffer = []
        current_role = None
        expect_role = False  # flag quand on a vu un ###

        def flush_buffer():
            nonlocal buffer, current_role
            if current_role and buffer:
                history.append({"role": current_role, "content": "\n".join(buffer).strip()})
            buffer = []
            current_role = None

        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue

            # Cas 1 : début de bloc ### timestamp
            if line_stripped.startswith("###"):
                flush_buffer()
                expect_role = True
                continue

            # Cas 2 : ligne de rôle après un ###
            if expect_role:
                m = re.match(r"^\*\*\[(.*?)\]\*\*$", line_stripped)
                if m:
                    current_role = m.group(1).lower()
                expect_role = False
                continue

            # Cas 3 : format alternatif **Vous** / **IA**
            if line_stripped.startswith("**Vous**"):
                flush_buffer()
                current_role = "user"
                continue
            if line_stripped.startswith("**IA**"):
                flush_buffer()
                current_role = "assistant"
                continue

            # Cas 4 : contenu
            if current_role:
                buffer.append(line_stripped)

        flush_buffer()
        return history
    
    def save_blocks_from_response(self, response_text: str, block_type: str, ext: str, base_name: str | None = None):
        """
        Extrait et sauvegarde tous les blocs de type ```<block_type> ... ``` présents dans le texte.
        Retourne la liste des chemins créés.
        
        Exemple :
        - block_type="python", ext="py"
        - block_type="txt", ext="txt"
        - block_type="csv", ext="csv"
        """
        import re
        if not response_text:
            return []

        pattern = rf"```{block_type}\s+(.*?)```"
        blocks = re.findall(pattern, response_text, flags=re.S | re.I)
        if not blocks:
            return []

        created = []
        from datetime import datetime
        ts = datetime.now().strftime("%H-%M-%S")

        for idx, block in enumerate(blocks, start=1):
            stem = base_name or f"{block_type}_{ts}"
            path = self.session_dir / (
                f"{stem}_{idx}.{ext}" if len(blocks) > 1 else f"{stem}.{ext}"
            )
            try:
                path.write_text(block.strip() + "\n", encoding="utf-8")
                created.append(path)
                logging.info(f"Bloc {block_type} sauvegardé : {path.resolve()}")
            except Exception as e:
                logging.error(f"Erreur sauvegarde bloc {block_type}: {e}")

        return created

