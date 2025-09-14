// ui_html/js/script.js

const API_BASE_URL = "http://127.0.0.1:8000";

let currentSession = null;

// ====== Utils DOM ======
function addMessage(text, sender = "bot") {
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
    bubble.classList.add("bot-bubble");
    bubble.textContent = text;

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

    wrapper.appendChild(logo);   // logo à gauche
    wrapper.appendChild(bubble); // bulle à droite
    msgDiv.appendChild(wrapper);
    }


  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
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
    const sessions = await apiGet("/sessions");
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
    const data = await apiPost("/sessions");
    await loadSessions();
    loadHistory(data.name);
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
async function sendMessage(prompt) {
  if (!currentSession) {
    await createSession();
  }
  addMessage(prompt, "user");
  try {
    const data = await apiPost("/chat", { prompt });
    addMessage(data.answer, "bot");
  } catch (err) {
    console.error("Erreur envoi prompt", err);
    addMessage("⚠️ Erreur API", "bot");
  }
}

// ====== Events ======
document.getElementById("send-btn").addEventListener("click", () => {
  const input = document.getElementById("chat-input");
  const text = input.value.trim();
  if (!text) return;
  sendMessage(text);
  input.value = "";
});

document.getElementById("chat-input").addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    document.getElementById("send-btn").click();
  }
});

// ====== Init ======
loadSessions();
