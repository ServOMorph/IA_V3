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
        self.partial_index = 1  # compteur de résumés partiels

    def generate_summary(self, old_messages: list, title: str = "Résumé partiel") -> tuple[str, int]:
        """Résume une tranche d'anciens messages en Markdown structuré (4 sections)."""
        if not USE_SUMMARY or not old_messages:
            return "", self.partial_index

        # Construire le texte en filtrant uniquement le dialogue utile
        lines = []
        for m in old_messages:
            if isinstance(m, dict):
                if "prompt" in m and "response" in m:
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
            return "", self.partial_index

        # Prompt structuré
        prompt = (
            f"Tu es un assistant chargé de condenser un extrait d'historique de conversation.\n"
            f"Structure ton résumé en 4 sections claires en français (max {SUMMARY_MAX_TOKENS} tokens) :\n"
            f"- Faits clés\n- Intentions utilisateur\n- Réponses IA\n- Points en suspens\n\n"
            "=== Début du dialogue ===\n"
            f"{text}\n"
            "=== Fin du dialogue ===\n\n"
            "Résumé structuré :"
        )

        # Génération via Ollama
        summary = self.client.send_prompt(prompt).strip()

        # Format Markdown avec numérotation
        current_index = self.partial_index
        header = f"## {title} #{current_index} (généré le {datetime.datetime.now():%Y-%m-%d %H:%M})\n\n"
        formatted = (
            f"{header}"
            f"- **Faits clés :** ...\n"
            f"- **Intentions utilisateur :** ...\n"
            f"- **Réponses IA :** ...\n"
            f"- **Points en suspens :** ...\n\n"
        )

        # Si l'IA a produit du contenu structuré, on l'utilise
        if summary:
            formatted = header + summary + "\n\n"

        # Sauvegarde en append
        with self.summary_file.open("a", encoding="utf-8") as f:
            f.write(formatted)

        # Incrémenter compteur
        self.partial_index += 1

        return summary, current_index

    def load_summary(self) -> str:
        """Recharge le résumé existant si disponible."""
        if self.summary_file.exists():
            return self.summary_file.read_text(encoding="utf-8")
        return ""

    def generate_global_summary(self) -> tuple[str, int]:
        """Fusionne tous les résumés partiels en un résumé global unique et structuré."""
        if not self.summary_file.exists():
            return "", 0

        # Lire tous les résumés partiels déjà générés
        text = self.summary_file.read_text(encoding="utf-8").strip()
        if not text:
            return "", 0

        # Prompt structuré
        prompt = (
            f"Tu es un assistant chargé de condenser plusieurs résumés partiels en un résumé global.\n"
            f"Structure ton résumé en 4 sections claires en français (max {SUMMARY_MAX_TOKENS} tokens) :\n"
            f"- Faits clés\n- Intentions utilisateur\n- Réponses IA\n- Points en suspens\n\n"
            "=== Début des résumés partiels ===\n"
            f"{text}\n"
            "=== Fin ===\n\n"
            "Résumé global structuré :"
        )

        # Génération via Ollama
        summary = self.client.send_prompt(prompt).strip()

        # Format Markdown propre
        header = f"## Résumé global (généré le {datetime.datetime.now():%Y-%m-%d %H:%M})\n\n"
        formatted = (
            f"{header}"
            f"- **Faits clés :** ...\n"
            f"- **Intentions utilisateur :** ...\n"
            f"- **Réponses IA :** ...\n"
            f"- **Points en suspens :** ...\n\n"
        )

        # Si l'IA a produit déjà structuré, on remplace le squelette par le contenu réel
        if summary:
            formatted = header + summary + "\n\n"

        # Sauvegarde en append
        with self.summary_file.open("a", encoding="utf-8") as f:
            f.write(formatted)

        return summary, self.partial_index
