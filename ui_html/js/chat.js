// js/chat.js
// Gestion des fonctionnalités de chat

import { appState } from './config.js';
import { sendChatMessage } from './api.js';
import { addMessage } from './messages.js';
import { createSession } from './sessions.js';
import { createCopyButton } from './ui-utils.js';

// Envoyer un message
export async function sendMessage(prompt) {
  if (!appState.currentSession) {
    await createSession();
  }

  addMessage(prompt, "user");
  const typingMsg = addMessage("", "assistant", true);

  try {
    const data = await sendChatMessage(appState.currentSession, prompt);
    const answer = data.answer ?? "⚠️ Pas de réponse";

    const bubble = typingMsg.querySelector(".typing-indicator") 
                 || typingMsg.querySelector(".bot-bubble");

    if (bubble) {
      bubble.classList.remove("typing-indicator");
      bubble.classList.add("bot-bubble");
      bubble.innerHTML = marked.parse(answer);
      
      // Ajouter le bouton copier
      const bubbleWrapper = bubble.parentElement;
      if (bubbleWrapper && !bubbleWrapper.querySelector(".copy-icon")) {
        bubbleWrapper.appendChild(createCopyButton(answer, "Réponse IA copiée ✅"));
      }
    }
  } catch (err) {
    console.error("Erreur envoi message :", err);
    const bubble = typingMsg.querySelector("div");
    if (bubble) bubble.textContent = "⚠️ Erreur API";
  }
}