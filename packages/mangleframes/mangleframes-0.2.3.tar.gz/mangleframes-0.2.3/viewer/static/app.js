const state = {
    currentFrame: null,
    columns: [],
    rows: [],
    total: 0,
    offset: 0,
    limit: 100,
    sortCol: null,
    sortDir: 'asc',
    searchTerm: '',
    loading: false,
    preloadComplete: false,
    tableHeight: null,
    sectionOrder: ['section-stats', 'section-quality', 'section-sql', 'section-join'],
    dqxAvailable: false,
    qualityRules: {},
    qualityResults: null,
    qualitySuggestions: null
};

const $ = id => document.getElementById(id);

function showLoadingOverlay() {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.innerHTML = `
        <div class="spinner"></div>
        <p>Connecting to Spark...</p>
    `;
    document.body.appendChild(overlay);
}

function hideLoadingOverlay() {
    const overlay = $('loading-overlay');
    if (overlay) overlay.remove();
}

async function checkPreloadStatus() {
    try {
        const data = await fetchJSON('/api/status');
        state.preloadComplete = data.ready;
        if (!data.ready) {
            showLoadingOverlay();
        }
    } catch (e) {
        // Status endpoint unavailable, proceed normally
        state.preloadComplete = true;
    }
}

async function fetchJSON(url, options = {}) {
    const res = await fetch(url, options);
    if (!res.ok) {
        const err = await res.json().catch(() => ({ error: res.statusText }));
        throw new Error(err.error || 'Request failed');
    }
    return res.json();
}

async function loadFrames() {
    try {
        const data = await fetchJSON('/api/frames');
        const select = $('frame-select');
        select.innerHTML = '<option value="">Select DataFrame...</option>';
        data.frames.forEach(name => {
            const opt = document.createElement('option');
            opt.value = name;
            opt.textContent = name;
            select.appendChild(opt);
        });
    } catch (e) {
        showError('Failed to load frames: ' + e.message);
    }
}

async function loadSchema(name) {
    const data = await fetchJSON(`/api/frames/${name}/schema`);
    state.columns = data.columns || [];
    renderHeader();
}

async function loadData(name, offset = 0) {
    if (state.loading) return;
    state.loading = true;

    const startTime = performance.now();
    let timerInterval = null;

    if (offset === 0) {
        timerInterval = setInterval(() => {
            const elapsed = ((performance.now() - startTime) / 1000).toFixed(1);
            $('load-status').textContent = `Waiting for Databricks... ${elapsed}s`;
        }, 100);
    } else {
        $('load-status').textContent = 'Loading more...';
    }

    try {
        const url = `/api/frames/${name}/data?offset=${offset}&limit=${state.limit}`;
        const data = await fetchJSON(url);

        if (timerInterval) clearInterval(timerInterval);
        const totalElapsed = ((performance.now() - startTime) / 1000).toFixed(2);

        if (offset === 0) {
            state.rows = data.rows;
        } else {
            state.rows = state.rows.concat(data.rows);
        }
        state.total = data.total;
        state.offset = offset + data.rows.length;

        renderRows();
        updateStatus();

        if (data.timing && offset === 0) {
            const { spark_ms, local_ms, cached } = data.timing;
            if (cached) {
                $('load-status').textContent = 'Loaded from cache';
            } else {
                const spark_s = (spark_ms / 1000).toFixed(2);
                const local_s = (local_ms / 1000).toFixed(2);
                $('load-status').textContent =
                    `Spark: ${spark_s}s | Local: ${local_s}s | Total: ${totalElapsed}s`;
            }
        } else {
            $('load-status').textContent = '';
        }
    } catch (e) {
        if (timerInterval) clearInterval(timerInterval);
        showError('Failed to load data: ' + e.message);
        $('load-status').textContent = '';
    } finally {
        state.loading = false;
    }
}

async function loadStats(name) {
    try {
        const data = await fetchJSON(`/api/frames/${name}/stats`);
        renderStats(data);
    } catch (e) {
        $('stats-content').innerHTML = `<p class="error">${e.message}</p>`;
    }
}

function renderHeader() {
    const thead = $('table-head');
    thead.innerHTML = '';
    const tr = document.createElement('tr');

    state.columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col.name;
        th.dataset.col = col.name;
        th.title = `${col.type}${col.nullable ? ' (nullable)' : ''}`;

        if (state.sortCol === col.name) {
            th.className = state.sortDir === 'asc' ? 'sorted-asc' : 'sorted-desc';
        }

        th.onclick = () => toggleSort(col.name);
        tr.appendChild(th);
    });

    thead.appendChild(tr);
}

