// Terminal.jsx — Live shell window with xterm.js over WebSocket

import React, { useEffect, useRef } from 'react';
import { Terminal } from 'xterm';
import 'xterm/css/xterm.css';

function TerminalView() {
  const termRef = useRef(null);
  const socketRef = useRef(null);

  useEffect(() => {
    const term = new Terminal({
      cols: 80,
      rows: 24,
      theme: {
        background: '#1e1e1e',
        foreground: '#ffffff'
      }
    });

    term.open(termRef.current);

    const socket = new WebSocket(`ws://${window.location.hostname}:8000/terminal`);
    socketRef.current = socket;

    socket.onmessage = (event) => {
      term.write(event.data);
    };

    term.onData((data) => {
      socket.send(data);
    });

    socket.onclose = () => {
      term.write('\r\n[Connection closed]');
    };

    return () => {
      term.dispose();
      socket.close();
    };
  }, []);

  return (
    <div className="terminal-wrapper">
      <div ref={termRef} style={{ height: "90vh", width: "100%", backgroundColor: "#000" }} />
    </div>
  );
}

export default TerminalView;