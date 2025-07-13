// Fetch and render reward+diff dashboard feed
fetch('/api/dashboard/reward_feed?n=10')
  .then(res => res.json())
  .then(data => {
    const feed = data.reward_feed || [];
    const container = document.getElementById('reward-feed');
    if (!container) return;
    if (feed.length === 0) {
      container.innerHTML = '<p>No recent reward/diff events.</p>';
      return;
    }
    container.innerHTML = feed.map(item => `
      <div class="reward-card">
        <div><b>Task:</b> ${item.task}</div>
        <div><b>Reward:</b> ${item.reward} <b>Conf:</b> ${item.confidence}</div>
        <div><b>Reason:</b> ${item.reason}</div>
        <div><b>Semantic:</b> ${item.semantic_score ?? ''} <b>Δ:</b> ${item.embedding_delta ?? ''}</div>
        <div><b>Output:</b> <pre>${item.output}</pre></div>
        ${item.diff_lines ? `<details><summary>Diff</summary><pre>${item.diff_lines.join('')}</pre></details>` : ''}
        <div class="timestamp">${item.timestamp}</div>
      </div>
    `).join('');
  })
  .catch(err => {
    const container = document.getElementById('reward-feed');
    if (container) container.innerHTML = '<p style="color:red">Error loading reward feed.</p>';
  });
