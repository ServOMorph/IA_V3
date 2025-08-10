from core.startup_utils import init_debug_log
from core.chat_manager import ChatManager

if __name__ == "__main__":
    init_debug_log()
    chat = ChatManager()
    chat.start_chat()
