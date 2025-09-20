// js/sessions.js
// Gestion des sessions de conversation

import { CONFIG, appState } from './config.js';
import { apiGet, apiPost, apiPut, apiDelete } from './api.js';
import { showToast, clearChat } from './ui-utils.js';
import { addMessage, parseHistoryFromMarkdown } from './messages.js';

// Marquer une session comme active
export function setActiveSession(name) {
  appState.currentSession = name;
  document.querySelectorAll(".conv-list li").forEach(li => {
    li.classList.toggle("active", li.dataset.session === name);
  });
}

// Charger la liste des sessions
export async function loadSessions() {
  try {
    const res = await apiGet("/sessions");
    const sessions = res.sessions;
    const list = document.querySelector(".conv-list");
    list.innerHTML = "";

    sessions.forEach(s => {
      const li = document.createElement("li");

      // identifiant brut (avec underscores) pour l'API
      li.dataset.session = s;

      // affichage texte (tel quel)
      const spanText = document.createElement("span");
      spanText.textContent = s;

      // bouton menu "..."
      const spanMenu = document.createElement("span");
      spanMenu.classList.add("conv-menu");
      spanMenu.textContent = "...";
      spanMenu.addEventListener("click", (e) => {
        e.stopPropagation(); // empêche d'ouvrir l'historique
        openConvMenu(e, li.dataset.session);
      });

      li.appendChild(spanText);
      li.appendChild(spanMenu);

      // clic principal → charger historique
      li.addEventListener("click", () => loadHistory(li.dataset.session));

      list.appendChild(li);
    });

  } catch (err) {
    console.error("Erreur chargement sessions :", err);
  }
}

// Créer une nouvelle session
export async function createSession() {
  try {
    const data = await apiPost("/sessions/");
    appState.currentSession = data.session;
    await loadSessions();
    await loadHistory(appState.currentSession);
  } catch (err) {
    console.error("Erreur création session :", err);
  }
}

// Charger l'historique d'une session
export async function loadHistory(sessionName) {
  try {
    const res = await apiGet(`/sessions/${sessionName}/history`);
    const mdText = res.history;
    clearChat();
    setActiveSession(sessionName);

    const history = parseHistoryFromMarkdown(mdText);

    // Rendu des messages avec marked.parse pour l'assistant seulement
    history.forEach(msg => {
      if (msg.role === "assistant") {
        addMessage(msg.content, "assistant");
      } else if (msg.role === "user") {
        addMessage(msg.content, "user");
      }
    });

  } catch (err) {
    console.error("Erreur chargement historique :", err);
  }
}

// Renommer une session
export async function renameSession(oldName, newName) {
  try {
    const url = `/sessions/${encodeURIComponent(oldName)}/rename?new_name=${encodeURIComponent(newName)}`;
    console.log("API RENAME URL:", url);

    await apiPut(url);
    
    await loadSessions();
    appState.currentSession = newName;
    setActiveSession(newName);
    await loadHistory(newName);
    showToast(`Session renommée en "${newName}" ✅`);
    
    return true;
  } catch (err) {
    console.error("Erreur JS renommer :", err);
    showToast("⚠️ Erreur lors du renommage");
    return false;
  }
}

// Supprimer une session
export async function deleteSession(sessionName) {
  try {
    const url = `/sessions/${encodeURIComponent(sessionName)}`;
    console.log("API DELETE URL:", url);

    await apiDelete(url);
    
    await loadSessions();
    if (appState.currentSession === sessionName) {
      await createSession();
    }
    showToast(`Session "${sessionName}" supprimée 🗑️`);
    
    return true;
  } catch (err) {
    console.error("Erreur JS suppression :", err);
    showToast("⚠️ Erreur lors de la suppression");
    return false;
  }
}

// Menu contextuel pour les conversations
function openConvMenu(event, sessionName) {
  const oldMenu = document.querySelector(".conv-context-menu");
  if (oldMenu) oldMenu.remove();

  const menu = document.createElement("div");
  menu.classList.add("conv-context-menu");

  // --- Renommer ---
  const rename = document.createElement("div");
  rename.textContent = "Renommer";
  rename.addEventListener("click", async () => {
    const newName = prompt("Nouveau nom :", sessionName);
    if (newName && newName !== sessionName) {
      await renameSession(sessionName, newName);
    }
    menu.remove();
  });

  // --- Supprimer ---
  const del = document.createElement("div");
  del.textContent = "Supprimer";
  del.addEventListener("click", async () => {
    if (confirm(`Supprimer la conversation "${sessionName}" ?`)) {
      await deleteSession(sessionName);
    }
    menu.remove();
  });

  menu.appendChild(rename);
  menu.appendChild(del);

  menu.style.top = event.clientY + "px";
  menu.style.left = event.clientX + "px";
  document.body.appendChild(menu);

  document.addEventListener("click", function closeMenu(e) {
    if (!menu.contains(e.target)) {
      menu.remove();
      document.removeEventListener("click", closeMenu);
    }
  });
}