// ExecutorsTab.js
export default function ExecutorsTab(containerId) {
  const el = (typeof containerId === 'string') ? document.getElementById(containerId) : containerId;
  if (!el) return;

  el.innerHTML = `
    <div class="row">
      <div class="col-12">
        <h3>Code & Tool Executors</h3>
        <p class="text-muted">Execute Python code, shell commands, and custom tools.</p>
      </div>
      
      <div class="col-md-4">
        <div class="card bg-secondary mb-3">
          <div class="card-header">Python Executor</div>
          <div class="card-body">
            <textarea id="pythonCode" class="form-control mb-2" rows="4" placeholder="# Enter Python code here
print('Hello from GremlinGPT!')"></textarea>
            <button class="btn btn-primary" onclick="executePython()">Execute Python</button>
            <div id="pythonOutput" class="mt-2"></div>
          </div>
        </div>
      </div>
      
      <div class="col-md-4">
        <div class="card bg-secondary mb-3">
          <div class="card-header">Shell Executor</div>
          <div class="card-body">
            <input id="shellCommand" class="form-control mb-2" type="text" placeholder="ls -la" />
            <button class="btn btn-warning" onclick="executeShell()">Execute Shell</button>
            <div id="shellOutput" class="mt-2"></div>
          </div>
        </div>
      </div>
      
      <div class="col-md-4">
        <div class="card bg-secondary mb-3">
          <div class="card-header">Tool Executor</div>
          <div class="card-body">
            <select id="toolSelect" class="form-control mb-2">
              <option value="reward_model">Reward Model</option>
              <option value="custom_tool">Custom Tool</option>
            </select>
            <button class="btn btn-success" onclick="executeTool()">Execute Tool</button>
            <div id="toolOutput" class="mt-2"></div>
          </div>
        </div>
      </div>
    </div>
  `;

  // Define global functions for button handlers
  window.executePython = () => {
    const code = document.getElementById('pythonCode').value;
    fetch('/api/execute/python', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({code})
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById('pythonOutput').innerHTML = `
        <div class="alert alert-info">
          <strong>Output:</strong><br>
          <pre>${data.output || data.error}</pre>
        </div>
      `;
    })
    .catch(err => {
      document.getElementById('pythonOutput').innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
    });
  };

  window.executeShell = () => {
    const command = document.getElementById('shellCommand').value;
    fetch('/api/execute/shell', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({command})
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById('shellOutput').innerHTML = `
        <div class="alert alert-warning">
          <strong>Output:</strong><br>
          <pre>${data.output || data.error}</pre>
        </div>
      `;
    })
    .catch(err => {
      document.getElementById('shellOutput').innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
    });
  };

  window.executeTool = () => {
    const tool = document.getElementById('toolSelect').value;
    fetch('/api/execute/tool', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({tool})
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById('toolOutput').innerHTML = `
        <div class="alert alert-success">
          <strong>Tool Result:</strong><br>
          <pre>${JSON.stringify(data, null, 2)}</pre>
        </div>
      `;
    })
    .catch(err => {
      document.getElementById('toolOutput').innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
    });
  };
}
