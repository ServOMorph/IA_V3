import { appState } from './config.js';
import { sendChatMessage } from './api.js';
import { addMessage } from './messages.js';
import { createSession, loadSessions, setActiveSession } from './sessions.js';
import { createCopyButton } from './ui-utils.js';

export async function sendMessage(prompt) {
  if (!appState.currentSession) {
    await createSession();
  }

  addMessage(prompt, "user");
  const typingMsg = addMessage("", "assistant", true);

  try {
    const data = await sendChatMessage(appState.currentSession, prompt);
    const answer = data.answer ?? "⚠️ Pas de réponse";

    // Vérifier si la session a été renommée automatiquement
    if (data.session && data.session !== appState.currentSession) {
      appState.currentSession = data.session;
      await loadSessions();
      setActiveSession(appState.currentSession);
    }

    const bubble = typingMsg.querySelector(".typing-indicator") 
                 || typingMsg.querySelector(".bot-bubble");

    if (bubble) {
      bubble.classList.remove("typing-indicator");
      bubble.classList.add("bot-bubble");
      bubble.innerHTML = marked.parse(answer);

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

// Gestion du bouton Plus
const plusBtn = document.getElementById("plus-btn");
if (plusBtn) {
  plusBtn.addEventListener("click", () => {
    console.log("Plus icon cliqué");
  });
}
