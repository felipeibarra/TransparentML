// TransparentML Central Dashboard
// ================================

const API_BASE = '';
let currentAnalysisId = null;
let mainChart = null;
let logTimelineChart = null;
let logsPaused = false;
let logsData = [];
let logStats = { total: 0, info: 0, warning: 0, error: 0 };

// DOM Elements
const modelSelect = document.getElementById('modelSelect');
const urlInput = document.getElementById('urlInput');
const analysisType = document.getElementById('analysisType');
const analyzeUrlBtn = document.getElementById('analyzeUrlBtn');
const logsContainer = document.getElementById('logsContainer');
const progressFill = document.getElementById('progressFill');
const progressPercent = document.getElementById('progressPercent');
const resultsContainer = document.getElementById('resultsContainer');
const recommendationsContainer = document.getElementById('recommendationsContainer');

// Model configs
const urlDiagConfig = document.getElementById('urlDiagConfig');
const linearRegConfig = document.getElementById('linearRegConfig');
const pcaConfig = document.getElementById('pcaConfig');

// Initialize
document.addEventListener('DOMContentLoaded', init);

function init() {
    console.log('TransparentML Dashboard Initialized');
    
    // Model selector
    modelSelect.addEventListener('change', handleModelChange);
    
    // URL Diagnostics
    analyzeUrlBtn.addEventListener('click', handleAnalyzeUrl);
    
    // Linear Regression
    document.getElementById('trainLrBtn')?.addEventListener('click', handleTrainLinearRegression);
    document.getElementById('predictLrBtn')?.addEventListener('click', handlePredictLinearRegression);
    
    // PCA
    document.getElementById('runPcaBtn')?.addEventListener('click', handleRunPCA);
    
    // Log controls
    document.getElementById('clearLogsBtn').addEventListener('click', clearLogs);
    document.getElementById('pauseLogsBtn').addEventListener('click', togglePauseLogs);
    document.getElementById('exportLogsBtn').addEventListener('click', exportLogs);
    
    // Clear all
    document.getElementById('clearBtn').addEventListener('click', clearAll);
    
    // Graph controls
    document.querySelectorAll('.graph-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.graph-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            const chartType = e.target.dataset.chart;
            updateMainChart(chartType);
        });
    });
    
    // Initialize charts
    initCharts();
}

// Model Change Handler
function handleModelChange(e) {
    const model = e.target.value;
    
    // Hide all configs
    urlDiagConfig.classList.add('hidden');
    linearRegConfig.classList.add('hidden');
    pcaConfig.classList.add('hidden');
    
    // Show selected config
    switch(model) {
        case 'url-diagnostics':
            urlDiagConfig.classList.remove('hidden');
            document.getElementById('currentModel').textContent = 'URL Diagnostics';
            break;
        case 'linear-regression':
            linearRegConfig.classList.remove('hidden');
            document.getElementById('currentModel').textContent = 'Linear Regression';
            break;
        case 'pca':
            pcaConfig.classList.remove('hidden');
            document.getElementById('currentModel').textContent = 'PCA Analysis';
            break;
        case 'all':
            urlDiagConfig.classList.remove('hidden');
            linearRegConfig.classList.remove('hidden');
            pcaConfig.classList.remove('hidden');
            document.getElementById('currentModel').textContent = 'All Models';
            break;
    }
    
    addLog(`Switched to ${document.getElementById('currentModel').textContent} model`, 'info');
}

