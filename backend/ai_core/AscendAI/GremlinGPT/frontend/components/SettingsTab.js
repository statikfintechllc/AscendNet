// SettingsTab.js (System tab)
export default function SettingsTab(containerId) {
  const el = (typeof containerId === 'string') ? document.getElementById(containerId) : containerId;
  if (!el) return;

  el.innerHTML = `
    <div class="row">
      <div class="col-12">
        <h3>System Settings & Configuration</h3>
        <p class="text-muted">Manage system configuration, backend selection, and view logs.</p>
      </div>
      
      <div class="col-md-6">
        <div class="card bg-secondary mb-3">
          <div class="card-header">Backend Selection</div>
          <div class="card-body">
            <div class="form-group mb-2">
              <label>Vector Backend:</label>
              <select id="backendSelect" class="form-control">
                <option value="faiss">FAISS</option>
                <option value="chromadb">ChromaDB</option>
              </select>
            </div>
            <button class="btn btn-primary" onclick="updateBackend()">Update Backend</button>
            <button class="btn btn-info ms-2" onclick="loadBackendStatus()">Refresh Status</button>
            <div id="backendStatus" class="mt-2"></div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card bg-secondary mb-3">
          <div class="card-header">Ngrok Integration</div>
          <div class="card-body">
            <button class="btn btn-success" onclick="startNgrok()">Start Ngrok</button>
            <button class="btn btn-danger ms-2" onclick="stopNgrok()">Stop Ngrok</button>
            <div id="ngrokStatus" class="mt-2"></div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card bg-secondary mb-3">
          <div class="card-header">Log Viewer</div>
          <div class="card-body">
            <select id="logSelect" class="form-control mb-2">
              <option value="runtime.log">Runtime Log</option>
              <option value="backend.out">Backend Log</option>
              <option value="frontend.out">Frontend Log</option>
              <option value="install.log">Install Log</option>
            </select>
            <button class="btn btn-info" onclick="viewLogs()">View Logs</button>
          </div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card bg-secondary mb-3">
          <div class="card-header">Feature Coverage Report</div>
          <div class="card-body">
            <button class="btn btn-warning" onclick="generateCoverageReport()">Generate Report</button>
            <div id="coverageReport" class="mt-2"></div>
          </div>
        </div>
      </div>
      
      <div class="col-12">
        <div class="card bg-secondary">
          <div class="card-header">System Information</div>
          <div class="card-body" id="systemInfo">Loading...</div>
        </div>
      </div>
    </div>
  `;

  // Define global functions for button handlers
  window.updateBackend = () => {
    const backend = document.getElementById('backendSelect').value;
    fetch('/api/system/backend_select', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({backend})
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        document.getElementById('backendStatus').innerHTML = `
          <div class="alert alert-danger">Error: ${data.error}</div>
        `;
      } else {
        document.getElementById('backendStatus').innerHTML = `
          <div class="alert alert-success">Backend updated to: ${data.backend}</div>
        `;
        // Refresh status after update
        setTimeout(loadBackendStatus, 1000);
      }
    })
    .catch(err => {
      document.getElementById('backendStatus').innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
    });
  };

  window.loadBackendStatus = () => {
    fetch('/api/system/backend_status')
      .then(res => res.json())
      .then(data => {
        const statusHtml = `
          <div class="alert alert-info">
            <strong>Current Backend:</strong> ${data.current_backend}<br>
            <strong>FAISS Available:</strong> ${data.faiss_available ? 'Yes' : 'No'} 
            ${data.faiss_available ? `(${data.faiss_index_count} vectors)` : ''}<br>
            <strong>ChromaDB Available:</strong> ${data.chromadb_available ? 'Yes' : 'No'} 
            ${data.chromadb_available ? `(${data.chroma_collection_count} vectors)` : ''}
          </div>
        `;
        document.getElementById('backendStatus').innerHTML = statusHtml;
        
        // Update select to match current backend
        document.getElementById('backendSelect').value = data.current_backend;
      })
      .catch(err => {
        document.getElementById('backendStatus').innerHTML = `<div class="alert alert-warning">Status unavailable: ${err.message}</div>`;
      });
  };

  window.startNgrok = () => {
    fetch('/api/system/ngrok', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        document.getElementById('ngrokStatus').innerHTML = `
          <div class="alert alert-success">
            Ngrok started: <a href="${data.url}" target="_blank">${data.url}</a>
          </div>
        `;
      })
      .catch(err => {
        document.getElementById('ngrokStatus').innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
      });
  };

  window.stopNgrok = () => {
    fetch('/api/system/ngrok', { method: 'DELETE' })
      .then(res => res.json())
      .then(data => {
        document.getElementById('ngrokStatus').innerHTML = `<div class="alert alert-info">Ngrok stopped</div>`;
      })
      .catch(err => {
        document.getElementById('ngrokStatus').innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
      });
  };

  window.viewLogs = () => {
    const logFile = document.getElementById('logSelect').value;
    fetch(`/api/system/logs?file=${logFile}`)
      .then(res => res.json())
      .then(data => {
        document.getElementById('systemInfo').innerHTML = `
          <h5>Log: ${logFile}</h5>
          <pre class="bg-dark text-light p-3" style="max-height: 300px; overflow-y: auto;">${data.content || 'No content'}</pre>
        `;
      })
      .catch(err => {
        document.getElementById('systemInfo').innerHTML = `<div class="alert alert-danger">Error loading logs: ${err.message}</div>`;
      });
  };

  window.generateCoverageReport = () => {
    fetch('/api/system/feature_coverage')
      .then(res => res.json())
      .then(data => {
        const report = data.coverage || {};
        const totalFeatures = report.total || 0;
        const implementedFeatures = report.implemented || 0;
        const coverage = totalFeatures > 0 ? Math.round((implementedFeatures / totalFeatures) * 100) : 0;
        
        document.getElementById('coverageReport').innerHTML = `
          <div class="alert alert-info">
            <strong>Coverage:</strong> ${coverage}% (${implementedFeatures}/${totalFeatures})<br>
            <strong>Missing:</strong> ${(report.missing || []).join(', ') || 'None'}
          </div>
        `;
      })
      .catch(err => {
        document.getElementById('coverageReport').innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
      });
  };

  // Load initial system info and backend status
  fetch('/api/system/config')
    .then(res => res.json())
    .then(data => {
      document.getElementById('systemInfo').innerHTML = `
        <h5>System Configuration</h5>
        <pre class="bg-dark text-light p-3">${JSON.stringify(data, null, 2)}</pre>
      `;
      
      // Set current backend in dropdown
      if (data.memory && data.memory.dashboard_selected_backend) {
        document.getElementById('backendSelect').value = data.memory.dashboard_selected_backend;
      }
    })
    .catch(err => {
      document.getElementById('systemInfo').innerHTML = `<div class="alert alert-danger">Error loading config: ${err.message}</div>`;
    });

  // Load backend status
  loadBackendStatus();
}
