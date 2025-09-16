# core/ollama_client.py
import requests
import logging
import subprocess
from pathlib import Path
from core.logging.conv_logger import setup_conv_logger
from datetime import datetime
import json
from config import OLLAMA_BASE_URL, DEFAULT_MODEL, OLLAMA_TIMEOUT, DEV_MODE, DATA_DIR, MAX_TOKENS, TEMPERATURE, TOP_P, TOP_K


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
        full_prompt = f"{context}\n\n---\n👤 Vous : {prompt}\n🤖 Ollama :" if context else prompt

        # Log prompt
        self.conv_logger.info("------ NOUVEL ÉCHANGE ------")
        self.conv_logger.info(f"[PROMPT ENVOYÉ À {self.model.upper()}]\n{full_prompt}")

        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "num_predict": MAX_TOKENS,
                "temperature": TEMPERATURE,
                "top_p": TOP_P,
                "top_k": TOP_K,
            }
        }

        # Mesure du temps
        import time
        start_time = time.perf_counter()
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            logging.error("Délai d’attente dépassé pour Ollama.")
            return ""
        except requests.exceptions.RequestException as e:
            logging.error(f"Erreur de connexion à Ollama : {e}")
            return ""
        end_time = time.perf_counter()
        elapsed = end_time - start_time

        try:
            data = response.json()
        except json.JSONDecodeError:
            logging.error("Réponse JSON invalide reçue d’Ollama.")
            return ""

        answer = data.get("response", "").strip()

        # Log réponse
        self.conv_logger.info(f"[RÉPONSE DE {self.model.upper()}]\n{answer}\n")

        # Historique interne
        self.history.append({
            "prompt": prompt,
            "response": answer,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "elapsed": elapsed
        })

        # Mode dev : affichage + sauvegarde dans data/
        if DEV_MODE:
            print(f"\n⏱ Temps de réponse ({self.model}): {elapsed:.2f} sec\n")

            # Log texte
            txt_file = DATA_DIR / "dev_responses.log"
            with txt_file.open("a", encoding="utf-8") as f:
                f.write("=== NOUVEL ESSAI ===\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Modèle: {self.model}\n")
                f.write(f"Prompt: {prompt}\n")
                f.write(f"Réponse: {answer}\n")
                f.write(f"Temps: {elapsed:.2f} sec\n")
                f.write("-------------------------------\n")

            # Log JSONL
            json_file = DATA_DIR / "dev_responses.jsonl"
            record = {
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "model": self.model,
                "prompt": prompt,
                "response": answer,
                "elapsed_sec": round(elapsed, 3)
            }
            with json_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

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


def list_installed_models():
    """Liste les modèles Ollama installés, sauvegarde dans data/ et affiche si DEV_MODE est True."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        models = result.stdout.strip()

        # Sauvegarde dans data/
        save_path = DATA_DIR / "models_list.txt"
        save_path.write_text(models, encoding="utf-8")

        # Print si mode dev
        if DEV_MODE:
            print("\n=== Modèles Ollama installés ===")
            print(models)
            print("================================\n")

        return models
    except Exception as e:
        logging.error(f"Impossible de lister les modèles Ollama : {e}")
        return ""
