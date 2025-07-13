// Editor.jsx — Monaco-based code editor for TouchCore (API-aligned)

import React, { useEffect, useRef, useState } from 'react';
import * as monaco from 'monaco-editor';
import { readFile, writeFile } from './api';
import './theme.css';

function Editor() {
  const editorRef = useRef(null);
  const monacoRef = useRef(null);
  const [filePath, setFilePath] = useState("/home/user/sample.py");

  useEffect(() => {
    monacoRef.current = monaco.editor.create(editorRef.current, {
      value: "// Loading...",
      language: "python",
      theme: "vs-dark",
      automaticLayout: true
    });

    loadFile(filePath);

    return () => {
      if (monacoRef.current) monacoRef.current.dispose();
    };
  }, [filePath]);

  const loadFile = async (path) => {
    const res = await readFile(path);
    if (res.content) {
      monacoRef.current.setValue(res.content);
    }
  };

  const saveFile = async () => {
    const content = monacoRef.current.getValue();
    const res = await writeFile(filePath, content);
    if (res.status === "success") {
      alert("💾 Saved successfully.");
    } else {
      alert("❌ Save failed.");
    }
  };

  return (
    <div className="editor-panel">
      <input
        type="text"
        value={filePath}
        onChange={(e) => setFilePath(e.target.value)}
        placeholder="/path/to/file.py"
        className="editor-path-input"
      />
      <button onClick={saveFile} className="save-button">💾 Save</button>
      <div ref={editorRef} style={{ height: "80vh", width: "100%" }} />
    </div>
  );
}

export default Editor;