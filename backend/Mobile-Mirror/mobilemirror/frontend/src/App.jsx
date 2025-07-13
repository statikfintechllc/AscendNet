// App.jsx — TouchCore root frontend shell
import React, { useState } from 'react';
import Terminal from './Terminal';
import Editor from './Editor';
import FileManager from './FileManager';
import ScreenView from './ScreenView';
import './theme.css';

function App() {
  const [activeTab, setActiveTab] = useState("screen");

  return (
    <div className="app-container">
      <header>
        <h1>TouchCore</h1>
        <nav>
          <button onClick={() => setActiveTab("screen")}>🖥️ Screen</button>
          <button onClick={() => setActiveTab("terminal")}>💻 Terminal</button>
          <button onClick={() => setActiveTab("editor")}>🧠 Editor</button>
          <button onClick={() => setActiveTab("files")}>📁 Files</button>
        </nav>
      </header>

      <main>
        {activeTab === "screen" && <ScreenView />}
        {activeTab === "terminal" && <Terminal />}
        {activeTab === "editor" && <Editor />}
        {activeTab === "files" && <FileManager />}
      </main>
    </div>
  );
}

export default App;