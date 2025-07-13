// ScreenView.jsx — View and interact with live screen stream (API-aligned)

import React, { useRef } from 'react';
import { sendMouse } from './api';
import './theme.css';

function ScreenView() {
  const screenRef = useRef(null);

  const handleTouch = (e) => {
    const bounds = screenRef.current.getBoundingClientRect();
    const touch = e.touches[0];

    const x = Math.round((touch.clientX - bounds.left) * window.devicePixelRatio);
    const y = Math.round((touch.clientY - bounds.top) * window.devicePixelRatio);
    const click = e.type === "touchend";

    sendMouse(x, y, click);
  };

  return (
    <div className="screen-container">
      <img
        src={`http://${window.location.hostname}:5901/`}
        alt="Live Desktop"
        ref={screenRef}
        onTouchStart={handleTouch}
        onTouchEnd={handleTouch}
        style={{ width: "100%", height: "auto", backgroundColor: "#000" }}
      />
      <p className="tip">🔒 Tap screen to click • Drag to move</p>
    </div>
  );
}

export default ScreenView;