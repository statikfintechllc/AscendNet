export default function TaskTreeView(targetId) {
  const el = document.getElementById(targetId);
  el.innerHTML = `
    <div class="card bg-secondary">
      <div class="card-header">Task Tree</div>
      <div class="card-body" id="taskList">Loading...</div>
    </div>
  `;

  function fetchTasks() {
    fetch("/api/agent/tasks")
      .then(res => res.json())
      .then(data => {
        const html = data.tasks.map(t => `<li>${t.type} - ${t.status}</li>`).join("");
        document.getElementById("taskList").innerHTML = `<ul>${html}</ul>`;
      });
  }

  fetchTasks();
  setInterval(fetchTasks, 5000);
}