// URL Diagnostics Handler
async function handleAnalyzeUrl() {
    const url = urlInput.value.trim();
    const type = analysisType.value;
    
    if (!url) {
        addLog('❌ Please enter a URL', 'error');
        return;
    }
    
    addLog(`🚀 Starting ${type} analysis for: ${url}`, 'info');
    updateStatus('running');
    updateProgress(10);
    
    try {
        const response = await fetch(`${API_BASE}/api/v1/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, analysis_type: type })
        });
        
        const data = await response.json();
        currentAnalysisId = data.analysis_id;
        
        addLog(`📝 Analysis ID: ${currentAnalysisId}`, 'info');
        
        // Start polling and streaming
        pollAnalysisStatus();
        streamLogs();
        
    } catch (error) {
        addLog(`❌ Error: ${error.message}`, 'error');
        updateStatus('error');
    }
}

// Poll Analysis Status
async function pollAnalysisStatus() {
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE}/api/v1/status/${currentAnalysisId}`);
            const status = await response.json();
            
            updateProgress(status.progress || 0);
            
            if (status.status === 'completed') {
                clearInterval(interval);
                await loadResults();
                updateStatus('complete');
                updateLastRun();
            } else if (status.status === 'failed') {
                clearInterval(interval);
                addLog(`❌ Analysis failed: ${status.error}`, 'error');
                updateStatus('error');
            }
        } catch (error) {
            console.error('Status poll error:', error);
        }
    }, 1000);
}

// Stream Logs
function streamLogs() {
    const eventSource = new EventSource(`${API_BASE}/api/v1/logs/${currentAnalysisId}`);
    
    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.log && !logsPaused) {
            addLog(data.log, 'info');
        }
        
        if (data.done) {
            eventSource.close();
        }
    };
    
    eventSource.onerror = (error) => {
        console.error('SSE Error:', error);
        eventSource.close();
    };
}

// Load Results
async function loadResults() {
    try {
        const response = await fetch(`${API_BASE}/api/v1/results/${currentAnalysisId}`);
        const results = await response.json();
        
        addLog('✅ Results loaded successfully!', 'info');
        displayResults(results);
        
    } catch (error) {
        addLog(`❌ Error loading results: ${error.message}`, 'error');
    }
}

// Display Results
function displayResults(data) {
    // Update statistics
    document.getElementById('statScore').textContent = Math.round(data.health_score) || '--';
    document.getElementById('statAccuracy').textContent = data.grade || '--';
    document.getElementById('statDataPoints').textContent = '30+';
    
    // Results panel
    resultsContainer.innerHTML = `
        <div class="result-score">
            <div class="score-circle">
                <span class="score-big">${Math.round(data.health_score)}</span>
                <span class="score-label">/100</span>
            </div>
            <div class="grade-badge">${data.grade}</div>
        </div>
        <div class="result-metrics">
            <div class="metric-item">
                <span class="metric-label">⚡ Load Time</span>
                <span class="metric-value">${data.metrics?.load_time?.toFixed(2)}s</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">📦 Size</span>
                <span class="metric-value">${data.metrics?.response_size_kb?.toFixed(0)}KB</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">🔒 SSL</span>
                <span class="metric-value">${data.metrics?.ssl_enabled ? '✅' : '❌'}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">📱 Mobile</span>
                <span class="metric-value">${data.metrics?.mobile_friendly ? '✅' : '❌'}</span>
            </div>
        </div>
    `;
    
    // Recommendations
    displayRecommendations(data.recommendations || []);
    
    // Update main chart
    if (data.feature_analysis) {
        updateChartWithData(data.feature_analysis);
    }
}

