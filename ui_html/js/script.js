// ui_html/js/script.js

const API_BASE_URL = "http://localhost:8001";
let currentSession = null;

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

    const bubble = document.createElement("div");
    bubble.classList.add(isTyping ? "typing-indicator" : "bot-bubble");
    bubble.textContent = isTyping ? "..." : text;

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
  return msgDiv;
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
      li.textContent = s;
      li.dataset.session = s;
      li.addEventListener("click", () => loadHistory(s));
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
        history.push({ role: currentRole, content: buffer.join("\n").trim() });
      }
      buffer = [];
      currentRole = null;
    }

    for (let line of lines) {
      const lineStripped = line.trim();
      if (!lineStripped) continue;

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

      if (lineStripped.startsWith("**Vous**")) {
        flushBuffer();
        currentRole = "user";
        continue;
      }
      if (lineStripped.startsWith("**IA**")) {
        flushBuffer();
        currentRole = "assistant";
        continue;
      }

      if (currentRole) buffer.push(lineStripped);
    }
    flushBuffer();

    history.forEach(msg => {
      addMessage(msg.content, msg.role);
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
      bubble.textContent = answer;
    }
  } catch (err) {
    console.error("Erreur envoi message :", err);
    const bubble = typingMsg.querySelector("div");
    if (bubble) bubble.textContent = "⚠️ Erreur API";
  }
}

// ====== Events & Init ======
window.addEventListener("DOMContentLoaded", async () => {
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

  await createSession();
});
