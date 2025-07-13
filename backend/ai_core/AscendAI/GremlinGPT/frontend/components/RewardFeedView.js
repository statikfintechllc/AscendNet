// RewardFeedView.js
export default function RewardFeedView(containerId) {
  const el = (typeof containerId === 'string') ? document.getElementById(containerId) : containerId;
  if (!el) return;
  el.innerHTML = '<div class="loading">Loading reward/diff feed...</div>';
  fetch('/api/dashboard/reward_feed?n=20')
    .then(res => res.json())
    .then(data => {
      const feed = data.reward_feed || [];
      if (feed.length === 0) {
        el.innerHTML = '<p>No recent reward/diff events.</p>';
        return;
      }
      el.innerHTML = feed.map(item => `
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
      el.innerHTML = '<p style="color:red">Error loading reward feed.</p>';
    });
}
