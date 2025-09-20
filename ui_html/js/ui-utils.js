// js/ui-utils.js
// Utilitaires pour l'interface utilisateur

import { CONFIG } from './config.js';

// Création du bouton copier
export function createCopyButton(text, successMsg) {
  const copyBtn = document.createElement("img");
  copyBtn.src = "assets/images/copier_icon.png";
  copyBtn.alt = "Copier";
  copyBtn.classList.add("copy-icon");
  copyBtn.addEventListener("click", () => {
    navigator.clipboard.writeText(text).then(() => {
      showToast(successMsg);
    });
  });
  return copyBtn;
}

// Gestion des notifications toast
export function showToast(message) {
  let container = document.querySelector(".toast-container");
  if (!container) {
    container = document.createElement("div");
    container.classList.add("toast-container");
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.classList.add("toast");
  toast.textContent = message;

  container.appendChild(toast);

  setTimeout(() => {
    toast.remove();
    if (container.children.length === 0) {
      container.remove();
    }
  }, CONFIG.TOAST_DURATION);
}

// Afficher une bannière d'erreur
export function showErrorBanner(message) {
  const chatBox = document.getElementById("chat-box");
  const div = document.createElement("div");
  div.className = "error-banner";
  div.textContent = message;
  chatBox.prepend(div);
}

// Nettoyer le contenu du chat
export function clearChat() {
  document.getElementById("chat-box").innerHTML = "";
}