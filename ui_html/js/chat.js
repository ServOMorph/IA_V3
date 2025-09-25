import { appState } from './config.js';
import { sendChatMessage } from './api.js';
import { addMessage } from './messages.js';
import { createSession, loadSessions, setActiveSession } from './sessions.js';
import { createCopyButton } from './ui-utils.js';
import { showToast } from './ui-utils.js';
import { CONFIG } from './config.js';

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
  // Créer dynamiquement un input file caché
  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.style.display = "none";
  document.body.appendChild(fileInput);

  plusBtn.addEventListener("click", () => {
    fileInput.click();
  });

  fileInput.addEventListener("change", async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (!appState.currentSession) {
      await createSession();
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${CONFIG.API_BASE_URL}/files/${appState.currentSession}/upload`, {
        method: "POST",
        body: formData
      });

      if (!res.ok) {
        const errText = await res.text();
        throw new Error(`Erreur upload: ${errText}`);
      }

      await res.json();
      // ✅ Affiche un toast succès
      showToast(`📎 ${file.name} ajouté au contexte`);
    } catch (err) {
      console.error("Erreur upload fichier:", err);
      // ⚠️ Affiche un toast erreur
      showToast("⚠️ Erreur lors de l’upload du fichier");
    } finally {
      fileInput.value = ""; // reset
    }
  });
}