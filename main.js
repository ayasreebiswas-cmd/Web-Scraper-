document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('scrape-form');
  const submitBtn = document.getElementById('submit-btn');
  const statusBox = document.getElementById('status-box');
  const tableBody = document.getElementById('table-body');
  const countTag = document.getElementById('count-tag');
  const filterInput = document.getElementById('table-filter');

  let currentItems = [];

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const url = document.getElementById('target-url').value;
    const limit = document.getElementById('item-limit').value;

    toggleLoading(true);
    updateStatus('Connecting and extraction in progress...', 'info');

    try {
      const res = await fetch('/api/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, limit })
      });

      const payload = await res.json();

      if (res.ok && payload.status === 'success') {
        currentItems = payload.data;
        updateStatus(`Done. Extracted ${payload.count} item(s).`, 'success');
        renderRows(currentItems);
      } else {
        updateStatus(payload.message || 'Scrape task failed.', 'error');
      }
    } catch (err) {
      console.error(err);
      updateStatus('Server error occurred during fetch.', 'error');
    } finally {
      toggleLoading(false);
    }
  });

  if (filterInput) {
    filterInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase().trim();
      const filtered = currentItems.filter(item => 
        (item.title && item.title.toLowerCase().includes(query)) ||
        (item.price && item.price.toLowerCase().includes(query))
      );
      renderRows(filtered, true);
    });
  }

  function toggleLoading(isLoading) {
    submitBtn.disabled = isLoading;
    submitBtn.textContent = isLoading ? 'Running...' : 'Run Scraper';
  }

  function updateStatus(msg, type) {
    statusBox.textContent = msg;
    statusBox.className = `alert ${type}`;
  }

  function renderRows(items, isFiltering = false) {
    if (!isFiltering) {
      countTag.textContent = `${items.length} items`;
    }

    if (!items || items.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="6" class="empty-cell">No items to display.</td>
        </tr>`;
      return;
    }

    tableBody.innerHTML = items.map((item, idx) => {
      const stockIn = item.availability && item.availability.toLowerCase().includes('in');
      const stockClass = stockIn ? 'in' : 'out';

      return `
        <tr>
          <td class="col-idx">${idx + 1}</td>
          <td class="col-title" title="${escapeHtml(item.title)}">${escapeHtml(item.title)}</td>
          <td><span class="price-tag">${escapeHtml(item.price)}</span></td>
          <td><span class="stock-tag ${stockClass}">${escapeHtml(item.availability)}</span></td>
          <td>${escapeHtml(item.rating)}</td>
          <td>
            ${item.url && item.url !== 'N/A' 
              ? `<a href="${escapeHtml(item.url)}" target="_blank" class="item-link">View Product</a>`
              : '<span style="color:var(--text-muted)">N/A</span>'}
          </td>
        </tr>
      `;
    }).join('');
  }

  function escapeHtml(str) {
    return String(str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
});