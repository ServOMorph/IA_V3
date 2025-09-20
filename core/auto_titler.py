# core/auto_titler.py
from pathlib import Path
from core.ollama_client import OllamaClient
from config import AUTO_TITLE_MODEL, AUTO_TITLE_MAX_CHARS


class AutoTitler:
    """
    Génère automatiquement un titre court pour une conversation
    en se basant sur le premier message utilisateur et la première réponse IA.
    """

    def __init__(self, session_dir: Path):
        self.session_dir = session_dir
        self.client = OllamaClient(model=AUTO_TITLE_MODEL)
        self.done = False  # évite de renommer plusieurs fois

    def maybe_generate_title(self, history: list[dict]) -> str | None:
        if self.done:
            return None

        first_msgs = []
        roles_seen = set()

        for m in history:
            if isinstance(m, dict):
                if "role" in m and "content" in m:
                    role = m["role"]
                    if role in ("user", "assistant"):
                        text = m["content"].strip()
                        if text:
                            first_msgs.append(text)
                            roles_seen.add(role)
                elif "prompt" in m and "response" in m:
                    if m.get("prompt"):
                        first_msgs.append(m["prompt"].strip())
                        roles_seen.add("user")
                    if m.get("response"):
                        first_msgs.append(m["response"].strip())
                        roles_seen.add("assistant")

            if len(first_msgs) >= 2 and {"user", "assistant"}.issubset(roles_seen):
                break

        if len(first_msgs) < 2 or not {"user", "assistant"}.issubset(roles_seen):
            return None

        # Génération du titre
        prompt = (
            f"Donne un titre très court et clair à cette conversation.\n"
            f"- Maximum {AUTO_TITLE_MAX_CHARS} caractères.\n"
            f"- Écris uniquement le titre, sans guillemets.\n\n"
            "Messages initiaux :\n" + "\n".join(first_msgs)
        )

        title = self.client.send_prompt(prompt).strip()
        title = " ".join(title.splitlines()).strip()
        if len(title) > AUTO_TITLE_MAX_CHARS:
            title = title[:AUTO_TITLE_MAX_CHARS].rstrip()

        self.done = True
        return title or None

