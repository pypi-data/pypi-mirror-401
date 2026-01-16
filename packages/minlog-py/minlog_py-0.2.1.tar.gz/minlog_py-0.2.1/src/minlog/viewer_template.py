DEFAULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MinLog Panorama Report</title>
    <style>
        :root {
            --bg-color: #ffffff;
            --sidebar-bg: #f8f9fa;
            --text-color: #1a1a1a;
            --border-color: #e0e0e0;
            --primary-color: #1e88e5;
            --success-color: #4caf50;
            --error-color: #f44336;
            --warning-color: #ff9800;
            --skipped-color: #9e9e9e;
            --hover-bg: #f0f2f5;
            --selected-bg: #e3f2fd;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --bg-color: #1e1e1e;
                --sidebar-bg: #252526;
                --text-color: #d4d4d4;
                --border-color: #3e3e42;
                --hover-bg: #2a2d2e;
                --selected-bg: #37373d;
            }
        }

        * { box-sizing: border-box; }
        body, html {
            margin: 0; padding: 0; height: 100%;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-size: 14px; color: var(--text-color); background: var(--bg-color);
        }

        .container { display: grid; grid-template-columns: 350px 1fr; height: 100vh; overflow: hidden; }

        /* Sidebar */
        .sidebar {
            background: var(--sidebar-bg); border-right: 1px solid var(--border-color);
            display: flex; flex-direction: column; overflow: hidden;
        }
        .sidebar-header {
            padding: 16px; border-bottom: 1px solid var(--border-color);
            display: flex; flex-direction: column; gap: 8px;
        }
        .report-title { font-size: 18px; font-weight: bold; margin: 0; }
        .stats { display: flex; gap: 12px; font-size: 12px; }
        .filter-bar { padding: 8px 16px; border-bottom: 1px solid var(--border-color); }
        .search-input {
            width: 100%; padding: 6px 12px; border: 1px solid var(--border-color);
            border-radius: 4px; background: var(--bg-color); color: var(--text-color);
        }

        .suite-list { flex: 1; overflow-y: auto; padding: 8px 0; }
        .suite-item {
            padding: 10px 16px; cursor: pointer; border-left: 4px solid transparent;
            display: flex; flex-direction: column; gap: 4px;
        }
        .suite-item:hover { background: var(--hover-bg); }
        .suite-item.active { background: var(--selected-bg); border-left-color: var(--primary-color); }
        .suite-item.passed { border-left-color: var(--success-color); }
        .suite-item.failed { border-left-color: var(--error-color); }
        
        .suite-meta { display: flex; justify-content: space-between; font-size: 12px; color: #888; }
        .status-tag {
            padding: 2px 6px; border-radius: 10px; font-size: 10px; font-weight: bold; text-transform: uppercase;
        }
        .status-passed { background: rgba(76, 175, 80, 0.1); color: var(--success-color); }
        .status-failed { background: rgba(244, 67, 54, 0.1); color: var(--error-color); }

        /* Main Content */
        .main { display: flex; flex-direction: column; overflow: hidden; }
        .main-header { padding: 16px 24px; border-bottom: 1px solid var(--border-color); }
        .timeline-container {
            height: 60px; padding: 10px 24px; border-bottom: 1px solid var(--border-color);
            display: flex; align-items: center;
        }
        .timeline { flex: 1; height: 12px; background: var(--border-color); border-radius: 6px; position: relative; }
        .timeline-chunk { position: absolute; height: 100%; border-radius: 6px; opacity: 0.8; cursor: pointer; }

        .details-view { flex: 1; overflow-y: auto; padding: 24px; }
        .step-node { margin-bottom: 12px; border: 1px solid var(--border-color); border-radius: 6px; overflow: hidden; }
        .step-header {
            padding: 12px 16px; background: var(--sidebar-bg); cursor: pointer;
            display: flex; align-items: center; gap: 12px;
        }
        .step-header:hover { background: var(--hover-bg); }
        .step-title { flex: 1; font-weight: 500; }
        .step-duration { font-size: 12px; color: #888; }
        
        .step-content { padding: 16px; border-top: 1px solid var(--border-color); display: none; }
        .step-node.open .step-content { display: block; }
        
        .attachments { margin-top: 12px; display: flex; flex-direction: column; gap: 8px; }
        .attachment-item { border: 1px solid var(--border-color); border-radius: 4px; overflow: hidden; }
        .attachment-header { padding: 8px 12px; background: var(--hover-bg); font-size: 12px; font-weight: bold; }
        .attachment-body {
            padding: 8px 12px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 12px; white-space: pre-wrap; overflow-x: auto; background: #00000010;
        }
        .error-message {
            margin-top: 12px; padding: 12px; background: rgba(244, 67, 54, 0.05);
            border-left: 4px solid var(--error-color); color: var(--error-color); font-family: monospace;
        }

        /* Icons */
        .icon { width: 16px; height: 16px; flex-shrink: 0; }
        .empty-state {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            height: 100%; color: #888; gap: 16px;
        }
    </style>
</head>
<body>
    <div id="root">
        <div class="container">
            <aside class="sidebar">
                <div class="sidebar-header">
                    <h1 class="report-title" id="reportTitle">Loading...</h1>
                    <div class="stats" id="statsArea"></div>
                </div>
                <div class="filter-bar">
                    <input type="text" class="search-input" id="searchInput" placeholder="Search suites...">
                </div>
                <div class="suite-list" id="suiteList"></div>
            </aside>
            <main class="main">
                <div class="timeline-container" id="timelineContainer">
                    <div class="timeline" id="timeline"></div>
                </div>
                <div id="mainContent" style="flex: 1; display: flex; flex-direction: column; overflow: hidden;">
                    <div class="empty-state">
                        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                             style="width: 48px; height: 48px;">
                            <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path>
                            <polyline points="13 2 13 9 20 9"></polyline>
                        </svg>
                        <span>Select a suite to view details</span>
                    </div>
                </div>
            </main>
        </div>
    </div>

    <script id="log-data">
        window.LOG_PAYLOAD = null;
    </script>

    <script>
        const state = {
            data: window.LOG_PAYLOAD,
            selectedSuiteIndex: -1,
            filters: {
                search: '',
                status: 'all'
            }
        };

        function init() {
            if (!state.data) return;
            renderSidebar();
            renderTimeline();
            
            document.getElementById('reportTitle').innerText = state.data.meta.title;
            document.getElementById('searchInput').addEventListener('input', (e) => {
                state.filters.search = e.target.value;
                renderSidebar();
            });
        }

        function renderSidebar() {
            const list = document.getElementById('suiteList');
            list.innerHTML = '';
            
            const stats = { passed: 0, failed: 0, total: 0 };
            
            state.data.suites.forEach((suite, index) => {
                if (suite.status === 'passed') stats.passed++;
                else stats.failed++;
                stats.total++;

                if (state.filters.search &&
                    !suite.title.toLowerCase().includes(state.filters.search.toLowerCase())) return;

                const item = document.createElement('div');
                item.className = `suite-item ${suite.status} ${state.selectedSuiteIndex === index ? 'active' : ''}`;
                item.onclick = () => selectSuite(index);
                
                item.innerHTML = `
                    <div style="font-weight: 500">${suite.title}</div>
                    <div class="suite-meta">
                        <span class="status-tag status-${suite.status}">${suite.status}</span>
                        <span>${suite.duration.toFixed(0)}ms</span>
                    </div>
                `;
                list.appendChild(item);
            });

            document.getElementById('statsArea').innerHTML = `
                <span style="color: var(--success-color)">${stats.passed} Passed</span>
                <span style="color: var(--error-color)">${stats.failed} Failed</span>
                <span>${stats.total} Total</span>
            `;
        }

        function renderTimeline() {
            const timeline = document.getElementById('timeline');
            timeline.innerHTML = '';
            
            // Simplified timeline: map suites to relative horizontal position
            const suites = state.data.suites;
            if (suites.length === 0) return;

            const minStart = Math.min(...suites.map(s => s.startTime));
            const maxEnd = Math.max(...suites.map(s => s.startTime + s.duration / 1000));
            const totalDuration = maxEnd - minStart;

            suites.forEach((suite, index) => {
                const startPct = ((suite.startTime - minStart) / totalDuration) * 100;
                const widthPct = (suite.duration / 1000 / totalDuration) * 100;
                
                const chunk = document.createElement('div');
                chunk.className = 'timeline-chunk';
                chunk.style.left = `${startPct}%`;
                chunk.style.width = `${Math.max(widthPct, 1)}%`;
                chunk.style.background = suite.status === 'passed' ? 'var(--success-color)' : 'var(--error-color)';
                chunk.title = `${suite.title} (${suite.duration.toFixed(0)}ms)`;
                chunk.onclick = () => selectSuite(index);
                timeline.appendChild(chunk);
            });
        }

        function selectSuite(index) {
            state.selectedSuiteIndex = index;
            renderSidebar();
            renderDetails();
        }

        function renderDetails() {
            const container = document.getElementById('mainContent');
            const suite = state.data.suites[state.selectedSuiteIndex];
            
            container.innerHTML = `
                <div class="main-header">
                    <h2 style="margin: 0 0 8px 0">${suite.title}</h2>
                    <div style="color: #888; font-size: 12px;">
                        Started at: ${new Date(suite.startTime * 1000).toLocaleString()} •
                        Duration: ${suite.duration.toFixed(2)}ms
                    </div>
                </div>
                <div class="details-view" id="detailsView"></div>
            `;

            const detailsView = document.getElementById('detailsView');
            suite.steps.forEach(step => {
                renderStep(step, detailsView);
            });
        }

        function renderStep(step, parentElement) {
            const node = document.createElement('div');
            node.className = `step-node ${step.status === 'failed' ? 'open' : ''}`;
            
            node.innerHTML = `
                <div class="step-header">
                    <span class="icon">${step.status === 'passed' ? '✅' : '❌'}</span>
                    <span class="step-title">${step.title}</span>
                    <span class="step-duration">${step.duration.toFixed(1)}ms</span>
                </div>
                <div class="step-content">
                    ${step.error ? `<div class="error-message">${step.error}</div>` : ''}
                    <div class="attachments"></div>
                    <div class="sub-steps"></div>
                </div>
            `;

            node.querySelector('.step-header').onclick = () => {
                node.classList.toggle('open');
            };

            const attachmentList = node.querySelector('.attachments');
            step.attachments.forEach(att => {
                const attNode = document.createElement('div');
                attNode.className = 'attachment-item';
                attNode.innerHTML = `
                    <div class="attachment-header">${att.name} (${att.contentType})</div>
                    <div class="attachment-body">${att.body}</div>
                `;
                attachmentList.appendChild(attNode);
            });

            const subStepsList = node.querySelector('.sub-steps');
            step.steps.forEach(sub => renderStep(sub, subStepsList));

            parentElement.appendChild(node);
        }

        init();
    </script>
</body>
</html>
"""
