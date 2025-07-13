import ChatInterface from './components/ChatInterface.js';
import TaskTreeView from './components/TaskTreeView.js';
import MemoryGraph from './components/MemoryGraph.js';
import TradingPanel from './components/TradingPanel.js';
import RewardFeedView from './components/RewardFeedView.js';
import SelfTrainingTab from './components/SelfTrainingTab.js';
import ExecutorsTab from './components/ExecutorsTab.js';
import ToolsTab from './components/ToolsTab.js';
import SettingsTab from './components/SettingsTab.js';
import ExperimentalTab from './components/ExperimentalTab.js';

window.onload = function () {
  // Tab Navigation
  document.getElementById('gremlin-app-root').innerHTML = `
    <nav>
      <ul class="nav nav-tabs justify-content-center mb-4">
        <li class="nav-item"><a class="nav-link active" id="tab-chat" href="#">Chat</a></li>
        <li class="nav-item"><a class="nav-link" id="tab-tasks" href="#">Tasks</a></li>
        <li class="nav-item"><a class="nav-link" id="tab-memory" href="#">Memory</a></li>
        <li class="nav-item"><a class="nav-link" id="tab-trading" href="#">Trading</a></li>
        <li class="nav-item"><a class="nav-link" id="tab-scraping" href="#">Scraping</a></li>
        <li class="nav-item"><a class="nav-link" id="tab-self-training" href="#">Self-Training</a></li>
        <li class="nav-item"><a class="nav-link" id="tab-executors" href="#">Executors</a></li>
        <li class="nav-item"><a class="nav-link" id="tab-tools" href="#">Tools</a></li>
        <li class="nav-item"><a class="nav-link" id="tab-system" href="#">System</a></li>
        <li class="nav-item"><a class="nav-link" id="tab-experimental" href="#">Experimental</a></li>
      </ul>
    </nav>
    <div id="tab-content" class="section-card"></div>
  `;

  // Tab logic
  function showTab(tab) {
    const tabContent = document.getElementById('tab-content');
    document.querySelectorAll('.nav-link').forEach(e => e.classList.remove('active'));
    document.getElementById('tab-' + tab).classList.add('active');

    if (tab === "chat") ChatInterface('tab-content');
    if (tab === "tasks") TaskTreeView('tab-content');
    if (tab === "memory") MemoryGraph('tab-content');
    if (tab === "trading") TradingPanel('tab-content');
    if (tab === "scraping") RewardFeedView('tab-content');
    if (tab === "self-training") SelfTrainingTab('tab-content');
    if (tab === "executors") ExecutorsTab('tab-content');
    if (tab === "tools") ToolsTab('tab-content');
    if (tab === "system") SettingsTab('tab-content');
    if (tab === "experimental") ExperimentalTab('tab-content');
  }
  showTab('chat');
  document.getElementById('tab-chat').onclick = e => {e.preventDefault(); showTab('chat');};
  document.getElementById('tab-tasks').onclick = e => {e.preventDefault(); showTab('tasks');};
  document.getElementById('tab-memory').onclick = e => {e.preventDefault(); showTab('memory');};
  document.getElementById('tab-trading').onclick = e => {e.preventDefault(); showTab('trading');};
  document.getElementById('tab-scraping').onclick = e => {e.preventDefault(); showTab('scraping');};
  document.getElementById('tab-self-training').onclick = e => {e.preventDefault(); showTab('self-training');};
  document.getElementById('tab-executors').onclick = e => {e.preventDefault(); showTab('executors');};
  document.getElementById('tab-tools').onclick = e => {e.preventDefault(); showTab('tools');};
  document.getElementById('tab-system').onclick = e => {e.preventDefault(); showTab('system');};
  document.getElementById('tab-experimental').onclick = e => {e.preventDefault(); showTab('experimental');};

  // Chat FAB (always bottom-right)
  document.body.insertAdjacentHTML("beforeend", `<div id="gremlin-chat-fab" title="Open Chat">💬</div>
    <div id="gremlin-chat-modal"><div id="gremlin-chat-content"></div><div id="gremlin-chat-close">&times;</div></div>`);
  document.getElementById('gremlin-chat-fab').onclick = () => {
    document.getElementById('gremlin-chat-modal').classList.add('active');
    ChatInterface('gremlin-chat-content');
  };
  document.getElementById('gremlin-chat-close').onclick = () => {
    document.getElementById('gremlin-chat-modal').classList.remove('active');
  };

  // Chat bar (fixed bottom, always clickable)
  document.getElementById('gremlin-chat-bar').innerHTML =
    `<span><img src="App_Icon_&_Loading_&_Inference_Image.png" style="height:32px;vertical-align:middle;margin-right:12px;">Talk to GremlinGPT (click icon)</span>`;
};