// Display Recommendations
function displayRecommendations(recommendations) {
    if (recommendations.length === 0) {
        recommendationsContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">✅</div>
                <p>No issues found!</p>
                <p class="empty-hint">Your site is in great shape</p>
            </div>
        `;
        return;
    }
    
    recommendationsContainer.innerHTML = recommendations.map(rec => `
        <div class="rec-item priority-${rec.priority}">
            <div class="rec-header">
                <span class="rec-category">${rec.category}</span>
                <span class="rec-priority">${rec.priority}</span>
            </div>
            <div class="rec-issue">${rec.issue}</div>
            <div class="rec-action">💡 ${rec.action}</div>
        </div>
    `).join('');
}

// Linear Regression Handlers
async function handleTrainLinearRegression() {
    addLog('🎯 Training Linear Regression model...', 'info');
    updateStatus('running');
    
    // Simulate training
    for (let i = 0; i <= 100; i += 20) {
        await sleep(500);
        updateProgress(i);
        addLog(`Training progress: ${i}%`, 'info');
    }
    
    addLog('✅ Model trained successfully!', 'info');
    updateStatus('complete');
    updateLastRun();
}

async function handlePredictLinearRegression() {
    addLog('🔮 Making predictions...', 'info');
    updateStatus('running');
    
    // Simulate prediction
    await sleep(1000);
    
    const prediction = Math.random() * 100;
    document.getElementById('statScore').textContent = prediction.toFixed(2);
    
    addLog(`✅ Prediction: ${prediction.toFixed(2)}`, 'info');
    updateStatus('complete');
}

// PCA Handlers
async function handleRunPCA() {
    const dataset = document.getElementById('pcaDataset').value;
    const components = document.getElementById('pcaComponents').value;
    
    addLog(`🌟 Running PCA on ${dataset} dataset (${components}D)...`, 'info');
    updateStatus('running');
    
    // Simulate PCA
    for (let i = 0; i <= 100; i += 25) {
        await sleep(400);
        updateProgress(i);
    }
    
    addLog('✅ PCA analysis complete!', 'info');
    updateStatus('complete');
    updateLastRun();
    
    // Generate fake PCA visualization
    updateMainChart('scatter');
}

// Charts
function initCharts() {
    const ctx = document.getElementById('mainChart').getContext('2d');
    mainChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Performance', 'Security', 'SEO', 'Mobile', 'Accessibility'],
            datasets: [{
                label: 'Score',
                data: [0, 0, 0, 0, 0],
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(139, 92, 246, 0.8)',
                    'rgba(236, 72, 153, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, max: 100 }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
    
    // Log timeline chart
    const timelineCtx = document.getElementById('logTimelineChart').getContext('2d');
    logTimelineChart = new Chart(timelineCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Events',
                data: [],
                borderColor: 'rgba(59, 130, 246, 1)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function updateMainChart(type) {
    if (!mainChart) return;
    
    mainChart.config.type = type;
    
    if (type === 'scatter') {
        // Generate random scatter data for PCA demo
        const data = Array.from({length: 50}, () => ({
            x: Math.random() * 100,
            y: Math.random() * 100
        }));
        
        mainChart.data.datasets[0] = {
            label: 'Data Points',
            data: data,
            backgroundColor: 'rgba(59, 130, 246, 0.6)'
        };
    }
    
    mainChart.update();
}

function updateChartWithData(featureAnalysis) {
    if (!mainChart) return;
    
    const perfScore = featureAnalysis.performance?.load_time?.status === 'good' ? 100 : 50;
    const secScore = featureAnalysis.security?.ssl?.enabled ? 100 : 0;
    const seoScore = featureAnalysis.seo?.mobile_friendly ? 100 : 50;
    
    mainChart.data.datasets[0].data = [perfScore, secScore, seoScore, 75, 80];
    mainChart.update();
}

// Log Management
function addLog(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = {
        time: timestamp,
        message: message,
        type: type
    };
    
    logsData.push(logEntry);
    
    // Update stats
    logStats.total++;
    if (type === 'info') logStats.info++;
    if (type === 'warning') logStats.warning++;
    if (type === 'error') logStats.error++;
    
    updateLogStats();
    
    if (!logsPaused) {
        const div = document.createElement('div');
        div.className = `log-entry ${type}`;
        div.textContent = `[${timestamp}] ${message}`;
        logsContainer.appendChild(div);
        logsContainer.scrollTop = logsContainer.scrollHeight;
    }
    
    document.getElementById('logsCount').textContent = `${logsData.length} logs`;
}

function updateLogStats() {
    document.getElementById('logStatTotal').textContent = logStats.total;
    document.getElementById('logStatInfo').textContent = logStats.info;
    document.getElementById('logStatWarning').textContent = logStats.warning;
    document.getElementById('logStatError').textContent = logStats.error;
    
    const errorRate = logStats.total > 0 ? (logStats.error / logStats.total * 100).toFixed(1) : 0;
    document.getElementById('logStatErrorRate').textContent = `${errorRate}%`;
    
    // Update timeline
    if (logTimelineChart) {
        const now = new Date().toLocaleTimeString();
        logTimelineChart.data.labels.push(now);
        logTimelineChart.data.datasets[0].data.push(logStats.total);
        
        if (logTimelineChart.data.labels.length > 10) {
            logTimelineChart.data.labels.shift();
            logTimelineChart.data.datasets[0].data.shift();
        }
        
        logTimelineChart.update();
    }
}

function clearLogs() {
    logsContainer.innerHTML = '';
    logsData = [];
    logStats = { total: 0, info: 0, warning: 0, error: 0 };
    updateLogStats();
    document.getElementById('logsCount').textContent = '0 logs';
}

function togglePauseLogs() {
    logsPaused = !logsPaused;
    const btn = document.getElementById('pauseLogsBtn');
    btn.textContent = logsPaused ? '▶️' : '⏸️';
    btn.title = logsPaused ? 'Resume logs' : 'Pause logs';
}

function exportLogs() {
    const content = logsData.map(log => `[${log.time}] [${log.type.toUpperCase()}] ${log.message}`).join('\n');
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `logs_${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    addLog('📥 Logs exported successfully', 'info');
}

// UI Updates
function updateProgress(percent) {
    progressFill.style.width = `${percent}%`;
    progressPercent.textContent = `${percent}%`;
}

function updateStatus(status) {
    const statusEl = document.getElementById('modelStatus');
    statusEl.className = `status-value status-${status}`;
    
    const statusText = {
        'idle': 'Idle',
        'running': 'Running...',
        'complete': 'Completed',
        'error': 'Error'
    };
    
    statusEl.textContent = statusText[status] || status;
}

function updateLastRun() {
    const now = new Date().toLocaleTimeString();
    document.getElementById('lastRun').textContent = now;
}

function clearAll() {
    clearLogs();
    resultsContainer.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">📊</div>
            <p>No results yet</p>
            <p class="empty-hint">Run an analysis to see results here</p>
        </div>
    `;
    recommendationsContainer.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">💡</div>
            <p>No recommendations</p>
            <p class="empty-hint">Complete an analysis first</p>
        </div>
    `;
    document.getElementById('statScore').textContent = '--';
    document.getElementById('statTime').textContent = '--';
    document.getElementById('statDataPoints').textContent = '--';
    document.getElementById('statAccuracy').textContent = '--';
    updateProgress(0);
    updateStatus('idle');
}

// Utilities
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Add some CSS for results display
const style = document.createElement('style');
style.textContent = `
    .result-score {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1rem;
    }
    .score-circle {
        display: inline-block;
        margin-bottom: 1rem;
    }
    .score-big {
        font-size: 3rem;
        font-weight: 800;
        color: var(--primary);
    }
    .score-label {
        font-size: 1.2rem;
        color: var(--text-muted);
    }
    .grade-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: linear-gradient(135deg, var(--primary), #8b5cf6);
        border-radius: 20px;
        font-size: 2rem;
        font-weight: 800;
        color: white;
    }
    .result-metrics {
        display: grid;
        gap: 0.75rem;
    }
    .metric-item {
        display: flex;
        justify-content: space-between;
        padding: 0.75rem;
        background: var(--bg-primary);
        border-radius: 8px;
    }
    .metric-label {
        color: var(--text-secondary);
    }
    .metric-value {
        font-weight: 700;
        color: var(--primary);
    }
    .rec-item {
        padding: 1rem;
        margin-bottom: 0.75rem;
        background: var(--bg-primary);
        border-radius: 8px;
        border-left: 4px solid var(--primary);
    }
    .rec-item.priority-critical { border-left-color: var(--danger); }
    .rec-item.priority-high { border-left-color: var(--warning); }
    .rec-item.priority-medium { border-left-color: var(--primary); }
    .rec-item.priority-low { border-left-color: var(--success); }
    .rec-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    .rec-category {
        font-weight: 600;
        color: var(--text-primary);
    }
    .rec-priority {
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        background: var(--bg-tertiary);
        color: var(--text-secondary);
    }
    .rec-issue {
        margin-bottom: 0.5rem;
        color: var(--text-secondary);
    }
    .rec-action {
        color: var(--primary);
        font-style: italic;
        font-size: 0.9rem;
    }
`;
document.head.appendChild(style);

console.log('Dashboard ready! 🚀');
