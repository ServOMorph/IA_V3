// js/api.js
// Gestion des appels API

import { CONFIG } from './config.js';

// Vérifier disponibilité du serveur Ollama
export async function checkOllama() {
  try {
    const res = await fetch(`${CONFIG.OLLAMA_URL}/api/tags`);
    if (!res.ok) throw new Error("HTTP " + res.status);
    console.log("Ollama serveur OK");
    return true;
  } catch (e) {
    console.error("Ollama indisponible:", e);
    return false;
  }
}

// Utilitaires API génériques
export async function apiGet(path) {
  const res = await fetch(`${CONFIG.API_BASE_URL}${path}`);
  if (!res.ok) throw new Error(`GET ${path} failed (${res.status})`);
  return res.json();
}

export async function apiPost(path, body = {}) {
  const res = await fetch(`${CONFIG.API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`POST ${path} failed (${res.status})`);
  return res.json();
}

export async function apiPut(path) {
  const res = await fetch(`${CONFIG.API_BASE_URL}${path}`, {
    method: "PUT"
  });
  if (!res.ok) throw new Error(`PUT ${path} failed (${res.status})`);
  return res.json();
}

export async function apiDelete(path) {
  const res = await fetch(`${CONFIG.API_BASE_URL}${path}`, {
    method: "DELETE"
  });
  if (!res.ok) throw new Error(`DELETE ${path} failed (${res.status})`);
  return res.json();
}

// API spécifique pour le chat
export async function sendChatMessage(sessionName, prompt) {
  const response = await fetch(`${CONFIG.API_BASE_URL}/chat/${sessionName}`, {
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