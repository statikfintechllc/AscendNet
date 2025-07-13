import ChatInterface from './components/ChatInterface.js';
import TaskTreeView from './components/TaskTreeView.js';
import MemoryGraph from './components/MemoryGraph.js';
import TradingPanel from './components/TradingPanel.js';
import RewardFeedView from './components/RewardFeedView.js';

window.onload = function () {
  // Tab Navigation
  document.getElementById('gremlin-app-root').innerHTML = `
    <nav>
      <ul class="nav nav-tabs justify-content-center mb-4">
        <li class="nav-item"><a class="nav-link active" id="tab-tasks" href="#">Tasks</a></li>
        <li class="nav-item"><a class="nav-link" id="tab-memory" href="#">Memory</a></li>
        <li class="nav-item"><a class="nav-link" id="tab-trading" href="#">Trading</a></li>
        <li class="nav-item"><a class="nav-link" id="tab-reward" href="#">Reward Feed</a></li>
      </ul>
    </nav>
    <div id="tab-content" class="section-card"></div>
  `;

  // Tab logic
  function showTab(tab) {
    const tabContent = document.getElementById('tab-content');
    document.querySelectorAll('.nav-link').forEach(e => e.classList.remove('active'));
    document.getElementById('tab-' + tab).classList.add('active');

    if (tab === "tasks") TaskTreeView('tab-content');
    if (tab === "memory") MemoryGraph('tab-content');
    if (tab === "trading") TradingPanel('tab-content');
    if (tab === "reward") RewardFeedView('tab-content');
  }
  showTab('tasks');
  document.getElementById('tab-tasks').onclick = e => {e.preventDefault(); showTab('tasks');};
  document.getElementById('tab-memory').onclick = e => {e.preventDefault(); showTab('memory');};
  document.getElementById('tab-trading').onclick = e => {e.preventDefault(); showTab('trading');};
  document.getElementById('tab-reward').onclick = e => {e.preventDefault(); showTab('reward');};

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