function renderRows() {
    const tbody = $('table-body');
    tbody.innerHTML = '';

    let rows = state.rows;

    if (state.searchTerm) {
        const term = state.searchTerm.toLowerCase();
        rows = rows.filter(row =>
            Object.values(row).some(v =>
                String(v).toLowerCase().includes(term)
            )
        );
    }

    if (state.sortCol) {
        rows = [...rows].sort((a, b) => {
            const av = a[state.sortCol];
            const bv = b[state.sortCol];
            if (av === null) return 1;
            if (bv === null) return -1;
            const cmp = av < bv ? -1 : av > bv ? 1 : 0;
            return state.sortDir === 'asc' ? cmp : -cmp;
        });
    }

    rows.forEach(row => {
        const tr = document.createElement('tr');
        state.columns.forEach(col => {
            const td = document.createElement('td');
            const val = row[col.name];
            if (val === null) {
                td.textContent = 'null';
                td.className = 'null';
            } else {
                td.textContent = String(val);
                td.title = String(val);
            }
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

function renderStats(data) {
    const container = $('stats-content');
    container.innerHTML = '';

    const rowCard = document.createElement('div');
    rowCard.className = 'stat-card';
    rowCard.innerHTML = `<h4>Total Rows</h4><p>${data.row_count?.toLocaleString() || 'N/A'}</p>`;
    container.appendChild(rowCard);

    if (data.columns) {
        data.columns.forEach(col => {
            const card = document.createElement('div');
            card.className = 'stat-card';
            let html = `<h4>${col.name}</h4>`;
            html += `<p>Type: ${col.type}</p>`;
            html += `<p>Nulls: ${col.null_count?.toLocaleString() || 0}</p>`;
            if (col.min !== undefined) html += `<p>Min: ${col.min}</p>`;
            if (col.max !== undefined) html += `<p>Max: ${col.max}</p>`;
            card.innerHTML = html;
            container.appendChild(card);
        });
    }
}

function toggleSort(colName) {
    if (state.sortCol === colName) {
        state.sortDir = state.sortDir === 'asc' ? 'desc' : 'asc';
    } else {
        state.sortCol = colName;
        state.sortDir = 'asc';
    }
    renderHeader();
    renderRows();
}

function updateStatus() {
    const showing = state.searchTerm ? 'filtered' : state.rows.length;
    $('row-count').textContent = `Showing ${showing} of ${state.total.toLocaleString()} rows`;
}

function showError(msg) {
    const tbody = $('table-body');
    tbody.innerHTML = `<tr><td colspan="${state.columns.length || 1}" class="error">${msg}</td></tr>`;
}

async function exportData(format) {
    if (!state.currentFrame) return;

    try {
        const res = await fetch(`/api/frames/${state.currentFrame}/export`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ format })
        });

        if (!res.ok) throw new Error('Export failed');

        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${state.currentFrame}.${format}`;
        a.click();
        URL.revokeObjectURL(url);
    } catch (e) {
        alert('Export failed: ' + e.message);
    }
}

async function runSQL() {
    const sql = $('sql-input').value.trim();
    if (!sql) return;

    const resultDiv = $('sql-result');
    resultDiv.innerHTML = '<p class="loading">Running query...</p>';

    try {
        const data = await fetchJSON('/api/query', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sql })
        });

        if (data.rows.length === 0) {
            resultDiv.innerHTML = '<p>No results</p>';
            return;
        }

        const cols = Object.keys(data.rows[0]);
        let html = '<table><thead><tr>';
        cols.forEach(c => html += `<th>${c}</th>`);
        html += '</tr></thead><tbody>';

        data.rows.forEach(row => {
            html += '<tr>';
            cols.forEach(c => {
                const v = row[c];
                html += v === null
                    ? '<td class="null">null</td>'
                    : `<td>${v}</td>`;
            });
            html += '</tr>';
        });

        html += '</tbody></table>';
        html += `<p style="margin-top:8px;font-size:12px;color:var(--text-muted)">${data.total} rows</p>`;
        resultDiv.innerHTML = html;
    } catch (e) {
        resultDiv.innerHTML = `<p class="error">${e.message}</p>`;
    }
}

function setupInfiniteScroll() {
    const container = $('table-container');
    container.addEventListener('scroll', () => {
        if (state.loading || state.offset >= state.total) return;

        const { scrollTop, scrollHeight, clientHeight } = container;
        if (scrollTop + clientHeight >= scrollHeight - 100) {
            loadData(state.currentFrame, state.offset);
        }
    });
}

function loadTableHeight() {
    const saved = localStorage.getItem('mangleframes-table-height');
    if (saved) {
        state.tableHeight = parseInt(saved, 10);
        applyTableHeight();
    }
}

function applyTableHeight() {
    const container = $('table-container');
    if (state.tableHeight) {
        container.style.setProperty('--table-height', `${state.tableHeight}px`);
    }
}

function saveTableHeight() {
    if (state.tableHeight) {
        localStorage.setItem('mangleframes-table-height', state.tableHeight);
    }
}

function setupResizeHandle() {
    const handle = $('resize-handle');
    const container = $('table-container');
    let startY, startHeight;

    handle.addEventListener('mousedown', (e) => {
        e.preventDefault();
        startY = e.clientY;
        startHeight = container.offsetHeight;
        handle.classList.add('dragging');
        document.addEventListener('mousemove', onDrag);
        document.addEventListener('mouseup', onDragEnd);
    });

    function onDrag(e) {
        const delta = e.clientY - startY;
        const newHeight = Math.max(150, startHeight + delta);
        state.tableHeight = newHeight;
        applyTableHeight();
    }

    function onDragEnd() {
        handle.classList.remove('dragging');
        document.removeEventListener('mousemove', onDrag);
        document.removeEventListener('mouseup', onDragEnd);
        saveTableHeight();
    }
}

function loadSectionOrder() {
    const saved = localStorage.getItem('mangleframes-section-order');
    if (saved) {
        try {
            const order = JSON.parse(saved);
            if (Array.isArray(order) && order.length >= 3) {
                // Ensure section-quality is included
                if (!order.includes('section-quality')) {
                    order.splice(1, 0, 'section-quality');
                }
                state.sectionOrder = order;
            }
        } catch (e) {
            // Invalid JSON, use default
        }
    }
    applySectionOrder();
}

function saveSectionOrder() {
    localStorage.setItem('mangleframes-section-order', JSON.stringify(state.sectionOrder));
}

function applySectionOrder() {
    const main = document.querySelector('main');
    const statusBar = document.querySelector('.status-bar');

    state.sectionOrder.forEach(id => {
        const section = $(id);
        if (section) {
            main.insertBefore(section, null);
        }
    });
}

function setupSectionDrag() {
    let draggedSection = null;

    document.querySelectorAll('.drag-handle').forEach(handle => {
        handle.addEventListener('dragstart', (e) => {
            draggedSection = handle.closest('details');
            draggedSection.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/plain', draggedSection.id);
        });

        handle.addEventListener('dragend', () => {
            if (draggedSection) {
                draggedSection.classList.remove('dragging');
                draggedSection = null;
            }
            document.querySelectorAll('details.drag-over').forEach(el => {
                el.classList.remove('drag-over');
            });
        });
    });

    state.sectionOrder.forEach(id => {
        const section = $(id);
        if (!section) return;

        section.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            if (draggedSection && section !== draggedSection) {
                section.classList.add('drag-over');
            }
        });

        section.addEventListener('dragleave', () => {
            section.classList.remove('drag-over');
        });

        section.addEventListener('drop', (e) => {
            e.preventDefault();
            section.classList.remove('drag-over');

            if (!draggedSection || section === draggedSection) return;

            const draggedId = draggedSection.id;
            const targetId = section.id;

            const draggedIdx = state.sectionOrder.indexOf(draggedId);
            const targetIdx = state.sectionOrder.indexOf(targetId);

            if (draggedIdx === -1 || targetIdx === -1) return;

            state.sectionOrder.splice(draggedIdx, 1);
            state.sectionOrder.splice(targetIdx, 0, draggedId);

            applySectionOrder();
            saveSectionOrder();
        });
    });
}

function setupWebSocket() {
    const ws = new WebSocket(`ws://${location.host}/ws`);

    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.type === 'refresh') {
            loadFrames();
        } else if (msg.type === 'preload_complete') {
            state.preloadComplete = true;
            hideLoadingOverlay();
            loadFrames().then(() => {
                if (msg.frame) {
                    $('frame-select').value = msg.frame;
                    $('frame-select').dispatchEvent(new Event('change'));
                }
            });
        }
    };

    ws.onclose = () => setTimeout(setupWebSocket, 3000);
}

function init() {
    loadTableHeight();
    loadSectionOrder();
    setupResizeHandle();
    setupSectionDrag();
    checkPreloadStatus();
    loadFrames();
    setupInfiniteScroll();
    setupWebSocket();
    initJoinAnalysis();
    initQuality();
    initReconciliation();

    $('frame-select').onchange = async (e) => {
        const name = e.target.value;
        if (!name) return;

        state.currentFrame = name;
        state.rows = [];
        state.offset = 0;
        state.sortCol = null;
        clearQualityResults();

        // Fetch schema and data in parallel for faster display
        await Promise.all([loadSchema(name), loadData(name)]);
        loadStats(name);  // Fire-and-forget, updates UI when ready
        updateQualityButtons();
        renderQualityConfig();
    };

    $('refresh-btn').onclick = () => {
        loadFrames();
        populateJoinFrameSelectors();
        if (state.currentFrame) {
            state.rows = [];
            state.offset = 0;
            loadData(state.currentFrame);
        }
    };

    $('search-input').oninput = (e) => {
        state.searchTerm = e.target.value;
        renderRows();
        updateStatus();
    };

    document.querySelectorAll('.export-buttons button').forEach(btn => {
        btn.onclick = () => exportData(btn.dataset.format);
    });

    $('run-sql').onclick = runSQL;
    $('sql-input').onkeydown = (e) => {
        if (e.ctrlKey && e.key === 'Enter') runSQL();
    };
}

// Join Analysis Module
const joinState = {
    leftFrame: null,
    rightFrame: null,
    leftKeys: [],
    rightKeys: [],
    leftColumns: [],
    rightColumns: [],
    currentSide: 'left',
    unmatched: { left: [], right: [] },
    unmatchedTotal: { left: 0, right: 0 },
    offset: 0,
    limit: 100,
    // History analysis extensions
    additionalFrames: [],
    bucketSize: 'month',
    coverageData: null
};

function initJoinAnalysis() {
    populateJoinFrameSelectors();
    setupJoinEventListeners();
    setupHistoryEventListeners();
}

async function populateJoinFrameSelectors() {
    try {
        const data = await fetchJSON('/api/frames');
        ['join-left-frame', 'join-right-frame'].forEach(id => {
            const select = $(id);
            select.innerHTML = '<option value="">Select frame...</option>';
            data.frames.forEach(name => {
                const opt = document.createElement('option');
                opt.value = name;
                opt.textContent = name;
                select.appendChild(opt);
            });
        });
    } catch (e) {
        console.error('Failed to load frames for join:', e);
    }
}

function setupJoinEventListeners() {
    console.log('[JOIN DEBUG] Setup:', { left: $('join-left-frame'), right: $('join-right-frame') });
    $('join-left-frame').onchange = (e) => {
        console.log('[JOIN DEBUG] Left frame selected:', e.target.value);
        loadColumnsForJoin('left', e.target.value);
    };
    $('join-right-frame').onchange = (e) => {
        console.log('[JOIN DEBUG] Right frame selected:', e.target.value);
        loadColumnsForJoin('right', e.target.value);
    };
    $('analyze-join').onclick = runJoinAnalysis;

    document.querySelectorAll('.viewer-tabs .tab').forEach(tab => {
        tab.onclick = () => switchUnmatchedTab(tab.dataset.side);
    });

    $('prev-page').onclick = () => paginateUnmatched(-1);
    $('next-page').onclick = () => paginateUnmatched(1);

    document.querySelectorAll('.unmatched-viewer .export-group button').forEach(btn => {
        btn.onclick = () => exportUnmatched(btn.dataset.format);
    });
}

async function loadColumnsForJoin(side, frameName) {
    if (!frameName) {
        joinState[side + 'Columns'] = [];
        joinState[side + 'Keys'] = [];
        renderColumnChips(side);
        return;
    }

    try {
        const schema = await fetchJSON(`/api/frames/${frameName}/schema`);
        joinState[side + 'Frame'] = frameName;
        joinState[side + 'Columns'] = schema.columns || [];
        joinState[side + 'Keys'] = [];
        renderColumnChips(side);
    } catch (e) {
        console.error(`Failed to load schema for ${frameName}:`, e);
    }
}

function renderColumnChips(side) {
    const parent = $(`${side}-columns`);
    const container = parent?.querySelector('.column-chips');
    console.log('[JOIN DEBUG] Container:', { side, parent, container, columns: joinState[side + 'Columns']?.length });
    if (!container) return;
    container.innerHTML = '';

    const columns = joinState[side + 'Columns'];
    const selectedKeys = joinState[side + 'Keys'];

    columns.forEach(col => {
        const chip = document.createElement('span');
        chip.className = 'column-chip';
        chip.dataset.column = col.name;

        const idx = selectedKeys.indexOf(col.name);
        if (idx >= 0) {
            chip.classList.add('selected');
            chip.innerHTML = `<span class="chip-order">${idx + 1}</span>${col.name}`;
        } else {
            chip.textContent = col.name;
        }

        chip.onclick = () => toggleKeyColumn(side, col.name);
        container.appendChild(chip);
    });
}

function toggleKeyColumn(side, colName) {
    const keys = joinState[side + 'Keys'];
    const idx = keys.indexOf(colName);

    if (idx >= 0) {
        keys.splice(idx, 1);
    } else {
        keys.push(colName);
    }

    renderColumnChips(side);
}

async function runJoinAnalysis() {
    const { leftFrame, rightFrame, leftKeys, rightKeys } = joinState;

    if (!leftFrame || !rightFrame) {
        alert('Please select both frames');
        return;
    }
    if (leftKeys.length === 0 || rightKeys.length === 0) {
        alert('Please select join keys for both frames');
        return;
    }
    if (leftKeys.length !== rightKeys.length) {
        alert('Key counts must match between frames');
        return;
    }

    const btn = $('analyze-join');
    btn.disabled = true;
    btn.textContent = 'Analyzing...';

    try {
        const result = await fetchJSON('/api/join/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                left_frame: leftFrame,
                right_frame: rightFrame,
                left_keys: leftKeys,
                right_keys: rightKeys
            })
        });

        displayJoinStatistics(result.statistics);
        joinState.unmatched.left = result.left_unmatched.rows;
        joinState.unmatched.right = result.right_unmatched.rows;
        joinState.unmatchedTotal.left = result.left_unmatched.total;
        joinState.unmatchedTotal.right = result.right_unmatched.total;

        $('tab-left-count').textContent = result.left_unmatched.total.toLocaleString();
        $('tab-right-count').textContent = result.right_unmatched.total.toLocaleString();

        $('join-stats').style.display = 'block';
        $('unmatched-viewer').style.display = 'block';

        switchUnmatchedTab('left');
    } catch (e) {
        alert('Analysis failed: ' + e.message);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Analyze Join';
    }
}

