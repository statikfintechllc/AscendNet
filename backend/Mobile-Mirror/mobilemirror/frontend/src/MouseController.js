// MouseController.js — Handles advanced mobile gestures for TouchCore

export function bindTouchToMouse(element, options = {}) {
  const scale = options.scale || window.devicePixelRatio || 1;

  element.addEventListener("touchstart", (e) => {
    const touch = e.touches[0];
    sendMouseEvent(touch, scale, false);
  });

  element.addEventListener("touchmove", (e) => {
    const touch = e.touches[0];
    sendMouseEvent(touch, scale, false);
  });

  element.addEventListener("touchend", (e) => {
    const touch = e.changedTouches[0];
    sendMouseEvent(touch, scale, true);
  });
}

function sendMouseEvent(touch, scale, click) {
  const bounds = touch.target.getBoundingClientRect();
  const x = Math.round((touch.clientX - bounds.left) * scale);
  const y = Math.round((touch.clientY - bounds.top) * scale);

  fetch("http://localhost:8000/mouse", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ x, y, click })
  });
}