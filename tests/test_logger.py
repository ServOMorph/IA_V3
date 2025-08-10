from core.logger import setup_logger
import logging

if __name__ == "__main__":
    setup_logger()  # Initialise le debug.log à la racine

    logging.debug("Ceci est un message DEBUG (devrait être seulement dans debug.log)")
    logging.info("Ceci est un message INFO (devrait être seulement dans debug.log)")
    logging.warning("Ceci est un message WARNING (devrait apparaître en console et debug.log)")
    logging.error("Ceci est un message ERROR (devrait apparaître en console et debug.log)")
    logging.critical("Ceci est un message CRITICAL (devrait apparaître en console et debug.log)")

    print("\n✅ Test terminé. Vérifiez le fichier debug.log à la racine du projet.")