function displayJoinStatistics(stats) {
    const matchPct = (stats.match_rate_left * 100).toFixed(1) + '%';
    $('stat-match-rate').textContent = matchPct;
    $('stat-cardinality').textContent = stats.cardinality;

    $('stat-left-total').textContent = stats.left_total.toLocaleString();
    $('stat-left-unmatched').textContent = (stats.left_total - stats.matched_left).toLocaleString();
    $('stat-left-nulls').textContent = stats.left_null_keys.toLocaleString();
    $('stat-left-dupes').textContent = stats.left_duplicate_keys.toLocaleString();

    $('stat-right-total').textContent = stats.right_total.toLocaleString();
    $('stat-right-unmatched').textContent = (stats.right_total - stats.matched_right).toLocaleString();
    $('stat-right-nulls').textContent = stats.right_null_keys.toLocaleString();
    $('stat-right-dupes').textContent = stats.right_duplicate_keys.toLocaleString();
}

function switchUnmatchedTab(side) {
    joinState.currentSide = side;
    joinState.offset = 0;

    document.querySelectorAll('.viewer-tabs .tab').forEach(t => {
        t.classList.toggle('active', t.dataset.side === side);
    });

    renderUnmatchedTable();
}

function renderUnmatchedTable() {
    const side = joinState.currentSide;
    const rows = joinState.unmatched[side];
    const total = joinState.unmatchedTotal[side];

    const thead = $('unmatched-head');
    const tbody = $('unmatched-body');

    if (!rows || rows.length === 0) {
        thead.innerHTML = '';
        tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;padding:20px;">No unmatched rows</td></tr>';
        $('unmatched-status').textContent = 'No unmatched rows';
        $('prev-page').disabled = true;
        $('next-page').disabled = true;
        return;
    }

    const cols = Object.keys(rows[0]);
    thead.innerHTML = '<tr>' + cols.map(c => `<th>${c}</th>`).join('') + '</tr>';

    tbody.innerHTML = rows.map(row =>
        '<tr>' + cols.map(c => {
            const v = row[c];
            return v === null
                ? '<td class="null">null</td>'
                : `<td title="${v}">${v}</td>`;
        }).join('') + '</tr>'
    ).join('');

    $('unmatched-status').textContent =
        `Showing ${joinState.offset + 1}-${joinState.offset + rows.length} of ${total.toLocaleString()} unmatched`;

    $('prev-page').disabled = joinState.offset === 0;
    $('next-page').disabled = joinState.offset + rows.length >= total;
}

async function paginateUnmatched(direction) {
    const newOffset = joinState.offset + (direction * joinState.limit);
    if (newOffset < 0) return;

    joinState.offset = newOffset;
    await fetchUnmatchedPage();
}

async function fetchUnmatchedPage() {
    const { leftFrame, rightFrame, leftKeys, rightKeys, currentSide, offset, limit } = joinState;

    const params = new URLSearchParams({
        left_frame: leftFrame,
        right_frame: rightFrame,
        left_keys: leftKeys.join(','),
        right_keys: rightKeys.join(','),
        offset: offset,
        limit: limit
    });

    try {
        const result = await fetchJSON(`/api/join/unmatched/${currentSide}?${params}`);
        joinState.unmatched[currentSide] = result.rows;
        joinState.unmatchedTotal[currentSide] = result.total;
        renderUnmatchedTable();
    } catch (e) {
        console.error('Failed to fetch unmatched rows:', e);
    }
}

