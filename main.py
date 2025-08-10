from core.logging.logger import setup_logger
from core.chat_manager import ChatManager
from config import DEFAULT_MODEL

if __name__ == "__main__":
    setup_logger()  # Initialise le debug.log
    chat = ChatManager(model=DEFAULT_MODEL)
    chat.start_chat()
