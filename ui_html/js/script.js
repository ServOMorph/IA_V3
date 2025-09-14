// ui_html/js/script.js

const API_BASE_URL = "http://127.0.0.1:8000";

async function saveMessageToServer(role, content) {
  if (!currentSession) {
    console.warn("Pas de session active, message non sauvegardé");
    return;
  }
  const msg = {
    role: role,
    content: content,
    timestamp: new Date().toISOString()
  };
  try {
    await fetch(`${API_BASE_URL}/sessions/${currentSession}/message`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(msg)
    });
  } catch (err) {
    console.error("Erreur sauvegarde message:", err);
  }
}

let currentSession = null;

// ====== Utils DOM ======
function addMessage(text, sender = "bot", isTyping = false) {
  const chatBox = document.getElementById("chat-box");
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);

  if (sender === "bot") {
    const wrapper = document.createElement("div");
    wrapper.classList.add("bot-message-wrapper");

    const logo = document.createElement("img");
    logo.src = "assets/images/logo_vertia_seul.png";
    logo.alt = "IA";
    logo.classList.add("bot-logo");

    const bubble = document.createElement("div");
    if (isTyping) {
      bubble.classList.add("typing-indicator");
      bubble.textContent = "...";
    } else {
      bubble.classList.add("bot-bubble");
      bubble.textContent = text;
    }

    wrapper.appendChild(logo);
    wrapper.appendChild(bubble);
    msgDiv.appendChild(wrapper);

  } else if (sender === "user") {
    const wrapper = document.createElement("div");
    wrapper.classList.add("user-message-wrapper");

    const logo = document.createElement("img");
    logo.src = "assets/images/logo_user.png";
    logo.alt = "User";
    logo.classList.add("user-logo");

    const bubble = document.createElement("div");
    bubble.classList.add("user-bubble");
    bubble.textContent = text;

    wrapper.appendChild(logo);
    wrapper.appendChild(bubble);
    msgDiv.appendChild(wrapper);
  }

  chatBox.appendChild(msgDiv);
  chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: "smooth" });

  // 🔹 Sauvegarde automatique côté serveur (sauf bulle typing)
  if (!isTyping) {
    saveMessageToServer(sender, text);
  }

  return msgDiv; // on renvoie l'élément pour pouvoir le remplacer
}

function clearChat() {
  document.getElementById("chat-box").innerHTML = "";
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
  if (!res.ok) throw new Error(`GET ${path} failed`);
  return res.json();
}

async function apiPost(path, body = {}) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`POST ${path} failed`);
  return res.json();
}

// ====== Sessions ======
async function loadSessions() {
  try {
    const res = await apiGet("/sessions");   // renvoie { sessions: [...] }
    const sessions = res.sessions;           // extraire la liste
    const list = document.querySelector(".conv-list");
    list.innerHTML = "";

    sessions.forEach(s => {
      const li = document.createElement("li");
      li.textContent = s;
      li.dataset.session = s;
      li.addEventListener("click", () => loadHistory(s));
      list.appendChild(li);
    });

    // bouton "Nouvelle conversation"
    const liNew = document.createElement("li");
    liNew.textContent = "Nouvelle conversation";
    liNew.classList.add("new-session");
    liNew.addEventListener("click", createSession);
    list.appendChild(liNew);

  } catch (err) {
    console.error("Erreur chargement sessions", err);
  }
}

async function createSession() {
  try {
    const data = await apiPost("/sessions");   // renvoie { session: "sav_conv_..." }
    currentSession = data.session;             // mettre à jour la session active
    await loadSessions();
    await loadHistory(currentSession);
  } catch (err) {
    console.error("Erreur création session", err);
  }
}

async function loadHistory(sessionName) {
  try {
    const history = await apiGet(`/sessions/${sessionName}/history`);
    clearChat();
    setActiveSession(sessionName);
    history.forEach(msg => {
      addMessage(msg.role === "user" ? msg.content : msg.answer, msg.role);
    });
  } catch (err) {
    console.error("Erreur chargement historique", err);
  }
}

// ====== Chat ======
async function apiSendMessage(prompt) {
  const res = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt })
  });
  if (!res.ok) throw new Error("Erreur API");
  return res.json(); // { answer: "..." }
}

async function sendMessage(prompt) {
  if (!currentSession) {
    await createSession();
  }

  // Message user
  addMessage(prompt, "user");

  // Bulle "IA est en train d'écrire"
  const typingMsg = addMessage("", "bot", true);

  try {
    const data = await apiSendMessage(prompt);
    const answer = data.answer ?? "⚠️ Pas de réponse";

    const bubble = typingMsg.querySelector(".typing-indicator") 
               || typingMsg.querySelector(".bot-bubble");

    if (bubble) {
      bubble.classList.remove("typing-indicator");
      bubble.classList.add("bot-bubble");
      bubble.textContent = answer;

      // 🔹 Sauvegarde automatique de la réponse IA
      saveMessageToServer("assistant", answer);
    }
  } catch (err) {
    console.error(err);
    const bubble = typingMsg.querySelector("div");
    if (bubble) bubble.textContent = "⚠️ Erreur API";
  }
}

// ====== Events ======
document.getElementById("send-btn").addEventListener("click", async () => {
  const input = document.getElementById("chat-input");
  const text = input.value.trim();
  if (!text) return;

  input.value = "";
  await sendMessage(text);
});

document.getElementById("chat-input").addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    document.getElementById("send-btn").click();
  }
});

// ====== Init ======
loadSessions();