async function exportUnmatched(format) {
    const { leftFrame, rightFrame, leftKeys, rightKeys, currentSide } = joinState;

    try {
        const res = await fetch('/api/join/export', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                left_frame: leftFrame,
                right_frame: rightFrame,
                left_keys: leftKeys,
                right_keys: rightKeys,
                side: currentSide,
                format
            })
        });

        if (!res.ok) throw new Error('Export failed');

        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${currentSide}_unmatched.${format}`;
        a.click();
        URL.revokeObjectURL(url);
    } catch (e) {
        alert('Export failed: ' + e.message);
    }
}

// History Coverage Analysis Module
function setupHistoryEventListeners() {
    $('add-frame-btn').onclick = addAdditionalFrame;
    $('analyze-history').onclick = runHistoryAnalysis;
    $('bucket-size').onchange = (e) => {
        joinState.bucketSize = e.target.value;
    };
}

function addAdditionalFrame() {
    if (joinState.additionalFrames.length >= 3) {
        alert('Maximum 5 frames total (2 primary + 3 additional)');
        return;
    }

    joinState.additionalFrames.push({
        frame: null,
        targetFrame: null,
        sourceKeys: [],
        targetKeys: [],
        columns: [],
        targetColumns: []
    });

    renderAdditionalFrames();
}

async function renderAdditionalFrames() {
    const container = $('additional-frames-list');
    container.innerHTML = '';

    const data = await fetchJSON('/api/frames').catch(() => ({ frames: [] }));
    const allFrames = data.frames || [];

    joinState.additionalFrames.forEach((af, idx) => {
        const div = document.createElement('div');
        div.className = 'additional-frame-row';
        div.innerHTML = buildAdditionalFrameHtml(idx, af, allFrames);
        container.appendChild(div);

        div.querySelector('.source-frame-select').onchange = (e) => {
            loadAdditionalFrameColumns(idx, e.target.value);
        };
        div.querySelector('.target-frame-select').onchange = (e) => {
            loadTargetFrameColumns(idx, e.target.value);
        };
        div.querySelector('.remove-frame-btn').onclick = () => removeAdditionalFrame(idx);

        if (af.frame) renderAdditionalFrameKeyMapping(idx);
    });
}

function buildAdditionalFrameHtml(idx, af, allFrames) {
    const targetOptions = getAvailableTargetFrames(idx);
    return `
        <div class="additional-frame-header">
            <select class="source-frame-select" data-idx="${idx}">
                <option value="">Select frame...</option>
                ${allFrames.map(f => `<option value="${f}" ${af.frame === f ? 'selected' : ''}>${f}</option>`).join('')}
            </select>
            <span class="join-arrow">joins</span>
            <select class="target-frame-select" data-idx="${idx}">
                <option value="">Select target...</option>
                ${targetOptions.map(f => `<option value="${f}" ${af.targetFrame === f ? 'selected' : ''}>${f}</option>`).join('')}
            </select>
            <button class="remove-frame-btn" data-idx="${idx}" title="Remove">×</button>
        </div>
        <div class="key-mapping-section" id="key-mapping-${idx}">
            <div class="source-keys-picker">
                <span class="picker-label">Source Keys</span>
                <div class="column-chips" id="source-chips-${idx}"></div>
            </div>
            <div class="target-keys-picker">
                <span class="picker-label">Target Keys</span>
                <div class="column-chips" id="target-chips-${idx}"></div>
            </div>
        </div>
    `;
}

function getAvailableTargetFrames(currentIdx) {
    const targets = [];
    if (joinState.leftFrame) targets.push(joinState.leftFrame);
    if (joinState.rightFrame) targets.push(joinState.rightFrame);
    joinState.additionalFrames.forEach((af, i) => {
        if (i < currentIdx && af.frame) targets.push(af.frame);
    });
    return targets;
}

async function loadAdditionalFrameColumns(idx, frameName) {
    const af = joinState.additionalFrames[idx];
    if (!frameName) {
        Object.assign(af, { frame: null, sourceKeys: [], columns: [] });
        renderAdditionalFrameKeyMapping(idx);
        return;
    }

    try {
        const schema = await fetchJSON(`/api/frames/${frameName}/schema`);
        Object.assign(af, {
            frame: frameName,
            columns: schema.columns || [],
            sourceKeys: []
        });
        renderAdditionalFrameKeyMapping(idx);
    } catch (e) {
        console.error(`Failed to load schema for ${frameName}:`, e);
    }
}

async function loadTargetFrameColumns(idx, targetFrameName) {
    const af = joinState.additionalFrames[idx];
    if (!targetFrameName) {
        Object.assign(af, { targetFrame: null, targetKeys: [], targetColumns: [] });
        renderAdditionalFrameKeyMapping(idx);
        return;
    }

    try {
        const schema = await getTargetFrameSchema(targetFrameName);
        Object.assign(af, {
            targetFrame: targetFrameName,
            targetColumns: schema.columns || [],
            targetKeys: []
        });
        renderAdditionalFrameKeyMapping(idx);
    } catch (e) {
        console.error(`Failed to load target schema for ${targetFrameName}:`, e);
    }
}

async function getTargetFrameSchema(frameName) {
    if (frameName === joinState.leftFrame && joinState.leftColumns.length > 0) {
        return { columns: joinState.leftColumns };
    }
    if (frameName === joinState.rightFrame && joinState.rightColumns.length > 0) {
        return { columns: joinState.rightColumns };
    }
    const existing = joinState.additionalFrames.find(af => af.frame === frameName);
    if (existing && existing.columns.length > 0) {
        return { columns: existing.columns };
    }
    return await fetchJSON(`/api/frames/${frameName}/schema`);
}

function renderAdditionalFrameKeyMapping(idx) {
    const af = joinState.additionalFrames[idx];
    renderKeyChips(`source-chips-${idx}`, af.columns, af.sourceKeys, (col) => toggleSourceKey(idx, col));
    renderKeyChips(`target-chips-${idx}`, af.targetColumns, af.targetKeys, (col) => toggleTargetKey(idx, col));
}

function renderKeyChips(containerId, columns, selectedKeys, onToggle) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = '';

    (columns || []).forEach(col => {
        const chip = document.createElement('span');
        chip.className = 'column-chip';
        const keyIndex = selectedKeys.indexOf(col.name);
        if (keyIndex >= 0) {
            chip.classList.add('selected');
            chip.innerHTML = `<span class="chip-order">${keyIndex + 1}</span>${col.name}`;
        } else {
            chip.textContent = col.name;
        }
        chip.onclick = () => onToggle(col.name);
        container.appendChild(chip);
    });
}

function toggleSourceKey(idx, colName) {
    const af = joinState.additionalFrames[idx];
    toggleKeyInArray(af.sourceKeys, colName);
    renderAdditionalFrameKeyMapping(idx);
}

function toggleTargetKey(idx, colName) {
    const af = joinState.additionalFrames[idx];
    toggleKeyInArray(af.targetKeys, colName);
    renderAdditionalFrameKeyMapping(idx);
}

function toggleKeyInArray(keyArray, colName) {
    const keyIdx = keyArray.indexOf(colName);
    if (keyIdx >= 0) {
        keyArray.splice(keyIdx, 1);
    } else {
        keyArray.push(colName);
    }
}

function removeAdditionalFrame(idx) {
    joinState.additionalFrames.splice(idx, 1);
    renderAdditionalFrames();
}

function getAllFrameConfigs() {
    const configs = [];
    const joinPairs = [];

    if (joinState.leftFrame && joinState.leftKeys.length > 0) {
        configs.push({ frame: joinState.leftFrame, columns: joinState.leftKeys });
    }
    if (joinState.rightFrame && joinState.rightKeys.length > 0) {
        configs.push({ frame: joinState.rightFrame, columns: joinState.rightKeys });
    }

    // Primary left-right join pair
    if (joinState.leftFrame && joinState.rightFrame &&
        joinState.leftKeys.length > 0 && joinState.rightKeys.length > 0) {
        joinPairs.push({
            source_frame: joinState.leftFrame,
            target_frame: joinState.rightFrame,
            source_keys: joinState.leftKeys,
            target_keys: joinState.rightKeys
        });
    }

    // Additional frames with explicit join pairs
    joinState.additionalFrames.forEach(af => {
        if (af.frame && af.sourceKeys.length > 0) {
            configs.push({ frame: af.frame, columns: af.sourceKeys });
        }
        if (af.frame && af.targetFrame &&
            af.sourceKeys.length > 0 && af.targetKeys.length > 0) {
            joinPairs.push({
                source_frame: af.frame,
                target_frame: af.targetFrame,
                source_keys: af.sourceKeys,
                target_keys: af.targetKeys
            });
        }
    });

    return { configs, joinPairs };
}

async function runHistoryAnalysis() {
    const { configs, joinPairs } = getAllFrameConfigs();

    if (configs.length < 2) {
        alert('Select at least 2 frames with join keys');
        return;
    }

    if (joinPairs.length === 0) {
        alert('Configure at least one join pair with source and target keys');
        return;
    }

    const btn = $('analyze-history');
    btn.disabled = true;
    btn.textContent = 'Analyzing...';

    try {
        const result = await fetchJSON('/api/history/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                frames: configs,
                join_pairs: joinPairs,
                bucket_size: joinState.bucketSize
            })
        });

        joinState.coverageData = result;
        renderCoverageTimeline(result);
        renderTemporalCoverage(result);
        renderPredictions(result);
        renderPairwiseOverlaps(result);

    } catch (e) {
        alert('Analysis failed: ' + e.message);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Analyze Coverage';
    }
}

function renderCoverageTimeline(result) {
    const container = $('coverage-timeline');
    const chart = $('timeline-chart');
    const labels = $('timeline-labels');

    if (!result.timeline || result.timeline.length === 0) {
        container.style.display = 'none';
        return;
    }

    container.style.display = 'block';
    chart.innerHTML = '';
    labels.innerHTML = '';

    const frames = result.frames;
    const timeline = result.timeline;

    // Add dense class for many buckets to reduce bar width
    chart.classList.toggle('dense', timeline.length > 200);
    const buckets = timeline.map(t => t.bucket);

    // Create row for each frame
    frames.forEach(frame => {
        const row = document.createElement('div');
        row.className = 'timeline-row';

        const label = document.createElement('span');
        label.className = 'timeline-label';
        label.textContent = frame;
        label.title = `Data presence for ${frame} over time`;
        row.appendChild(label);

        const bars = document.createElement('div');
        bars.className = 'timeline-bars';

        timeline.forEach(bucket => {
            const bar = document.createElement('div');
            bar.className = 'timeline-bar';
            const count = bucket.frame_counts[frame] || 0;
            bar.classList.add(count > 0 ? 'present' : 'absent');
            bar.title = `${bucket.bucket}: ${count.toLocaleString()} rows`;
            bars.appendChild(bar);
        });

        row.appendChild(bars);
        chart.appendChild(row);
    });

    // Add INNER join coverage row
    const innerRow = document.createElement('div');
    innerRow.className = 'timeline-row timeline-row-inner';

    const innerLabel = document.createElement('span');
    innerLabel.className = 'timeline-label';
    innerLabel.textContent = 'INNER (all)';
    innerLabel.title = 'Shows periods where an INNER join across all frames would retain data';
    innerRow.appendChild(innerLabel);

    const innerBars = document.createElement('div');
    innerBars.className = 'timeline-bars';

    timeline.forEach(bucket => {
        const bar = document.createElement('div');
        bar.className = 'timeline-bar';
        bar.classList.add(bucket.all_present ? 'all-present' : 'partial');
        bar.title = bucket.all_present ? `${bucket.bucket}: All frames present` : `${bucket.bucket}: Partial coverage`;
        innerBars.appendChild(bar);
    });

    innerRow.appendChild(innerBars);
    chart.appendChild(innerRow);

    // Add time labels
    if (buckets.length > 0) {
        const labelRow = document.createElement('div');
        labelRow.className = 'timeline-labels-row';
        labelRow.innerHTML = `
            <span class="timeline-label"></span>
            <div class="timeline-label-bar">
                <span>${buckets[0]}</span>
                <span>${buckets[buckets.length - 1]}</span>
            </div>
        `;
        labels.appendChild(labelRow);
    }
}

function renderPredictions(result) {
    const container = $('join-predictions');
    const tbody = $('predictions-body');

    if (!result.predictions || result.predictions.length === 0) {
        container.style.display = 'none';
        return;
    }

    container.style.display = 'block';
    tbody.innerHTML = '';

    result.predictions.forEach(pred => {
        const tr = document.createElement('tr');

        const nullCols = Object.entries(pred.null_columns || {})
            .map(([frame, count]) => `${frame}: ${count.toLocaleString()}`)
            .join(', ') || 'None';

        tr.innerHTML = `
            <td>${pred.join_type}</td>
            <td>${pred.estimated_rows.toLocaleString()}</td>
            <td>${nullCols}</td>
            <td>${pred.coverage_pct.toFixed(1)}%</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderPairwiseOverlaps(result) {
    const container = $('pairwise-overlaps');
    const grid = $('overlaps-grid');

    if (!result.pairwise_overlaps || result.pairwise_overlaps.length === 0) {
        container.style.display = 'none';
        return;
    }

    container.style.display = 'block';
    grid.innerHTML = '';

    result.pairwise_overlaps.forEach(overlap => {
        const card = document.createElement('div');
        card.className = 'overlap-card';
        card.innerHTML = `
            <div class="overlap-header">${overlap.frame1} ↔ ${overlap.frame2}</div>
            <div class="overlap-stats">
                <div class="overlap-stat" title="Percentage of keys shared between both frames (common keys / larger key set)">
                    <span class="overlap-value">${overlap.overlap_pct.toFixed(1)}%</span>
                    <span class="overlap-label">Overlap</span>
                </div>
                <div class="overlap-stat" title="Count of distinct keys that exist in both frames">
                    <span class="overlap-value">${overlap.both.toLocaleString()}</span>
                    <span class="overlap-label">Common Keys</span>
                </div>
            </div>
            <div class="overlap-details">
                <span title="Keys in ${overlap.frame1} but not ${overlap.frame2} - would be NULL in RIGHT join or dropped in INNER">${overlap.frame1} only: ${overlap.left_only.toLocaleString()}</span>
                <span title="Keys in ${overlap.frame2} but not ${overlap.frame1} - would be NULL in LEFT join or dropped in INNER">${overlap.frame2} only: ${overlap.right_only.toLocaleString()}</span>
            </div>
        `;
        grid.appendChild(card);
    });
}

