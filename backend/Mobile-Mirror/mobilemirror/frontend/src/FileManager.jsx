// FileManager.jsx — Minimal filesystem explorer using api.js

import React, { useEffect, useState } from 'react';
import { getFiles } from './api';
import './theme.css';

function FileManager() {
  const [currentPath, setCurrentPath] = useState(".");
  const [items, setItems] = useState([]);

  useEffect(() => {
    loadFiles(currentPath);
  }, [currentPath]);

  const loadFiles = (path) => {
    getFiles(path).then(data => {
      if (data.items) {
        setItems(data.items);
      }
    });
  };

  const handleClick = (item) => {
    if (item.type === "dir") {
      setCurrentPath(item.path);
    } else {
      window.dispatchEvent(new CustomEvent("file-load", {
        detail: { path: item.path }
      }));
    }
  };

  return (
    <div className="file-manager">
      <h3>📁 {currentPath}</h3>
      <ul>
        {items.map((item, idx) => (
          <li key={idx}>
            <button
              className={`file-item ${item.type}`}
              onClick={() => handleClick(item)}
            >
              {item.type === "dir" ? "📂" : "📄"} {item.name}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default FileManager;