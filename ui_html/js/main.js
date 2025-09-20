// js/main.js
// Point d'entrée principal de l'application

import { checkOllama } from './api.js';
import { showErrorBanner } from './ui-utils.js';
import { createSession } from './sessions.js';
import { sendMessage } from './chat.js';

// Initialisation de l'application
async function initializeApp() {
  // Vérifier la disponibilité d'Ollama
  const ollamaAvailable = await checkOllama();
  
  if (!ollamaAvailable) {
    showErrorBanner("⚠ Serveur Ollama non disponible. Lancez `ollama serve`.");
    
    // Désactiver les contrôles de saisie
    document.getElementById("chat-input").disabled = true;
    document.getElementById("send-btn").disabled = true;
    return;
  }

  // Si Ollama est disponible, créer une session par défaut
  await createSession();
}

// Configuration des événements
function setupEventListeners() {
  const chatInput = document.getElementById("chat-input");
  const sendBtn = document.getElementById("send-btn");
  const newSessionBtn = document.getElementById("new-session-btn");

  function handleSend() {
    const text = chatInput.value.trim();
    if (text.length > 0) {
      sendMessage(text);
      chatInput.value = "";
    }
  }

  // Événements d'envoi de message
  sendBtn.addEventListener("click", handleSend);
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  });

  // Événement nouvelle session
  if (newSessionBtn) {
    newSessionBtn.addEventListener("click", () => {
      createSession();
    });
  }
}

// Démarrage de l'application
window.addEventListener("DOMContentLoaded", async () => {
  setupEventListeners();
  
  // Ne pas initialiser si Ollama n'est pas disponible
  if (!document.querySelector(".error-banner")) {
    await initializeApp();
  }
});