function renderTemporalCoverage(result) {
    const container = $('temporal-coverage');
    const banner = $('overlap-zone-banner');
    const tbody = $('temporal-ranges-body');
    const dataLossSection = $('data-loss-section');
    const dataLossGrid = $('data-loss-grid');
    const gapsSection = $('internal-gaps-section');
    const gapsList = $('internal-gaps-list');

    if (!result.temporal_ranges || result.temporal_ranges.length === 0) {
        container.style.display = 'none';
        return;
    }

    container.style.display = 'block';
    tbody.innerHTML = '';

    // Render overlap zone banner
    if (result.overlap_zone) {
        const oz = result.overlap_zone;
        if (oz.valid) {
            banner.className = 'overlap-zone-banner overlap-valid';
            banner.innerHTML = `
                <span class="overlap-zone-label">Overlap Zone (Safe for INNER Join):</span>
                <span class="overlap-zone-range">${oz.start} → ${oz.end}</span>
                <span class="overlap-zone-span">(${oz.span})</span>
            `;
        } else {
            banner.className = 'overlap-zone-banner overlap-invalid';
            banner.innerHTML = `
                <span class="overlap-zone-warning">No date overlap between frames - INNER join would return 0 rows</span>
            `;
        }
        banner.style.display = 'flex';
    } else {
        banner.style.display = 'none';
    }

    // Render temporal ranges table
    let hasAnyGaps = false;
    result.temporal_ranges.forEach(range => {
        const tr = document.createElement('tr');
        const gapCount = range.internal_gaps ? range.internal_gaps.length : 0;
        if (gapCount > 0) hasAnyGaps = true;

        tr.innerHTML = `
            <td>${range.frame}</td>
            <td>${range.min_date || '-'}</td>
            <td>${range.max_date || '-'}</td>
            <td>${formatDateSpan(range.min_date, range.max_date)}</td>
            <td>${range.total_rows.toLocaleString()}</td>
            <td class="${range.null_dates > 0 ? 'issue' : ''}">${range.null_dates.toLocaleString()}</td>
            <td class="${gapCount > 0 ? 'issue' : ''}">${gapCount}</td>
        `;
        tbody.appendChild(tr);
    });

    // Render data loss section
    if (result.data_loss && result.data_loss.length > 0) {
        const hasLoss = result.data_loss.some(dl => dl.total_lost > 0);
        if (hasLoss) {
            dataLossSection.style.display = 'block';
            dataLossGrid.innerHTML = '';

            result.data_loss.forEach(loss => {
                if (loss.total_lost === 0) return;

                const card = document.createElement('div');
                card.className = 'data-loss-card';
                card.innerHTML = `
                    <div class="data-loss-frame">${loss.frame}</div>
                    <div class="data-loss-stats">
                        <div class="data-loss-stat">
                            <span class="data-loss-value">${loss.total_lost.toLocaleString()}</span>
                            <span class="data-loss-label">rows lost (${loss.pct_lost.toFixed(1)}%)</span>
                        </div>
                    </div>
                    <div class="data-loss-breakdown">
                        ${loss.rows_before_overlap > 0 ? `<span>Before overlap: ${loss.rows_before_overlap.toLocaleString()}</span>` : ''}
                        ${loss.rows_after_overlap > 0 ? `<span>After overlap: ${loss.rows_after_overlap.toLocaleString()}</span>` : ''}
                    </div>
                `;
                dataLossGrid.appendChild(card);
            });
        } else {
            dataLossSection.style.display = 'none';
        }
    } else {
        dataLossSection.style.display = 'none';
    }

    // Render internal gaps section
    if (hasAnyGaps) {
        gapsSection.style.display = 'block';
        gapsList.innerHTML = '';

        result.temporal_ranges.forEach(range => {
            if (!range.internal_gaps || range.internal_gaps.length === 0) return;

            const gapItem = document.createElement('div');
            gapItem.className = 'gap-item';

            const gapDescriptions = range.internal_gaps.map(gap =>
                `${gap.start} → ${gap.end} (${gap.periods} ${range.granularity}s)`
            ).join(', ');

            gapItem.innerHTML = `
                <span class="gap-frame">${range.frame}:</span>
                <span class="gap-details">${gapDescriptions}</span>
            `;
            gapsList.appendChild(gapItem);
        });
    } else {
        gapsSection.style.display = 'none';
    }
}

function formatDateSpan(minDate, maxDate) {
    if (!minDate || !maxDate) return '-';

    const start = new Date(minDate);
    const end = new Date(maxDate);
    const days = Math.floor((end - start) / (1000 * 60 * 60 * 24));

    if (days < 0) return '-';

    const years = Math.floor(days / 365);
    const months = Math.floor((days % 365) / 30);
    const remainingDays = days % 30;

    const parts = [];
    if (years > 0) parts.push(`${years}y`);
    if (months > 0) parts.push(`${months}m`);
    if (remainingDays > 0 || parts.length === 0) parts.push(`${remainingDays}d`);

    return parts.join(' ');
}

// Data Quality (DQX) Module
const DQX_CHECKS = {
    is_not_null: { label: 'Not Null', params: [] },
    is_not_empty: { label: 'Not Empty', params: [] },
    is_not_null_and_not_empty: { label: 'Not Null & Not Empty', params: [] },
    is_in_range: { label: 'In Range', params: ['min', 'max'] },
    is_not_less_than: { label: 'Min Value', params: ['limit'] },
    is_not_greater_than: { label: 'Max Value', params: ['limit'] },
    regex_match: { label: 'Regex', params: ['regex'] },
    is_valid_date: { label: 'Valid Date', params: [] },
    is_valid_timestamp: { label: 'Valid Timestamp', params: [] },
    is_valid_json: { label: 'Valid JSON', params: [] },
    is_valid_ipv4_address: { label: 'Valid IPv4', params: [] },
    is_valid_ipv6_address: { label: 'Valid IPv6', params: [] }
};

async function initQuality() {
    try {
        const data = await fetchJSON('/api/dqx/available');
        state.dqxAvailable = data.available;
        renderDqxAvailability();
    } catch (e) {
        state.dqxAvailable = false;
        renderDqxAvailability();
    }
    setupQualityEventListeners();
}

function renderDqxAvailability() {
    const container = $('dqx-availability');
    if (state.dqxAvailable) {
        container.className = 'dqx-availability available';
        container.innerHTML = '<span class="dqx-status">DQX Available</span>';
        $('profile-btn').disabled = !state.currentFrame;
        $('run-checks-btn').disabled = !state.currentFrame;
    } else {
        container.className = 'dqx-availability unavailable';
        container.innerHTML = `
            <span class="dqx-status">DQX Not Available</span>
            <span class="dqx-hint">Install with: pip install databricks-labs-dqx</span>
        `;
    }
}

function setupQualityEventListeners() {
    $('profile-btn').onclick = runProfile;
    $('run-checks-btn').onclick = runQualityChecks;
    $('clear-quality-btn').onclick = clearQualityResults;
}

function updateQualityButtons() {
    const hasFrame = !!state.currentFrame;
    const hasRules = Object.keys(state.qualityRules).length > 0;
    const hasResults = !!state.qualityResults;

    $('profile-btn').disabled = !state.dqxAvailable || !hasFrame;
    $('run-checks-btn').disabled = !state.dqxAvailable || !hasFrame || !hasRules;
    $('clear-quality-btn').disabled = !hasResults && !hasRules;
}

async function runProfile() {
    if (!state.currentFrame || !state.dqxAvailable) return;

    const btn = $('profile-btn');
    btn.disabled = true;
    btn.textContent = 'Profiling...';

    try {
        const data = await fetchJSON(`/api/frames/${state.currentFrame}/quality/profile`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });

        state.qualitySuggestions = data;
        renderProfileResults(data);
        renderQualityConfig();

    } catch (e) {
        alert('Profiling failed: ' + e.message);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Profile Data';
        updateQualityButtons();
    }
}

function renderProfileResults(data) {
    const container = $('profile-results');
    const suggestedContainer = $('suggested-rules');
    const codegenContainer = $('codegen-actions');

    console.log('renderProfileResults called', data);
    console.log('codegenContainer:', codegenContainer);

    if (!data.suggested_rules || data.suggested_rules.length === 0) {
        container.style.display = 'none';
        if (codegenContainer) codegenContainer.style.display = 'none';
        return;
    }

    container.style.display = 'block';
    if (codegenContainer) codegenContainer.style.display = 'flex';
    suggestedContainer.innerHTML = '';

    // Wire up code generation buttons
    $('copy-python-btn').onclick = () => copyCodeToClipboard('python');
    $('copy-yaml-btn').onclick = () => copyCodeToClipboard('yaml');

    const byColumn = {};
    data.suggested_rules.forEach(rule => {
        const col = rule.column || 'dataset';
        if (!byColumn[col]) byColumn[col] = [];
        byColumn[col].push(rule);
    });

    Object.entries(byColumn).forEach(([col, rules]) => {
        const div = document.createElement('div');
        div.className = 'suggested-column';
        div.innerHTML = `
            <span class="suggested-col-name">${col}</span>
            <div class="suggested-checks">
                ${rules.map(r => `
                    <button class="apply-rule-btn" data-column="${col}" data-func="${r.check_func}">
                        + ${r.check_func}
                    </button>
                `).join('')}
            </div>
        `;
        suggestedContainer.appendChild(div);

        div.querySelectorAll('.apply-rule-btn').forEach(btn => {
            btn.onclick = () => applySuggestedRule(btn.dataset.column, btn.dataset.func);
        });
    });
}

function applySuggestedRule(column, checkFunc) {
    if (!state.qualityRules[column]) {
        state.qualityRules[column] = {};
    }
    state.qualityRules[column][checkFunc] = { enabled: true, params: {} };
    renderQualityConfig();
    updateQualityButtons();
}

function generatePythonCode(rules) {
    const imports = `from databricks.labs.dqx.rule import DQRowRule
from databricks.labs.dqx import check_funcs
from databricks.labs.dqx.engine import DQEngine
from databricks.sdk import WorkspaceClient`;

    const ruleLines = rules.map(r => {
        const kwargs = r.check_func_kwargs || {};
        const hasKwargs = Object.keys(kwargs).length > 0;
        const kwargsStr = hasKwargs
            ? `,\n        check_func_kwargs=${JSON.stringify(kwargs)}`
            : '';
        return `    DQRowRule(
        name="${r.name}",
        criticality="${r.criticality}",
        check_func=check_funcs.${r.check_func},
        column="${r.column}"${kwargsStr}
    )`;
    }).join(',\n');

    return `${imports}

rules = [
${ruleLines}
]

# Apply checks
ws = WorkspaceClient()
engine = DQEngine(ws)
valid_df, quarantine_df = engine.apply_checks_and_split(input_df, rules)`;
}

