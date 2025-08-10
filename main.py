from core.logger import setup_logger
from core.chat_manager import ChatManager

if __name__ == "__main__":
    setup_logger()  # Initialise le debug.log
    chat = ChatManager(model="mistral")
    chat.start_chat()
