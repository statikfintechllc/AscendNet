export default function TradingPanel(targetId) {
  const el = document.getElementById(targetId);
  el.innerHTML = `
    <div class="card bg-secondary">
      <div class="card-header">Live Signals</div>
      <div class="card-body" id="signals">Loading...</div>
    </div>
  `;

  function fetchSignals() {
    fetch("/api/trading/signals")
      .then(res => res.json())
      .then(data => {
        const html = data.map(sig => `
          <div><b>${sig.symbol}</b> $${sig.price} | Signal: ${sig.signal}</div>
        `).join("");
        document.getElementById("signals").innerHTML = html;
      });
  }

  fetchSignals();
  setInterval(fetchSignals, 2000);
}

