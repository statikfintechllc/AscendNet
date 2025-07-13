// api.js — Unified fetch wrapper for TouchCore frontend (auth-ready)

const API_HOST = `http://${window.location.hostname}:8000`;
const TOKEN = localStorage.getItem("TOUCHCORE_TOKEN") || "touchcore-access";

const defaultHeaders = {
  "Content-Type": "application/json",
  "Authorization": TOKEN
};

export async function getFiles(path = ".") {
  const res = await fetch(`${API_HOST}/files?path=${encodeURIComponent(path)}`, {
    headers: defaultHeaders
  });
  return await res.json();
}

export async function readFile(path) {
  const res = await fetch(`${API_HOST}/read`, {
    method: "POST",
    headers: defaultHeaders,
    body: JSON.stringify({ path })
  });
  return await res.json();
}

export async function writeFile(path, content) {
  const res = await fetch(`${API_HOST}/write`, {
    method: "POST",
    headers: defaultHeaders,
    body: JSON.stringify({ path, content })
  });
  return await res.json();
}

export async function sendMouse(x, y, click = false) {
  return await fetch(`${API_HOST}/mouse`, {
    method: "POST",
    headers: defaultHeaders,
    body: JSON.stringify({ x, y, click })
  });
}

export async function getQR() {
  const res = await fetch(`${API_HOST}/qr`);
  return await res.json();
}