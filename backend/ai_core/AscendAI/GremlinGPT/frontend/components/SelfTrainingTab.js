// SelfTrainingTab.js
export default function SelfTrainingTab(containerId) {
  const el = (typeof containerId === 'string') ? document.getElementById(containerId) : containerId;
  if (!el) return;

  el.innerHTML = `
    <div class="row">
      <div class="col-12">
        <h3>Self-Training & Autonomy</h3>
        <p class="text-muted">Manage mutation engine, feedback loops, and autonomous learning.</p>
      </div>
      
      <div class="col-md-6">
        <div class="card bg-secondary mb-3">
          <div class="card-header d-flex justify-content-between align-items-center">
            <span>Mutation Engine</span>
            <button class="btn btn-sm btn-danger" onclick="triggerMutation()">Trigger Mutation</button>
          </div>
          <div class="card-body" id="mutationStatus">Loading...</div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card bg-secondary mb-3">
          <div class="card-header d-flex justify-content-between align-items-center">
            <span>Feedback Loop</span>
            <button class="btn btn-sm btn-success" onclick="startFeedback()">Start Feedback</button>
          </div>
          <div class="card-body" id="feedbackStatus">Loading...</div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card bg-secondary mb-3">
          <div class="card-header d-flex justify-content-between align-items-center">
            <span>Retrain Scheduler</span>
            <button class="btn btn-sm btn-warning" onclick="scheduleRetrain()">Schedule Retrain</button>
          </div>
          <div class="card-body" id="retrainStatus">Loading...</div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card bg-secondary mb-3">
          <div class="card-header">Watcher/Autonomy</div>
          <div class="card-body" id="watcherStatus">Loading...</div>
        </div>
      </div>
    </div>
  `;

  // Define global functions for button handlers
  window.triggerMutation = () => {
    fetch('/api/self_training/mutate', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        document.getElementById('mutationStatus').innerHTML = `<div class="alert alert-info">${JSON.stringify(data)}</div>`;
      })
      .catch(err => {
        document.getElementById('mutationStatus').innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
      });
  };

  window.startFeedback = () => {
    fetch('/api/self_training/feedback', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        document.getElementById('feedbackStatus').innerHTML = `<div class="alert alert-success">${JSON.stringify(data)}</div>`;
      })
      .catch(err => {
        document.getElementById('feedbackStatus').innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
      });
  };

  window.scheduleRetrain = () => {
    fetch('/api/self_training/retrain', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        document.getElementById('retrainStatus').innerHTML = `<div class="alert alert-warning">${JSON.stringify(data)}</div>`;
      })
      .catch(err => {
        document.getElementById('retrainStatus').innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
      });
  };

  // Load initial status
  fetch('/api/self_training/status')
    .then(res => res.json())
    .then(data => {
      document.getElementById('mutationStatus').innerHTML = `<small>Status: ${data.mutation_status || 'Idle'}</small>`;
      document.getElementById('feedbackStatus').innerHTML = `<small>Status: ${data.feedback_status || 'Idle'}</small>`;
      document.getElementById('retrainStatus').innerHTML = `<small>Status: ${data.retrain_status || 'Idle'}</small>`;
      document.getElementById('watcherStatus').innerHTML = `<small>Status: ${data.watcher_status || 'Monitoring'}</small>`;
    })
    .catch(err => {
      ['mutationStatus', 'feedbackStatus', 'retrainStatus', 'watcherStatus'].forEach(id => {
        document.getElementById(id).innerHTML = '<small class="text-danger">Error loading status</small>';
      });
    });
}
