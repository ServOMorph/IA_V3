# core/summarizer.py
from config import SUMMARY_MODEL, SUMMARY_MAX_TOKENS, MAX_HISTORY_MESSAGES, USE_SUMMARY
from pathlib import Path
from core.ollama_client import OllamaClient
import datetime


class Summarizer:
    """
    Gestionnaire de résumé pour les conversations trop longues.
    - Gère plusieurs formats d'historique (role/content et prompt/response).
    - Génère un résumé condensé de l'historique avec un modèle léger.
    - Sauvegarde le résumé dans /sav/<session>/summary.md
    - Permet de recharger un résumé existant.
    """

    def __init__(self, session_dir: Path):
        self.session_dir = session_dir
        self.summary_file = session_dir / "summary.md"
        self.client = OllamaClient(model=SUMMARY_MODEL)

    def generate_summary(self, old_messages: list) -> str:
        """Résume une liste de messages anciens et sauvegarde le résultat."""
        if not USE_SUMMARY or not old_messages:
            return ""

        # Construire le texte en filtrant uniquement le dialogue utile
        lines = []
        for m in old_messages:
            if isinstance(m, dict):
                if "prompt" in m and "response" in m:
                    # Format conversation utile
                    user_text = m.get("prompt", "").strip()
                    ai_text = m.get("response", "").strip()
                    if user_text:
                        lines.append(f"user: {user_text}")
                    if ai_text:
                        lines.append(f"assistant: {ai_text}")
                elif "role" in m and "content" in m:
                    if m.get("role") not in ("system", None):
                        role = m.get("role", "unknown")
                        content = m.get("content", "").strip()
                        if content:
                            lines.append(f"{role}: {content}")
            else:
                lines.append(str(m))
        text = "\n".join(lines).strip()

        if not text:
            return ""

        # Prompt de résumé
        prompt = (
            f"Tu es un assistant chargé de condenser un historique de conversation.\n"
            f"Fais un résumé clair et concis en français (max {SUMMARY_MAX_TOKENS} tokens).\n\n"
            "=== Début du dialogue ===\n"
            f"{text}\n"
            "=== Fin du dialogue ===\n\n"
            "Résumé :"
        )

        # Génération via Ollama
        summary = self.client.send_prompt(prompt).strip()

        # Sauvegarde dans summary.md
        header = f"## Résumé historique (généré le {datetime.datetime.now():%Y-%m-%d %H:%M})\n\n"
        self.summary_file.write_text(header + summary, encoding="utf-8")

        return summary

    def load_summary(self) -> str:
        """Recharge le résumé existant si disponible."""
        if self.summary_file.exists():
            return self.summary_file.read_text(encoding="utf-8")
        return ""
