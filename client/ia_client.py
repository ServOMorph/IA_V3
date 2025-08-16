from core.chat_manager import ChatManager

class IAClient:
    def __init__(self):
        self.backend = ChatManager()

    def send_message(self, message: str) -> str:
        return self.backend.client.send_prompt(message)

    def save_conversation(self, last_response: str | None = None):
        try:
            self.backend.save_manager.save_md(self.backend.client.history)

            if last_response:
                self.backend.save_manager.save_python_from_response(last_response)
                self.backend.save_manager.save_txt_from_response(last_response)
        except Exception as e:
            print(f"[ERREUR SAVE] {e}")