function generateYamlCode(rules) {
    const ruleLines = rules.map(r => {
        const kwargs = r.check_func_kwargs || {};
        let yaml = `  - name: ${r.name}
    criticality: ${r.criticality}
    check_func: ${r.check_func}
    column: ${r.column}`;
        Object.entries(kwargs).forEach(([k, v]) => {
            yaml += `\n    ${k}: ${typeof v === 'string' ? v : JSON.stringify(v)}`;
        });
        return yaml;
    }).join('\n');

    return `rules:\n${ruleLines}`;
}

async function copyCodeToClipboard(format) {
    const rules = state.qualitySuggestions?.suggested_rules;
    if (!rules?.length) return;

    const btnId = format === 'python' ? 'copy-python-btn' : 'copy-yaml-btn';
    const btn = $(btnId);
    const code = format === 'python' ? generatePythonCode(rules) : generateYamlCode(rules);

    try {
        await navigator.clipboard.writeText(code);
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(() => {
            btn.textContent = format === 'python' ? 'Copy Python' : 'Copy YAML';
            btn.classList.remove('copied');
        }, 2000);
    } catch (e) {
        alert('Copy failed: ' + e.message);
    }
}

function renderQualityConfig() {
    const container = $('quality-config');
    const columnsDiv = $('quality-columns');

    if (!state.columns || state.columns.length === 0) {
        container.style.display = 'none';
        return;
    }

    container.style.display = 'block';
    columnsDiv.innerHTML = '';

    state.columns.forEach(col => {
        const colRules = state.qualityRules[col.name] || {};
        const hasRules = Object.keys(colRules).some(k => colRules[k]?.enabled);

        const div = document.createElement('div');
        div.className = 'quality-column' + (hasRules ? ' has-rules' : '');
        div.innerHTML = `
            <div class="quality-col-header">
                <span class="quality-col-name">${col.name}</span>
                <span class="quality-col-type">${col.type}</span>
            </div>
            <div class="quality-checks">
                ${Object.entries(DQX_CHECKS).map(([func, info]) => {
                    const ruleConfig = colRules[func] || {};
                    const checked = ruleConfig.enabled ? 'checked' : '';
                    const paramsHtml = info.params.length > 0 ? `
                        <div class="check-params" style="${ruleConfig.enabled ? '' : 'display:none'}">
                            ${info.params.map(p => `
                                <input type="text" class="check-param"
                                       data-col="${col.name}" data-func="${func}" data-param="${p}"
                                       placeholder="${p}" value="${ruleConfig.params?.[p] || ''}">
                            `).join('')}
                        </div>
                    ` : '';
                    return `
                        <label class="check-option">
                            <input type="checkbox" data-col="${col.name}" data-func="${func}" ${checked}>
                            <span>${info.label}</span>
                            ${paramsHtml}
                        </label>
                    `;
                }).join('')}
            </div>
        `;
        columnsDiv.appendChild(div);

        div.querySelectorAll('input[type="checkbox"]').forEach(cb => {
            cb.onchange = () => toggleQualityCheck(cb.dataset.col, cb.dataset.func, cb.checked);
        });
        div.querySelectorAll('.check-param').forEach(input => {
            input.onchange = () => updateCheckParam(
                input.dataset.col, input.dataset.func, input.dataset.param, input.value
            );
        });
    });
}

function toggleQualityCheck(column, checkFunc, enabled) {
    if (!state.qualityRules[column]) {
        state.qualityRules[column] = {};
    }
    if (enabled) {
        state.qualityRules[column][checkFunc] = { enabled: true, params: {} };
    } else {
        delete state.qualityRules[column][checkFunc];
        if (Object.keys(state.qualityRules[column]).length === 0) {
            delete state.qualityRules[column];
        }
    }
    renderQualityConfig();
    updateQualityButtons();
}

function updateCheckParam(column, checkFunc, param, value) {
    if (!state.qualityRules[column]?.[checkFunc]) return;
    if (!state.qualityRules[column][checkFunc].params) {
        state.qualityRules[column][checkFunc].params = {};
    }
    state.qualityRules[column][checkFunc].params[param] = value;
}

async function runQualityChecks() {
    if (!state.currentFrame || !state.dqxAvailable) return;

    const rules = buildRulesPayload();
    if (rules.length === 0) {
        alert('Please configure at least one quality check');
        return;
    }

    const btn = $('run-checks-btn');
    btn.disabled = true;
    btn.textContent = 'Checking...';

    try {
        const data = await fetchJSON(`/api/frames/${state.currentFrame}/quality/check`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rules })
        });

        state.qualityResults = data;
        renderQualitySummary(data);
        renderRowsWithQuality();

    } catch (e) {
        alert('Quality check failed: ' + e.message);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Run Checks';
        updateQualityButtons();
    }
}

function buildRulesPayload() {
    const rules = [];
    Object.entries(state.qualityRules).forEach(([column, checks]) => {
        Object.entries(checks).forEach(([func, config]) => {
            if (!config.enabled) return;
            rules.push({
                name: `${column}_${func}`,
                check_func: func,
                column: column,
                criticality: 'error',
                check_func_kwargs: config.params || {}
            });
        });
    });
    return rules;
}

function renderQualitySummary(data) {
    const container = $('quality-summary');
    const statsDiv = $('summary-stats');

    container.style.display = 'block';

    const totalErrors = Object.values(data.error_summary || {}).reduce((a, b) => a + b, 0);
    const totalWarnings = Object.values(data.warning_summary || {}).reduce((a, b) => a + b, 0);

    statsDiv.innerHTML = `
        <div class="quality-stat ${totalErrors > 0 ? 'has-errors' : 'no-errors'}">
            <span class="quality-stat-value">${totalErrors}</span>
            <span class="quality-stat-label">Errors</span>
        </div>
        <div class="quality-stat ${totalWarnings > 0 ? 'has-warnings' : 'no-warnings'}">
            <span class="quality-stat-value">${totalWarnings}</span>
            <span class="quality-stat-label">Warnings</span>
        </div>
        <div class="quality-stat">
            <span class="quality-stat-value">${data.total_rows || 0}</span>
            <span class="quality-stat-label">Rows Checked</span>
        </div>
        <div class="quality-stat">
            <span class="quality-stat-value">${data.compute_ms || 0}ms</span>
            <span class="quality-stat-label">Time</span>
        </div>
    `;

    if (Object.keys(data.error_summary || {}).length > 0) {
        statsDiv.innerHTML += `
            <div class="error-breakdown">
                <h5>Errors by Column</h5>
                ${Object.entries(data.error_summary).map(([col, count]) =>
                    `<span class="error-col">${col}: ${count}</span>`
                ).join('')}
            </div>
        `;
    }
}

function renderRowsWithQuality() {
    // Extend renderRows to show quality indicators
    const tbody = $('table-body');
    if (!state.qualityResults || !tbody.children.length) return;

    const rowsData = state.qualityResults.rows || [];
    const rowsByIndex = {};
    rowsData.forEach(r => { rowsByIndex[r.row_index] = r; });

    // Add error/warning indicators to existing rows
    Array.from(tbody.children).forEach((tr, idx) => {
        const qr = rowsByIndex[idx];
        if (!qr) return;

        const hasErrors = qr.errors && qr.errors.length > 0;
        const hasWarnings = qr.warnings && qr.warnings.length > 0;

        if (hasErrors) tr.classList.add('row-has-errors');
        if (hasWarnings) tr.classList.add('row-has-warnings');

        // Add cell-level indicators
        const cells = tr.children;
        state.columns.forEach((col, colIdx) => {
            const cellErrors = (qr.errors || []).filter(e =>
                e.columns && e.columns.includes(col.name)
            );
            const cellWarnings = (qr.warnings || []).filter(w =>
                w.columns && w.columns.includes(col.name)
            );

            if (cellErrors.length > 0) {
                cells[colIdx].classList.add('cell-error');
                cells[colIdx].title = cellErrors.map(e => e.message).join('; ');
            }
            if (cellWarnings.length > 0) {
                cells[colIdx].classList.add('cell-warning');
                cells[colIdx].title = cellWarnings.map(w => w.message).join('; ');
            }
        });
    });
}

function clearQualityResults() {
    state.qualityRules = {};
    state.qualityResults = null;
    state.qualitySuggestions = null;

    $('quality-config').style.display = 'none';
    $('quality-summary').style.display = 'none';
    $('profile-results').style.display = 'none';

    // Remove quality indicators from table
    const tbody = $('table-body');
    Array.from(tbody.children).forEach(tr => {
        tr.classList.remove('row-has-errors', 'row-has-warnings');
        Array.from(tr.children).forEach(td => {
            td.classList.remove('cell-error', 'cell-warning');
        });
    });

    updateQualityButtons();
}

// ============================================================
// CSV Reconciliation Module
// ============================================================

const reconcileState = {
    sourceType: 'csv', // 'csv' or 'dataframe'
    csvFrames: [],
    sourceFrame: null,
    targetFrame: null,
    sourceColumns: [],
    targetColumns: [],
    sourceGroupBy: [],
    targetGroupBy: [],
    sourceJoinKeys: [],
    targetJoinKeys: [],
    joinType: 'full',
    aggregations: [],
    results: null
};

