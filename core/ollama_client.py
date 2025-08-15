# core/ollama_client.py
import requests
import logging
from pathlib import Path
from core.logging.conv_logger import setup_conv_logger
from datetime import datetime
import json
from config import OLLAMA_BASE_URL, DEFAULT_MODEL, OLLAMA_TIMEOUT


class OllamaClient:
    def __init__(self, base_url=OLLAMA_BASE_URL, model=DEFAULT_MODEL, timeout=OLLAMA_TIMEOUT, session_file=None):
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        self.history = []  # échanges en mémoire
        self.session_file = Path(session_file) if session_file else None

        # Nommer le logger avec le dossier de session, pas le fichier
        session_name = self.session_file.parent.name if self.session_file else "conversation"
        self.conv_logger, self.conv_log_file = setup_conv_logger(session_name)

    def send_prompt(self, prompt: str) -> str:
        if not prompt.strip():
            logging.error("Le prompt est vide.")
            return ""

        # Contexte depuis l'historique interne
        context = self._get_saved_conversation()

        # Prompt complet
        if context:
            full_prompt = f"{context}\n\n---\n👤 Vous : {prompt}\n🤖 Ollama :"
        else:
            full_prompt = prompt

        # Log prompt
        self.conv_logger.info("------ NOUVEL ÉCHANGE ------")
        self.conv_logger.info(f"[PROMPT ENVOYÉ À MISTRAL]\n{full_prompt}")

        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            logging.error("Délai d’attente dépassé pour Ollama.")
            return ""
        except requests.exceptions.RequestException as e:
            logging.error(f"Erreur de connexion à Ollama : {e}")
            return ""

        try:
            data = response.json()
        except json.JSONDecodeError:
            logging.error("Réponse JSON invalide reçue d’Ollama.")
            return ""

        answer = data.get("response", "").strip()

        # Log réponse
        self.conv_logger.info(f"[RÉPONSE DE MISTRAL]\n{answer}\n")

        # Historique interne
        self.history.append({
            "prompt": prompt,
            "response": answer,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        return answer

    def _get_saved_conversation(self):
        """Reconstruit le contexte depuis self.history."""
        if not self.history:
            return ""

        lines = []
        for ex in self.history:
            # Messages système (role/content)
            if "role" in ex and "content" in ex:
                ts = ex.get("timestamp", None)
                if ts:
                    lines.append(f"--- {ts} ---")
                lines.append(f"[{ex['role'].upper()}] : {ex['content']}\n")
                continue

            # Échanges classiques (prompt/response)
            ts = ex.get("timestamp", "")
            if ts:
                lines.append(f"--- {ts} ---")
            if "prompt" in ex:
                lines.append(f"👤 Vous : {ex['prompt']}")
            if "response" in ex:
                lines.append(f"🤖 Ollama : {ex['response']}\n")

        return "\n".join(lines).strip()
