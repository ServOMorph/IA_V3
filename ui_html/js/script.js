document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const input = document.getElementById("chat-input");
  const sendBtn = document.getElementById("send-btn");

  // Fonction pour afficher un message
function addMessage(sender, text) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;

  if (sender === "bot") {
    const wrapper = document.createElement("div");
    wrapper.className = "bot-message-wrapper";

    const logo = document.createElement("img");
    logo.src = "../assets/images/logo_vertia_seul.png";
    logo.alt = "IA";
    logo.className = "bot-logo";

    const bubble = document.createElement("div");
    bubble.className = "bot-bubble";
    bubble.textContent = text;

    wrapper.appendChild(logo);
    wrapper.appendChild(bubble);
    div.appendChild(wrapper);
  } else {
    div.textContent = text;
  }

  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

  // Fonction pour envoyer un message
  function sendMessage() {
    const text = input.value.trim();
    if (text !== "") {
      addMessage("user", text);
      input.value = "";
      autoResize(); // reset hauteur

      // Réponse bot simulée
      setTimeout(() => {
        addMessage("bot", "Réponse mock de l’IA : " + text);
      }, 500);
    }
  }

  // Bouton Envoyer
  sendBtn.addEventListener("click", sendMessage);

  // Gestion clavier : Enter = envoyer, Shift+Enter = retour à la ligne
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      if (e.shiftKey) {
        return; // permet saut de ligne
      } else {
        e.preventDefault();
        sendMessage();
      }
    }
  });

  // Auto-ajustement hauteur textarea avec limite max
function autoResize() {
  const style = getComputedStyle(input);
  const lineHeight = parseFloat(style.lineHeight);
  const maxLines = parseInt(getComputedStyle(document.documentElement).getPropertyValue("--max-lines")) || 6;
  const maxHeight = lineHeight * maxLines;

  // Reset provisoire sur une ligne
  input.style.height = lineHeight + "px";

  // Calculer la hauteur réelle du texte (scrollHeight inclut padding → on soustrait)
  const padding = parseFloat(style.paddingTop) + parseFloat(style.paddingBottom);
  let newHeight = input.scrollHeight - padding;

  // Tant qu’on n’a pas forcé un retour ligne ou wrap → rester sur une ligne
  if (!input.value.includes("\n") && input.scrollWidth <= input.clientWidth) {
    newHeight = lineHeight;
  }

  // Appliquer limite
  newHeight = Math.min(newHeight, maxHeight);
  input.style.height = newHeight + "px";
  input.style.overflowY = (newHeight >= maxHeight) ? "auto" : "hidden";
}

  input.addEventListener("input", autoResize);

  // Messages mock au chargement
  const messages = [
    { sender: "user", text: "Bonjour, IA !" },
    { sender: "bot", text: "💬 Session de chat démarrée (mock)." },
    { sender: "user", text: "Quelle est la capitale de la France ?" },
    { sender: "bot", text: "La capitale est Paris." }
  ];
  messages.forEach(msg => addMessage(msg.sender, msg.text));
});