function initReconciliation() {
    $('csv-file-input').onchange = handleCsvFileSelect;
    $('upload-csv-btn').onclick = uploadCsv;
    $('run-reconcile').onclick = runReconciliation;

    $('reconcile-source').onchange = handleSourceSelect;
    $('reconcile-target').onchange = handleTargetSelect;
    $('reconcile-source-df').onchange = handleSourceDfSelect;

    $('source-type-csv').onclick = () => setSourceType('csv');
    $('source-type-df').onclick = () => setSourceType('dataframe');

    document.querySelectorAll('.join-type-buttons button').forEach(btn => {
        btn.onclick = () => selectReconcileJoinType(btn.dataset.join);
    });

    document.querySelectorAll('#reconcile-unmatched .viewer-tabs .tab').forEach(btn => {
        btn.onclick = () => showReconcileTab(btn.dataset.side);
    });

    document.getElementById('export-dashboard-btn').onclick = () => exportReconciliation();
}

function setSourceType(type) {
    reconcileState.sourceType = type;
    reconcileState.sourceFrame = null;
    reconcileState.sourceColumns = [];
    reconcileState.sourceGroupBy = [];
    reconcileState.sourceJoinKeys = [];

    $('source-type-csv').classList.toggle('active', type === 'csv');
    $('source-type-df').classList.toggle('active', type === 'dataframe');

    $('csv-upload-section').style.display = type === 'csv' ? 'block' : 'none';
    $('df-source-section').style.display = type === 'dataframe' ? 'block' : 'none';
    $('csv-source-group').style.display = type === 'csv' ? 'block' : 'none';

    if (type === 'dataframe') {
        populateSourceDfSelector();
        populateTargetSelector();
        $('reconcile-config').style.display = 'block';
    } else {
        $('reconcile-config').style.display = reconcileState.csvFrames.length > 0 ? 'block' : 'none';
    }

    renderSourceGroupByChips();
    renderSourceJoinKeyChips();
    renderAggregationColumns();
}

function handleCsvFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;
    const suggestedName = file.name.replace(/\.csv$/i, '');
    $('csv-frame-name').value = suggestedName;
}

async function uploadCsv() {
    const fileInput = $('csv-file-input');
    const file = fileInput.files[0];
    if (!file) {
        $('upload-status').textContent = 'Please select a CSV file';
        return;
    }

    const frameName = $('csv-frame-name').value || file.name.replace(/\.csv$/i, '');
    const formData = new FormData();
    formData.append('file', file);
    formData.append('frame_name', frameName);

    $('upload-status').textContent = 'Uploading...';

    try {
        const res = await fetch('/api/reconcile/upload', {
            method: 'POST',
            body: formData
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.error);
        }

        const data = await res.json();
        $('upload-status').textContent =
            `Uploaded: ${data.row_count.toLocaleString()} rows, ${data.columns.length} columns`;

        reconcileState.csvFrames.push({
            name: data.frame_name,
            columns: data.columns
        });

        populateReconcileSelectors();
        $('reconcile-config').style.display = 'block';
    } catch (e) {
        $('upload-status').textContent = 'Upload failed: ' + e.message;
    }
}

async function populateReconcileSelectors() {
    const sourceSelect = $('reconcile-source');
    sourceSelect.innerHTML = '<option value="">Select CSV...</option>';
    reconcileState.csvFrames.forEach(f => {
        const opt = document.createElement('option');
        opt.value = f.name;
        opt.textContent = f.name;
        sourceSelect.appendChild(opt);
    });

    const targetSelect = $('reconcile-target');
    targetSelect.innerHTML = '<option value="">Select DataFrame...</option>';
    try {
        const data = await fetchJSON('/api/frames');
        data.frames.forEach(name => {
            const opt = document.createElement('option');
            opt.value = name;
            opt.textContent = name;
            targetSelect.appendChild(opt);
        });
    } catch (e) {
        console.error('Failed to load frames:', e);
    }
}

function handleSourceSelect(e) {
    const name = e.target.value;
    reconcileState.sourceFrame = name;
    reconcileState.sourceGroupBy = [];
    reconcileState.sourceJoinKeys = [];

    const frame = reconcileState.csvFrames.find(f => f.name === name);
    if (frame) {
        reconcileState.sourceColumns = frame.columns;
        renderSourceGroupByChips();
        renderSourceJoinKeyChips();
        renderAggregationColumns();
    }
}

async function populateSourceDfSelector() {
    const select = $('reconcile-source-df');
    select.innerHTML = '<option value="">Select DataFrame...</option>';
    try {
        const data = await fetchJSON('/api/frames');
        data.frames.forEach(name => {
            const opt = document.createElement('option');
            opt.value = name;
            opt.textContent = name;
            select.appendChild(opt);
        });
    } catch (e) {
        console.error('Failed to load frames:', e);
    }
}

async function populateTargetSelector() {
    const select = $('reconcile-target');
    select.innerHTML = '<option value="">Select DataFrame...</option>';
    try {
        const data = await fetchJSON('/api/frames');
        data.frames.forEach(name => {
            const opt = document.createElement('option');
            opt.value = name;
            opt.textContent = name;
            select.appendChild(opt);
        });
    } catch (e) {
        console.error('Failed to load frames:', e);
    }
}

async function handleSourceDfSelect(e) {
    const name = e.target.value;
    reconcileState.sourceFrame = name;
    reconcileState.sourceGroupBy = [];
    reconcileState.sourceJoinKeys = [];

    if (name) {
        try {
            const data = await fetchJSON(`/api/frames/${name}/schema`);
            reconcileState.sourceColumns = data.columns || [];
            renderSourceGroupByChips();
            renderSourceJoinKeyChips();
            renderAggregationColumns();
        } catch (err) {
            console.error('Failed to load source schema:', err);
        }
    }
}

async function handleTargetSelect(e) {
    const name = e.target.value;
    reconcileState.targetFrame = name;
    reconcileState.targetGroupBy = [];
    reconcileState.targetJoinKeys = [];

    if (name) {
        try {
            const data = await fetchJSON(`/api/frames/${name}/schema`);
            reconcileState.targetColumns = data.columns || [];
            renderTargetGroupByChips();
            renderTargetJoinKeyChips();
        } catch (err) {
            console.error('Failed to load target schema:', err);
        }
    }
}

function renderSourceGroupByChips() {
    const container = $('source-group-by-chips');
    container.innerHTML = '';
    reconcileState.sourceColumns.forEach(col => {
        const chip = document.createElement('span');
        chip.className = 'column-chip';
        chip.textContent = col.name;
        if (reconcileState.sourceGroupBy.includes(col.name)) {
            chip.classList.add('selected');
        }
        chip.onclick = () => toggleSourceGroupBy(col.name);
        container.appendChild(chip);
    });
}

function renderTargetGroupByChips() {
    const container = $('target-group-by-chips');
    container.innerHTML = '';
    reconcileState.targetColumns.forEach(col => {
        const chip = document.createElement('span');
        chip.className = 'column-chip';
        chip.textContent = col.name;
        if (reconcileState.targetGroupBy.includes(col.name)) {
            chip.classList.add('selected');
        }
        chip.onclick = () => toggleTargetGroupBy(col.name);
        container.appendChild(chip);
    });
}

function toggleSourceGroupBy(name) {
    const idx = reconcileState.sourceGroupBy.indexOf(name);
    if (idx >= 0) {
        reconcileState.sourceGroupBy.splice(idx, 1);
        const keyIdx = reconcileState.sourceJoinKeys.indexOf(name);
        if (keyIdx >= 0) {
            reconcileState.sourceJoinKeys.splice(keyIdx, 1);
        }
    } else {
        reconcileState.sourceGroupBy.push(name);
    }
    renderSourceGroupByChips();
    renderSourceJoinKeyChips();
}

function toggleTargetGroupBy(name) {
    const idx = reconcileState.targetGroupBy.indexOf(name);
    if (idx >= 0) {
        reconcileState.targetGroupBy.splice(idx, 1);
        const keyIdx = reconcileState.targetJoinKeys.indexOf(name);
        if (keyIdx >= 0) {
            reconcileState.targetJoinKeys.splice(keyIdx, 1);
        }
    } else {
        reconcileState.targetGroupBy.push(name);
    }
    renderTargetGroupByChips();
    renderTargetJoinKeyChips();
}

function renderSourceJoinKeyChips() {
    const container = $('source-join-key-chips');
    container.innerHTML = '';
    if (reconcileState.sourceGroupBy.length === 0) {
        container.innerHTML = '<span class="hint">Select group-by columns first</span>';
        return;
    }
    reconcileState.sourceGroupBy.forEach(colName => {
        const chip = document.createElement('span');
        chip.className = 'column-chip';

        const idx = reconcileState.sourceJoinKeys.indexOf(colName);
        if (idx >= 0) {
            chip.classList.add('selected');
            chip.innerHTML = `<span class="chip-order">${idx + 1}</span>${colName}`;
        } else {
            chip.textContent = colName;
        }

        chip.onclick = () => toggleSourceJoinKey(colName);
        container.appendChild(chip);
    });
}

function renderTargetJoinKeyChips() {
    const container = $('target-join-key-chips');
    container.innerHTML = '';
    if (reconcileState.targetGroupBy.length === 0) {
        container.innerHTML = '<span class="hint">Select group-by columns first</span>';
        return;
    }
    reconcileState.targetGroupBy.forEach(colName => {
        const chip = document.createElement('span');
        chip.className = 'column-chip';

        const idx = reconcileState.targetJoinKeys.indexOf(colName);
        if (idx >= 0) {
            chip.classList.add('selected');
            chip.innerHTML = `<span class="chip-order">${idx + 1}</span>${colName}`;
        } else {
            chip.textContent = colName;
        }

        chip.onclick = () => toggleTargetJoinKey(colName);
        container.appendChild(chip);
    });
}

