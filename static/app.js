const $ = (id) => document.getElementById(id);
let latestContent = null;

async function request(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || `Request failed (${response.status})`);
  return data;
}

async function checkHealth() {
  try {
    const health = await request('/api/health');
    $('status-dot').classList.toggle('good', health.ollama_reachable);
    $('status-text').textContent = health.ollama_reachable
      ? `Local AI · ${health.configured_model}`
      : 'Offline template mode · Ollama not detected';
  } catch {
    $('status-text').textContent = 'API status unavailable';
  }
}

function showView(which) {
  const isCreate = which === 'create';
  $('create-view').classList.toggle('hidden', !isCreate);
  $('history-view').classList.toggle('hidden', isCreate);
  $('nav-create').classList.toggle('active', isCreate);
  $('nav-history').classList.toggle('active', !isCreate);
  $('page-title').textContent = isCreate ? 'Make your next post easier.' : 'Your content, all in one place.';
  if (!isCreate) loadHistory();
}

$('nav-create').addEventListener('click', () => showView('create'));
$('nav-history').addEventListener('click', () => showView('history'));
$('refresh-history').addEventListener('click', loadHistory);

$('generate-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  $('error-box').classList.add('hidden');
  $('results').classList.add('hidden');
  const button = $('generate-btn');
  button.disabled = true;
  button.innerHTML = '<span>◌</span> Creating your content…';
  const payload = Object.fromEntries(['business_name','product','price','audience','tone','language','platform','details'].map(k => [k, $(k).value.trim()]));
  try {
    const result = await request('/api/generate', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    latestContent = result.content;
    Object.entries(result.content).forEach(([key, value]) => { $(`out-${key}`).textContent = value; });
    $('result-mode').textContent = result.mode === 'ollama' ? `Generated with ${result.model}` : 'Offline template · no model needed';
    $('results').classList.remove('hidden');
    $('results').scrollIntoView({behavior:'smooth', block:'start'});
    checkHealth();
  } catch (error) {
    $('error-box').textContent = error.message || 'Could not generate content. Please try again.';
    $('error-box').classList.remove('hidden');
  } finally {
    button.disabled = false;
    button.innerHTML = '<span>✳</span> Generate content <span>↗</span>';
  }
});

document.querySelectorAll('[data-copy]').forEach(button => {
  button.addEventListener('click', async () => {
    const value = latestContent?.[button.dataset.copy] || $(`out-${button.dataset.copy}`).textContent;
    try {
      await navigator.clipboard.writeText(value);
      const old = button.textContent;
      button.textContent = 'Copied ✓';
      setTimeout(() => button.textContent = old, 1200);
    } catch {
      window.prompt('Copy your content:', value);
    }
  });
});

async function loadHistory() {
  const container = $('history-list');
  container.innerHTML = '<div class="empty-state">Loading your content…</div>';
  try {
    const result = await request('/api/history?limit=50');
    if (!result.items.length) {
      container.innerHTML = '<div class="empty-state">No content saved yet. Generate your first content kit to see it here.</div>';
      return;
    }
    container.innerHTML = '';
    result.items.forEach(item => {
      const row = document.createElement('article');
      row.className = 'history-item';
      const left = document.createElement('div');
      const title = document.createElement('h3');
      title.textContent = item.product;
      const meta = document.createElement('p');
      meta.textContent = `${item.business_name} · ${item.platform} · ${item.language} · ${new Date(item.created_at).toLocaleString()}`;
      left.append(title, meta);
      const actions = document.createElement('div');
      actions.className = 'history-actions';
      const view = document.createElement('button');
      view.textContent = 'View content';
      view.addEventListener('click', () => {
        latestContent = item.content;
        Object.entries(item.content).forEach(([key, value]) => { $(`out-${key}`).textContent = value; });
        $('result-mode').textContent = item.mode === 'ollama' ? 'Generated with local AI' : 'Offline template';
        $('results').classList.remove('hidden');
        showView('create');
        $('results').scrollIntoView({behavior:'smooth'});
      });
      const remove = document.createElement('button');
      remove.textContent = 'Delete';
      remove.addEventListener('click', async () => {
        if (!confirm('Delete this saved content?')) return;
        try { await request(`/api/history/${item.id}`, {method:'DELETE'}); loadHistory(); }
        catch (error) { alert(error.message); }
      });
      actions.append(view, remove);
      row.append(left, actions);
      container.append(row);
    });
  } catch (error) {
    container.innerHTML = `<div class="error-box">${error.message}</div>`;
  }
}

checkHealth();
