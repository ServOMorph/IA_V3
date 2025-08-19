import os
import shutil

# Dossier de travail
base_dir = r"C:\Users\raph6\Documents\ServOMorph"
zip_name = "IA_V3"
zip_path = os.path.join(base_dir, zip_name)

# Étape 1 : supprimer l'ancien zip s'il existe
old_zip = zip_path + ".zip"
if os.path.exists(old_zip):
    try:
        os.remove(old_zip)
        print(f"Supprimé : {old_zip}")
    except Exception as e:
        print(f"Erreur suppression {old_zip}: {e}")

# Étape 2 : créer un nouveau zip du dossier IA_V3
src_folder = os.path.join(base_dir, zip_name)
try:
    shutil.make_archive(zip_path, 'zip', src_folder)
    print(f"Archive créée : {old_zip}")
except Exception as e:
    print(f"Erreur création zip: {e}")
    
    
