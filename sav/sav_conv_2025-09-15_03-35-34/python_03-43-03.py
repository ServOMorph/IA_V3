import random

class LocalAI:
    def __init__(self):
        self.responses = {
            "hello": ["Bonjour!", "Salut!"],
            "how are you?": ["Je vais bien, merci.", "Ça va ?", "Je suis en train de me développer."],
            "what's your name?": ["Je m'appelle Ollama."]
        }

    def respond(self, query):
        for key in self.responses:
            if key in query.lower():
                return random.choice(self.responses[key])
        return "Désolé, je ne comprends pas."

# Créer une instance de l'IA
local_ai = LocalAI()

while True:
    user_input = input("Vous: ")
    response = local_ai.respond(user_input)
    print("Ollama:", response)
