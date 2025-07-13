// ExperimentalTab.js
export default function ExperimentalTab(containerId) {
  const el = (typeof containerId === 'string') ? document.getElementById(containerId) : containerId;
  if (!el) return;

  el.innerHTML = `
    <div class="row">
      <div class="col-12">
        <h3>Experimental Features</h3>
        <p class="text-muted text-warning">⚠️ These features are experimental and may be unstable.</p>
      </div>
      
      <div class="col-md-4">
        <div class="card bg-secondary mb-3">
          <div class="card-header">Mutation Watcher</div>
          <div class="card-body">
            <button class="btn btn-danger" onclick="startMutationWatcher()">Start Watcher</button>
            <button class="btn btn-secondary ms-2" onclick="stopMutationWatcher()">Stop</button>
            <div id="mutationWatcherStatus" class="mt-2">Loading...</div>
          </div>
        </div>
      </div>
      
      <div class="col-md-4">
        <div class="card bg-secondary mb-3">
          <div class="card-header">New Agents</div>
          <div class="card-body">
            <select id="newAgentSelect" class="form-control mb-2">
              <option value="">Select new agent...</option>
            </select>
            <button class="btn btn-success" onclick="testNewAgent()">Test Agent</button>
            <div id="newAgentOutput" class="mt-2"></div>
          </div>
        </div>
      </div>
      
      <div class="col-md-4">
        <div class="card bg-secondary mb-3">
          <div class="card-header">Broken Scrapers</div>
          <div class="card-body">
            <div id="brokenScrapersList" class="mb-2">Loading...</div>
            <button class="btn btn-warning" onclick="refreshBrokenScrapers()">Refresh List</button>
          </div>
        </div>
      </div>
      
      <div class="col-12">
        <div class="card bg-secondary">
          <div class="card-header">Experimental Output</div>
          <div class="card-body">
            <div id="experimentalOutput">No experimental features executed yet.</div>
          </div>
        </div>
      </div>
    </div>
  `;

  // Define global functions for button handlers
  window.startMutationWatcher = () => {
    fetch('/api/experimental/mutation_watcher', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        document.getElementById('mutationWatcherStatus').innerHTML = `
          <div class="alert alert-info">Mutation watcher started</div>
        `;
        document.getElementById('experimentalOutput').innerHTML = `
          <div class="alert alert-success">
            <strong>Mutation Watcher:</strong><br>
            <pre>${JSON.stringify(data, null, 2)}</pre>
          </div>
        `;
      })
      .catch(err => {
        document.getElementById('mutationWatcherStatus').innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
      });
  };

  window.stopMutationWatcher = () => {
    fetch('/api/experimental/mutation_watcher', { method: 'DELETE' })
      .then(res => res.json())
      .then(data => {
        document.getElementById('mutationWatcherStatus').innerHTML = `<div class="alert alert-secondary">Mutation watcher stopped</div>`;
      })
      .catch(err => {
        document.getElementById('mutationWatcherStatus').innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
      });
  };

  window.testNewAgent = () => {
    const agent = document.getElementById('newAgentSelect').value;
    if (!agent) {
      document.getElementById('newAgentOutput').innerHTML = '<div class="alert alert-warning">Please select an agent to test.</div>';
      return;
    }

    fetch('/api/experimental/new_agents', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({agent})
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById('newAgentOutput').innerHTML = `<div class="alert alert-info">Agent tested: ${agent}</div>`;
      document.getElementById('experimentalOutput').innerHTML = `
        <div class="alert alert-success">
          <strong>New Agent Test Result:</strong><br>
          <pre>${JSON.stringify(data, null, 2)}</pre>
        </div>
      `;
    })
    .catch(err => {
      document.getElementById('newAgentOutput').innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
    });
  };

  window.refreshBrokenScrapers = () => {
    fetch('/api/experimental/broken_scrapers')
      .then(res => res.json())
      .then(data => {
        const scrapers = data.scrapers || [];
        if (scrapers.length === 0) {
          document.getElementById('brokenScrapersList').innerHTML = '<small class="text-success">No broken scrapers found!</small>';
        } else {
          document.getElementById('brokenScrapersList').innerHTML = scrapers.map(scraper => `
            <div class="alert alert-warning py-1">
              <small><strong>${scraper.name}</strong>: ${scraper.status}</small>
            </div>
          `).join('');
        }
      })
      .catch(err => {
        document.getElementById('brokenScrapersList').innerHTML = `<small class="text-danger">Error loading scrapers: ${err.message}</small>`;
      });
  };

  // Load initial data
  fetch('/api/experimental/mutation_watcher')
    .then(res => res.json())
    .then(data => {
      document.getElementById('mutationWatcherStatus').innerHTML = `<small>Status: ${data.status || 'Stopped'}</small>`;
    })
    .catch(err => {
      document.getElementById('mutationWatcherStatus').innerHTML = '<small class="text-danger">Error loading status</small>';
    });

  fetch('/api/experimental/new_agents')
    .then(res => res.json())
    .then(data => {
      const agents = data.agents || [];
      const select = document.getElementById('newAgentSelect');
      select.innerHTML = '<option value="">Select new agent...</option>' + 
        agents.map(agent => `<option value="${agent.name}">${agent.name} - ${agent.description}</option>`).join('');
    })
    .catch(err => {
      document.getElementById('newAgentSelect').innerHTML = '<option value="">Error loading agents</option>';
    });

  window.refreshBrokenScrapers();
}