function toggleSourceJoinKey(name) {
    const idx = reconcileState.sourceJoinKeys.indexOf(name);
    if (idx >= 0) {
        reconcileState.sourceJoinKeys.splice(idx, 1);
    } else {
        reconcileState.sourceJoinKeys.push(name);
    }
    renderSourceJoinKeyChips();
}

function toggleTargetJoinKey(name) {
    const idx = reconcileState.targetJoinKeys.indexOf(name);
    if (idx >= 0) {
        reconcileState.targetJoinKeys.splice(idx, 1);
    } else {
        reconcileState.targetJoinKeys.push(name);
    }
    renderTargetJoinKeyChips();
}

function selectReconcileJoinType(type) {
    reconcileState.joinType = type;
    document.querySelectorAll('.join-type-buttons button').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.join === type);
    });
}

function renderAggregationColumns() {
    const container = $('aggregation-columns');
    container.innerHTML = '';

    const numericCols = reconcileState.sourceColumns.filter(c => {
        const dtype = (c.data_type || c.type || '').toLowerCase();
        return dtype.includes('int') || dtype.includes('float') ||
               dtype.includes('decimal') || dtype.includes('double') ||
               dtype.includes('long') || dtype.includes('short');
    });

    if (numericCols.length === 0) {
        container.innerHTML = '<div class="no-numeric">No numeric columns found</div>';
        return;
    }

    numericCols.forEach(col => {
        const row = document.createElement('div');
        row.className = 'agg-row';
        row.innerHTML = `
            <label class="agg-col-label">
                <input type="checkbox" data-col="${col.name}">
                ${col.name}
            </label>
            <div class="agg-options">
                <label><input type="checkbox" data-agg="sum" checked> Sum</label>
                <label><input type="checkbox" data-agg="count"> Count</label>
                <label><input type="checkbox" data-agg="min"> Min</label>
                <label><input type="checkbox" data-agg="max"> Max</label>
                <label><input type="checkbox" data-agg="avg"> Avg</label>
            </div>
        `;
        container.appendChild(row);
    });
}

function collectAggregations() {
    const aggs = [];
    document.querySelectorAll('#aggregation-columns .agg-row').forEach(row => {
        const colCheckbox = row.querySelector('input[data-col]');
        if (!colCheckbox.checked) return;

        const column = colCheckbox.dataset.col;
        const aggregations = [];
        row.querySelectorAll('.agg-options input:checked').forEach(cb => {
            aggregations.push(cb.dataset.agg);
        });

        if (aggregations.length > 0) {
            aggs.push({ column, aggregations });
        }
    });
    return aggs;
}

async function runReconciliation() {
    if (!reconcileState.sourceFrame || !reconcileState.targetFrame) {
        alert('Please select source and target frames');
        return;
    }
    if (reconcileState.sourceGroupBy.length === 0) {
        alert('Please select at least one source group-by column');
        return;
    }
    if (reconcileState.targetGroupBy.length === 0) {
        alert('Please select at least one target group-by column');
        return;
    }
    if (reconcileState.sourceJoinKeys.length === 0) {
        alert('Please select at least one source join key');
        return;
    }
    if (reconcileState.sourceJoinKeys.length !== reconcileState.targetJoinKeys.length) {
        alert('Source and target join key counts must match');
        return;
    }
    const aggregations = collectAggregations();
    if (aggregations.length === 0) {
        alert('Please select at least one aggregation');
        return;
    }

    const btn = $('run-reconcile');
    btn.disabled = true;
    btn.textContent = 'Running...';

    try {
        const result = await fetchJSON('/api/reconcile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                source_frame: reconcileState.sourceFrame,
                target_frame: reconcileState.targetFrame,
                source_type: reconcileState.sourceType,
                source_group_by: reconcileState.sourceGroupBy,
                target_group_by: reconcileState.targetGroupBy,
                source_join_keys: reconcileState.sourceJoinKeys,
                target_join_keys: reconcileState.targetJoinKeys,
                join_type: reconcileState.joinType,
                aggregations: aggregations
            })
        });

        reconcileState.results = result;
        renderReconcileResults(result);
        $('reconcile-results').style.display = 'block';
    } catch (e) {
        alert('Reconciliation failed: ' + e.message);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Run Reconciliation';
    }
}

function renderReconcileResults(result) {
    renderReconcileStats(result.statistics);
    renderColumnTotals(result.column_totals);
    $('source-only-count').textContent = result.source_only.total.toLocaleString();
    $('target-only-count').textContent = result.target_only.total.toLocaleString();
    showReconcileTab('matched');
}

function renderReconcileStats(stats) {
    const container = $('reconcile-stats');
    container.innerHTML = `
        <div class="stat-row stat-row-primary">
            <div class="stat-block stat-match">
                <span class="stat-value">${(stats.match_rate * 100).toFixed(1)}%</span>
                <span class="stat-label">Match Rate</span>
            </div>
            <div class="stat-block">
                <span class="stat-value">${stats.matched_groups.toLocaleString()}</span>
                <span class="stat-label">Matched Groups</span>
            </div>
        </div>
        <div class="stat-row stat-row-details">
            <div class="stat-group">
                <h4>Source${reconcileState.sourceType === 'csv' ? ' (CSV)' : ''}</h4>
                <div class="stat-mini">
                    <span class="mini-label">Total Groups</span>
                    <span class="mini-value">${stats.source_groups.toLocaleString()}</span>
                </div>
                <div class="stat-mini">
                    <span class="mini-label">Unmatched</span>
                    <span class="mini-value issue">${stats.source_only_groups.toLocaleString()}</span>
                </div>
            </div>
            <div class="stat-group">
                <h4>Target</h4>
                <div class="stat-mini">
                    <span class="mini-label">Total Groups</span>
                    <span class="mini-value">${stats.target_groups.toLocaleString()}</span>
                </div>
                <div class="stat-mini">
                    <span class="mini-label">Unmatched</span>
                    <span class="mini-value issue">${stats.target_only_groups.toLocaleString()}</span>
                </div>
            </div>
        </div>
    `;
}

function renderColumnTotals(totals) {
    const container = $('aggregate-comparisons');
    if (!totals || totals.length === 0) {
        container.style.display = 'none';
        return;
    }

    container.style.display = 'block';
    container.innerHTML = `
        <h4>Column Totals</h4>
        <table class="agg-table">
            <thead>
                <tr>
                    <th>Column</th>
                    <th>Aggregation</th>
                    <th>Source Total</th>
                    <th>Target Total</th>
                    <th>Difference</th>
                    <th>% Diff</th>
                </tr>
            </thead>
            <tbody>
                ${totals.map(c => {
                    const hasDiff = c.difference !== null && Math.abs(c.difference) > 0.001;
                    const rowClass = hasDiff ? 'agg-mismatch' : 'agg-match';
                    return `
                    <tr class="${rowClass}">
                        <td>${c.column}</td>
                        <td>${c.aggregation}</td>
                        <td>${formatAggValue(c.source_total)}</td>
                        <td>${formatAggValue(c.target_total)}</td>
                        <td>${formatAggValue(c.difference)}</td>
                        <td>${c.percent_diff !== null ? c.percent_diff.toFixed(2) + '%' : '-'}</td>
                    </tr>`;
                }).join('')}
            </tbody>
        </table>
    `;
}

function formatAggValue(val) {
    if (val === null || val === undefined) return '-';
    if (Number.isInteger(val)) return val.toLocaleString();
    return val.toLocaleString(undefined, { maximumFractionDigits: 2 });
}

function showReconcileTab(side) {
    document.querySelectorAll('#reconcile-unmatched .tab').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.side === side);
    });

    const result = reconcileState.results;
    if (!result) return;

    let rows = [];
    if (side === 'source') rows = result.source_only.rows;
    else if (side === 'target') rows = result.target_only.rows;
    else if (side === 'matched') rows = result.matched_rows.rows;

    renderReconcileTable(rows);
}

function renderReconcileTable(rows) {
    const thead = $('reconcile-head');
    const tbody = $('reconcile-body');

    if (!rows || rows.length === 0) {
        thead.innerHTML = '';
        tbody.innerHTML = '<tr><td>No data</td></tr>';
        return;
    }

    const cols = Object.keys(rows[0]);
    thead.innerHTML = '<tr>' + cols.map(c => `<th>${c}</th>`).join('') + '</tr>';
    tbody.innerHTML = rows.map(row =>
        '<tr>' + cols.map(c => `<td>${row[c] ?? ''}</td>`).join('') + '</tr>'
    ).join('');
}

async function exportReconciliation() {
    if (!reconcileState.results) {
        alert('Run reconciliation first');
        return;
    }

    try {
        const res = await fetch('/api/reconcile/export', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                source_frame: reconcileState.sourceFrame,
                target_frame: reconcileState.targetFrame,
                source_type: reconcileState.sourceType,
                source_group_by: reconcileState.sourceGroupBy,
                target_group_by: reconcileState.targetGroupBy,
                source_join_keys: reconcileState.sourceJoinKeys,
                target_join_keys: reconcileState.targetJoinKeys,
                join_type: reconcileState.joinType,
                aggregations: collectAggregations()
            })
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.error);
        }

        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `reconciliation_${reconcileState.sourceFrame}_${reconcileState.targetFrame}.html`;
        a.click();
        URL.revokeObjectURL(url);
    } catch (e) {
        alert('Export failed: ' + e.message);
    }
}

document.addEventListener('DOMContentLoaded', init);
