// js/messages.js
// Gestion des messages dans le chat

import { createCopyButton } from './ui-utils.js';

// Ajouter un message dans le chat
export function addMessage(text, sender = "assistant", isTyping = false) {
  const chatBox = document.getElementById("chat-box");
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender === "user" ? "user" : "assistant");

  if (sender === "assistant") {
    const wrapper = document.createElement("div");
    wrapper.classList.add("bot-message-wrapper");

    const logo = document.createElement("img");
    logo.src = "assets/images/logo_vertia_seul.png";
    logo.alt = "IA";
    logo.classList.add("bot-logo");

    // Bulle IA
    const bubble = document.createElement("div");
    bubble.classList.add(isTyping ? "typing-indicator" : "bot-bubble");
    if (isTyping) {
      bubble.textContent = "...";
    } else {
      bubble.innerHTML = marked.parse(text);
    }

    // Wrapper bulle + bouton
    const bubbleWrapper = document.createElement("div");
    bubbleWrapper.classList.add("bot-bubble-wrapper");
    bubbleWrapper.appendChild(bubble);
    if (!isTyping) {
      bubbleWrapper.appendChild(createCopyButton(text, "Réponse IA copiée ✅"));
    }

    wrapper.appendChild(logo);
    wrapper.appendChild(bubbleWrapper);
    msgDiv.appendChild(wrapper);

  } else if (sender === "user") {
    const wrapper = document.createElement("div");
    wrapper.classList.add("user-message-wrapper");

    const logo = document.createElement("img");
    logo.src = "assets/images/logo_user.png";
    logo.alt = "User";
    logo.classList.add("user-logo");

    // Bulle
    const bubble = document.createElement("div");
    bubble.classList.add("user-bubble");
    bubble.textContent = text;

    // Wrapper bulle + bouton
    const bubbleWrapper = document.createElement("div");
    bubbleWrapper.classList.add("user-bubble-wrapper");
    bubbleWrapper.appendChild(bubble);
    bubbleWrapper.appendChild(createCopyButton(text, "Message copié ✅"));

    wrapper.appendChild(logo);
    wrapper.appendChild(bubbleWrapper);
    msgDiv.appendChild(wrapper);
  }

  chatBox.appendChild(msgDiv);
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });
  return msgDiv;
}

// Parser l'historique depuis le format Markdown
export function parseHistoryFromMarkdown(mdText) {
  const lines = mdText.split("\n");
  let history = [];
  let buffer = [];
  let currentRole = null;
  let expectRole = false;

  function flushBuffer() {
    if (currentRole && buffer.length > 0) {
      // Ignorer les messages système
      if (currentRole === "system") {
        buffer = [];
        currentRole = null;
        return;
      }

      // Fusionner contenu
      let content = buffer.join("\n").trim();

      // Supprimer TOUTES les lignes d'horodatage (avec ou sans **)
      content = content.replace(/^\*\*\d{4}-\d{2}-\d{2}.*\*\*$/gm, "").trim();
      content = content.replace(/^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$/gm, "").trim();

      // Supprimer les marqueurs de rôle
      content = content.replace(/^(\*\*IA\*\*:?)/i, "").trim();
      content = content.replace(/^(\*\*Vous\*\*:?)/i, "").trim();
      content = content.replace(/^IA\s*:/i, "").trim();
      content = content.replace(/^Vous\s*:/i, "").trim();

      // Nettoyer les lignes vides au début et à la fin
      content = content.replace(/^\n+|\n+$/g, "");
      
      // Nettoyer les lignes vides multiples
      content = content.replace(/\n\s*\n\s*\n+/g, "\n\n").trim();

      if (content) {
        history.push({ role: currentRole, content });
      }
    }
    buffer = [];
    currentRole = null;
  }

  for (let line of lines) {
    const lineStripped = line.trim();
    
    // Ignorer les lignes vides
    if (!lineStripped) continue;

    // Ignorer les séparateurs "---"
    if (lineStripped === "---") continue;

    // Ignorer les lignes qui sont uniquement des horodatages
    if (/^\*?\*?\d{4}-\d{2}-\d{2}.*\*?\*?$/.test(lineStripped)) continue;

    // Détecter les sections ###
    if (lineStripped.startsWith("###")) {
      flushBuffer();
      expectRole = true;
      continue;
    }

    if (expectRole) {
      const m = lineStripped.match(/^\*\*\[(.*?)\]\*\*$/);
      if (m) currentRole = m[1].toLowerCase();
      expectRole = false;
      continue;
    }

    // Détecter **Vous**: ou **Vous**
    if (lineStripped.match(/^\*\*Vous\*\*:?$/i)) {
      flushBuffer();
      currentRole = "user";
      continue;
    }

    // Détecter **IA**: ou **IA**
    if (lineStripped.match(/^\*\*IA\*\*:?$/i)) {
      flushBuffer();
      currentRole = "assistant";
      continue;
    }

    // Ajouter le contenu au buffer si on a un rôle actuel
    if (currentRole) {
      buffer.push(lineStripped);
    }
  }
  
  // Traiter le dernier buffer
  flushBuffer();

  return history;
}