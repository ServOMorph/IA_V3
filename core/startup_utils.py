from pathlib import Path
from datetime import datetime

def init_debug_log():
    """Vide le fichier debug.log et écrit les infos de démarrage."""
    debug_log_path = Path("debug.log")
    
    # Vider ou créer le fichier
    if debug_log_path.exists():
        debug_log_path.write_text("", encoding="utf-8")
    else:
        debug_log_path.touch()

    # Écrire les infos de démarrage dans le log
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with debug_log_path.open("a", encoding="utf-8") as f:
        f.write(f"🚀 Programme lancé le {now}\n")
        f.write("🧹 Fichier debug.log vidé au démarrage.\n")
