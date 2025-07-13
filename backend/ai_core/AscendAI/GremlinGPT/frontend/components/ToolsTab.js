// ToolsTab.js
export default function ToolsTab(containerId) {
  const el = (typeof containerId === 'string') ? document.getElementById(containerId) : containerId;
  if (!el) return;

  el.innerHTML = `
    <div class="row">
      <div class="col-12">
        <h3>Tools & Models</h3>
        <p class="text-muted">Access reward models and custom tools.</p>
      </div>
      
      <div class="col-md-6">
        <div class="card bg-secondary mb-3">
          <div class="card-header">Reward Model</div>
          <div class="card-body">
            <textarea id="rewardInput" class="form-control mb-2" rows="3" placeholder="Enter task description or output to score..."></textarea>
            <button class="btn btn-primary" onclick="runRewardModel()">Score with Reward Model</button>
            <div id="rewardOutput" class="mt-2"></div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card bg-secondary mb-3">
          <div class="card-header">Custom Tools</div>
          <div class="card-body">
            <div class="mb-2">
              <label>Available Tools:</label>
              <div id="customToolsList">Loading...</div>
            </div>
            <button class="btn btn-success" onclick="refreshTools()">Refresh Tools</button>
          </div>
        </div>
      </div>
      
      <div class="col-12">
        <div class="card bg-secondary">
          <div class="card-header">Tool Output</div>
          <div class="card-body">
            <div id="toolResults">No tools executed yet.</div>
          </div>
        </div>
      </div>
    </div>
  `;

  // Define global functions for button handlers
  window.runRewardModel = () => {
    const input = document.getElementById('rewardInput').value;
    if (!input.trim()) {
      document.getElementById('rewardOutput').innerHTML = '<div class="alert alert-warning">Please enter some text to score.</div>';
      return;
    }

    fetch('/api/tools/reward_model', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({input})
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById('rewardOutput').innerHTML = `
        <div class="alert alert-info">
          <strong>Reward Score:</strong> ${data.score || 'N/A'}<br>
          <strong>Confidence:</strong> ${data.confidence || 'N/A'}<br>
          <strong>Reasoning:</strong> ${data.reasoning || 'N/A'}
        </div>
      `;
      document.getElementById('toolResults').innerHTML = `
        <div class="alert alert-success">
          <strong>Reward Model Result:</strong><br>
          <pre>${JSON.stringify(data, null, 2)}</pre>
        </div>
      `;
    })
    .catch(err => {
      document.getElementById('rewardOutput').innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
    });
  };

  window.refreshTools = () => {
    fetch('/api/tools/custom')
      .then(res => res.json())
      .then(data => {
        const tools = data.tools || [];
        if (tools.length === 0) {
          document.getElementById('customToolsList').innerHTML = '<small class="text-muted">No custom tools available.</small>';
        } else {
          document.getElementById('customToolsList').innerHTML = tools.map(tool => `
            <div class="form-check">
              <input class="form-check-input" type="checkbox" value="${tool.name}" id="tool-${tool.name}">
              <label class="form-check-label" for="tool-${tool.name}">
                ${tool.name} - ${tool.description || 'No description'}
              </label>
            </div>
          `).join('');
        }
      })
      .catch(err => {
        document.getElementById('customToolsList').innerHTML = `<small class="text-danger">Error loading tools: ${err.message}</small>`;
      });
  };

  // Load initial tools list
  window.refreshTools();
}
