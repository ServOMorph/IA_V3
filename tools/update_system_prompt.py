# update_system_prompt.py
import re
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.py"

def update_system_prompt():
    print("=== Mise à jour du prompt système ===")
    print("Entrez le nouveau prompt (finir par une ligne vide) :")

    lines = []
    while True:
        line = input()
        if line.strip() == "" and lines:  # stop si vide et déjà du contenu
            break
        lines.append(line)

    new_prompt = "\n".join(lines)

    # Charger config.py
    content = CONFIG_PATH.read_text(encoding="utf-8")

    # Remplacer le contenu de DEFAULT_SYSTEM_PROMPT
    new_prompt_literal = '"""\n' + new_prompt + '\n"""'
    content = re.sub(
        r'DEFAULT_SYSTEM_PROMPT\s*=\s*("""[\s\S]*?""")',
        f'DEFAULT_SYSTEM_PROMPT = {new_prompt_literal}',
        content
    )

    CONFIG_PATH.write_text(content, encoding="utf-8")
    print(f"✅ Prompt système mis à jour dans {CONFIG_PATH}")

if __name__ == "__main__":
    update_system_prompt()
