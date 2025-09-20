// ui_html/js/script.js

const API_BASE_URL = "http://localhost:8001";
let currentSession = null;

// Vérifier disponibilité du serveur Ollama
async function checkOllama() {
  try {
    const res = await fetch("http://localhost:11434/api/tags");
    if (!res.ok) throw new Error("HTTP " + res.status);
    console.log("Ollama serveur OK");
  } catch (e) {
    const chatBox = document.getElementById("chat-box");
    const div = document.createElement("div");
    div.className = "error-banner";
    div.textContent = "⚠ Serveur Ollama non disponible. Lancez `ollama serve`.";
    chatBox.prepend(div);

    document.getElementById("chat-input").disabled = true;
    document.getElementById("send-btn").disabled = true;
  }
}

// ====== Utils DOM ======
function addMessage(text, sender = "assistant", isTyping = false) {
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

function clearChat() {
  document.getElementById("chat-box").innerHTML = "";
}

// ====== Utils Copier ======
function createCopyButton(text, successMsg) {
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

function setActiveSession(name) {
  currentSession = name;
  document.querySelectorAll(".conv-list li").forEach(li => {
    li.classList.toggle("active", li.dataset.session === name);
  });
}



// ====== API calls ======
async function apiGet(path) {
  const res = await fetch(`${API_BASE_URL}${path}`);
  if (!res.ok) throw new Error(`GET ${path} failed (${res.status})`);
  return res.json();
}

async function apiPost(path, body = {}) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`POST ${path} failed (${res.status})`);
  return res.json();
}

// ====== Sessions ======
async function loadSessions() {
  try {
    const res = await apiGet("/sessions");
    const sessions = res.sessions;
    const list = document.querySelector(".conv-list");
    list.innerHTML = "";

    sessions.forEach(s => {
      const li = document.createElement("li");

      // ✅ identifiant brut (avec underscores) pour l'API
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
        openConvMenu(e, li.dataset.session); // ✅ toujours dataset
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

async function createSession() {
  try {
    const data = await apiPost("/sessions/");
    currentSession = data.session;
    await loadSessions();
    await loadHistory(currentSession);
  } catch (err) {
    console.error("Erreur création session :", err);
  }
}

async function loadHistory(sessionName) {
  try {
    const res = await apiGet(`/sessions/${sessionName}/history`);
    const mdText = res.history;
    clearChat();
    setActiveSession(sessionName);

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

        // ✅ CORRECTION : Supprimer TOUTES les lignes d'horodatage (avec ou sans **)
        content = content.replace(/^\*\*\d{4}-\d{2}-\d{2}.*\*\*$/gm, "").trim();
        content = content.replace(/^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$/gm, "").trim();

        // ✅ CORRECTION : Supprimer les marqueurs de rôle
        content = content.replace(/^(\*\*IA\*\*:?)/i, "").trim();
        content = content.replace(/^(\*\*Vous\*\*:?)/i, "").trim();
        content = content.replace(/^IA\s*:/i, "").trim();
        content = content.replace(/^Vous\s*:/i, "").trim();

        // ✅ NOUVEAU : Nettoyer les lignes vides au début et à la fin
        content = content.replace(/^\n+|\n+$/g, "");
        
        // ✅ NOUVEAU : Nettoyer les lignes vides multiples
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
      
      // ✅ NOUVEAU : Ignorer les lignes vides
      if (!lineStripped) continue;

      // ✅ NOUVEAU : Ignorer les séparateurs "---"
      if (lineStripped === "---") continue;

      // ✅ NOUVEAU : Ignorer les lignes qui sont uniquement des horodatages
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

      // ✅ CORRECTION : Détecter **Vous**: ou **Vous**
      if (lineStripped.match(/^\*\*Vous\*\*:?$/i)) {
        flushBuffer();
        currentRole = "user";
        continue;
      }

      // ✅ CORRECTION : Détecter **IA**: ou **IA**
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

    // ✅ CORRECTION : Rendu des messages avec marked.parse pour l'assistant seulement
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
// ====== Chat ======
async function apiSendMessage(prompt) {
  const response = await fetch(`${API_BASE_URL}/chat/${currentSession}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt })
  });

  if (!response.ok) {
    const errText = await response.text();
    console.error("Erreur API /chat :", errText);
    throw new Error("Erreur API /chat");
  }

  return response.json();
}

async function sendMessage(prompt) {
  if (!currentSession) {
    await createSession();
  }

  addMessage(prompt, "user");
  const typingMsg = addMessage("", "assistant", true);

  try {
    const data = await apiSendMessage(prompt);
    const answer = data.answer ?? "⚠️ Pas de réponse";

    const bubble = typingMsg.querySelector(".typing-indicator") 
                 || typingMsg.querySelector(".bot-bubble");

    if (bubble) {
      bubble.classList.remove("typing-indicator");
      bubble.classList.add("bot-bubble");
      bubble.innerHTML = marked.parse(answer);
      // ✅ Ajouter le bouton copier
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

// ====== Toast notifications ======
function showToast(message) {
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
  }, 3000);
}

// ====== Menu contextuel conversation ======
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
      try {
        const url = `${API_BASE_URL}/sessions/${encodeURIComponent(sessionName)}/rename?new_name=${encodeURIComponent(newName)}`;
        console.log("API RENAME URL:", url);

        const res = await fetch(url, { method: "PUT" });
        console.log("RENAME status:", res.status);

        if (res.ok) {
          await loadSessions();               // recharge la sidebar
          currentSession = newName;           // mettre à jour la session active
          setActiveSession(newName);          // repère visuel
          await loadHistory(newName);         // recharger l'historique
          showToast(`Session renommée en "${newName}" ✅`);
        }
        else {
          const txt = await res.text();
          console.error("Erreur API rename:", txt);
          showToast("⚠️ Erreur API lors du renommage");
        }
      } catch (err) {
        console.error("Erreur JS renommer :", err);
        showToast("⚠️ Erreur lors du renommage");
      }
    }
    menu.remove();
  });

  // --- Supprimer ---
  const del = document.createElement("div");
  del.textContent = "Supprimer";
  del.addEventListener("click", async () => {
    if (confirm(`Supprimer la conversation "${sessionName}" ?`)) {
      try {
        const url = `${API_BASE_URL}/sessions/${encodeURIComponent(sessionName)}`;
        console.log("API DELETE URL:", url);

        const res = await fetch(url, { method: "DELETE" });
        console.log("DELETE status:", res.status);

        if (res.ok) {
          await loadSessions();
          if (currentSession === sessionName) {
            await createSession();
          }
          showToast(`Session "${sessionName}" supprimée 🗑️`);
        } else {
          const txt = await res.text();
          console.error("Erreur API delete:", txt);
          showToast("⚠️ Erreur API lors de la suppression");
        }
      } catch (err) {
        console.error("Erreur JS suppression :", err);
        showToast("⚠️ Erreur lors de la suppression");
      }
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

// ====== Events & Init ======
window.addEventListener("DOMContentLoaded", async () => {
  // Vérifie Ollama AVANT toute initialisation
  await checkOllama();

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

  sendBtn.addEventListener("click", handleSend);
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  });

  if (newSessionBtn) {
    newSessionBtn.addEventListener("click", () => {
      createSession();
    });
  }

  // ⚠️ Ne crée une session que si Ollama est disponible
  if (!document.querySelector(".error-banner")) {
    await createSession();
  }
});