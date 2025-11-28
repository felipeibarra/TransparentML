// TransparentML URL Diagnostics - Frontend Application
// =====================================================

const API_BASE = '';  // Same origin
let currentAnalysisId = null;
let featureChart = null;
let categoryChart = null;

// DOM Elements
const form = document.getElementById('analyzeForm');
const urlInput = document.getElementById('urlInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const progressSection = document.getElementById('progressSection');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const logsSection = document.getElementById('logsSection');
const logsContainer = document.getElementById('logsContainer');
const resultsSection = document.getElementById('resultsSection');

// Event Listeners
form.addEventListener('submit', handleAnalyze);

// Main Analysis Function
async function handleAnalyze(e) {
    e.preventDefault();
    
    const url = urlInput.value.trim();
    const analysisType = document.querySelector('input[name="analysisType"]:checked').value;
    
    if (!url) return;
    
    // Reset UI
    resetUI();
    showSection(progressSection);
    showSection(logsSection);
    
    // Disable button
    analyzeBtn.disabled = true;
    document.querySelector('.btn-text').textContent = 'Analyzing...';
    
    try {
        // Start analysis
        const response = await fetch(`${API_BASE}/api/v1/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, analysis_type: analysisType })
        });
        
        const data = await response.json();
        currentAnalysisId = data.analysis_id;
        
        addLog(`🚀 Analysis started for: ${url}`);
        addLog(`📝 Analysis ID: ${currentAnalysisId}`);
        
        // Start polling for status
        pollAnalysisStatus();
        
        // Start streaming logs
        streamLogs();
        
    } catch (error) {
        console.error('Error:', error);
        addLog(`❌ Error: ${error.message}`, 'error');
        resetButton();
    }
}

// Poll Analysis Status
async function pollAnalysisStatus() {
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE}/api/v1/status/${currentAnalysisId}`);
            const status = await response.json();
            
            // Update progress
            updateProgress(status.progress || 0);
            
            // Check if completed
            if (status.status === 'completed') {
                clearInterval(interval);
                await loadResults();
                resetButton();
            } else if (status.status === 'failed') {
                clearInterval(interval);
                addLog(`❌ Analysis failed: ${status.error}`, 'error');
                resetButton();
            }
        } catch (error) {
            console.error('Status poll error:', error);
        }
    }, 1000);
}

// Stream Logs via Server-Sent Events
function streamLogs() {
    const eventSource = new EventSource(`${API_BASE}/api/v1/logs/${currentAnalysisId}`);
    
    eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.log) {
            addLog(data.log);
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
        
        addLog('✅ Results loaded successfully!');
        
        // Display results
        displayResults(results);
        
    } catch (error) {
        console.error('Error loading results:', error);
        addLog(`❌ Error loading results: ${error.message}`, 'error');
    }
}

// Display Results
function displayResults(data) {
    showSection(resultsSection);
    
    // Health Score
    displayHealthScore(data.health_score, data.grade);
    
    // Metrics
    displayMetrics(data.metrics);
    
    // Charts
    displayCharts(data.feature_analysis);
    
    // Anomalies
    displayAnomalies(data.anomalies);
    
    // Recommendations
    displayRecommendations(data.recommendations);
    
    // Raw Data
    document.getElementById('rawData').textContent = JSON.stringify(data, null, 2);
    
    // Show new analysis button
    showNewAnalysisButton();
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Display Health Score
function displayHealthScore(score, grade) {
    const scoreValue = document.getElementById('scoreValue');
    const gradeDisplay = document.getElementById('gradeDisplay');
    const scoreCircle = document.getElementById('scoreCircle');
    const scoreInterpretation = document.getElementById('scoreInterpretation');
    
    // Animate score
    animateValue(scoreValue, 0, score, 1500);
    
    // Update grade
    gradeDisplay.textContent = grade;
    
    // Update circle gradient
    const percentage = score;
    const color = getScoreColor(score);
    scoreCircle.style.background = `conic-gradient(${color} ${percentage}%, var(--surface-light) ${percentage}%)`;
    
    // Interpretation
    const interpretation = getScoreInterpretation(score);
    scoreInterpretation.textContent = interpretation;
}

// Display Metrics
function displayMetrics(metrics) {
    document.getElementById('loadTime').textContent = `${metrics.load_time?.toFixed(2) || '-'}s`;
    document.getElementById('pageSize').textContent = `${metrics.response_size_kb?.toFixed(0) || '-'}KB`;
    document.getElementById('sslStatus').textContent = metrics.ssl_enabled ? '✅ Enabled' : '❌ Disabled';
    document.getElementById('mobileStatus').textContent = metrics.mobile_friendly ? '✅ Yes' : '❌ No';
}

// Display Charts
function displayCharts(featureAnalysis) {
    // Feature Analysis Chart
    const featureCtx = document.getElementById('featureChart').getContext('2d');
    const perfData = featureAnalysis.performance;
    const secData = featureAnalysis.security;
    const seoData = featureAnalysis.seo;
    
    if (featureChart) featureChart.destroy();
    
    featureChart = new Chart(featureCtx, {
        type: 'bar',
        data: {
            labels: ['Load Time', 'Page Size', 'Compression', 'SSL', 'Mobile', 'SEO'],
            datasets: [{
                label: 'Status',
                data: [
                    perfData.load_time.status === 'good' ? 100 : 50,
                    perfData.page_size.status === 'good' ? 100 : 50,
                    perfData.compression.enabled ? 100 : 0,
                    secData.ssl.enabled ? 100 : 0,
                    seoData.mobile_friendly ? 100 : 0,
                    seoData.meta_description ? 100 : 0
                ],
                backgroundColor: [
                    perfData.load_time.status === 'good' ? '#10b981' : '#f59e0b',
                    perfData.page_size.status === 'good' ? '#10b981' : '#f59e0b',
                    perfData.compression.enabled ? '#10b981' : '#ef4444',
                    secData.ssl.enabled ? '#10b981' : '#ef4444',
                    seoData.mobile_friendly ? '#10b981' : '#ef4444',
                    seoData.meta_description ? '#10b981' : '#ef4444'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { color: '#cbd5e1' },
                    grid: { color: '#334155' }
                },
                x: {
                    ticks: { color: '#cbd5e1' },
                    grid: { color: '#334155' }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
    
    // Category Scores Chart
    const categoryCtx = document.getElementById('categoryChart').getContext('2d');
    
    if (categoryChart) categoryChart.destroy();
    
    categoryChart = new Chart(categoryCtx, {
        type: 'radar',
        data: {
            labels: ['Performance', 'Security', 'SEO', 'Mobile', 'Content'],
            datasets: [{
                label: 'Score',
                data: [
                    calculateCategoryScore(featureAnalysis.performance),
                    calculateCategoryScore(featureAnalysis.security),
                    calculateCategoryScore(featureAnalysis.seo),
                    seoData.mobile_friendly ? 100 : 0,
                    50  // Default for content
                ],
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderColor: '#3b82f6',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: { color: '#cbd5e1', backdropColor: 'transparent' },
                    grid: { color: '#334155' },
                    pointLabels: { color: '#cbd5e1' }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

// Display Anomalies
function displayAnomalies(anomalies) {
    const container = document.getElementById('anomaliesList');
    container.innerHTML = '';
    
    anomalies.forEach(anomaly => {
        const div = document.createElement('div');
        div.className = anomaly.includes('✅') ? 'anomaly-item success' : 'anomaly-item';
        div.textContent = anomaly;
        container.appendChild(div);
    });
}

// Display Recommendations
function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendationsList');
    container.innerHTML = '';
    
    if (recommendations.length === 0) {
        container.innerHTML = '<p>✅ No recommendations - your site looks great!</p>';
        return;
    }
    
    recommendations.forEach(rec => {
        const div = document.createElement('div');
        div.className = `recommendation-item ${rec.priority}`;
        div.innerHTML = `
            <div class="recommendation-header">
                <span class="recommendation-category">${rec.category}</span>
                <span class="recommendation-priority priority-${rec.priority}">${rec.priority}</span>
            </div>
            <div class="recommendation-issue">${rec.issue}</div>
            <div class="recommendation-details">
                Current: ${rec.current} → Target: ${rec.target}
            </div>
            <div class="recommendation-action">💡 ${rec.action}</div>
        `;
        container.appendChild(div);
    });
}

// Utility Functions
function showSection(section) {
    section.classList.remove('hidden');
}

function hideSection(section) {
    section.classList.add('hidden');
}

function updateProgress(percent) {
    progressFill.style.width = `${percent}%`;
    progressText.textContent = `${percent}%`;
}

function addLog(message, type = 'info') {
    const div = document.createElement('div');
    div.className = `log-entry log-${type}`;
    div.textContent = message;
    logsContainer.appendChild(div);
    logsContainer.scrollTop = logsContainer.scrollHeight;
}

function resetUI() {
    hideSection(resultsSection);
    logsContainer.innerHTML = '';
    updateProgress(0);
    
    // Remove new analysis button if exists
    const existingBtn = document.getElementById('newAnalysisBtn');
    if (existingBtn) {
        existingBtn.remove();
    }
}

function resetButton() {
    analyzeBtn.disabled = false;
    document.querySelector('.btn-text').textContent = 'Analyze URL';
}

function showNewAnalysisButton() {
    // Remove existing button if any
    const existing = document.getElementById('newAnalysisBtn');
    if (existing) existing.remove();
    
    // Create new analysis button
    const btnContainer = document.createElement('div');
    btnContainer.id = 'newAnalysisBtn';
    btnContainer.style.cssText = 'text-align: center; margin: 30px 0;';
    
    const newBtn = document.createElement('button');
    newBtn.className = 'btn btn-primary';
    newBtn.innerHTML = '<span>🔄 Analyze Another URL</span>';
    newBtn.onclick = () => {
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
        // Clear input
        urlInput.value = '';
        // Focus on input
        setTimeout(() => urlInput.focus(), 500);
        // Hide results
        hideSection(resultsSection);
        hideSection(progressSection);
        hideSection(logsSection);
    };
    
    btnContainer.appendChild(newBtn);
    resultsSection.appendChild(btnContainer);
}

function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.round(current);
    }, 16);
}

function getScoreColor(score) {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#3b82f6';
    if (score >= 40) return '#f59e0b';
    return '#ef4444';
}

function getScoreInterpretation(score) {
    if (score >= 90) return '🎉 Excellent! Your site is in great shape.';
    if (score >= 75) return '👍 Good! A few improvements could make it even better.';
    if (score >= 60) return '⚠️ Fair. Several areas need attention.';
    if (score >= 40) return '⚠️ Poor. Significant improvements needed.';
    return '❌ Critical. Immediate action required.';
}

function calculateCategoryScore(category) {
    let score = 0;
    let count = 0;
    
    for (const key in category) {
        const value = category[key];
        if (typeof value === 'object' && value.status) {
            score += value.status === 'good' ? 100 : value.status === 'warning' ? 50 : 0;
            count++;
        } else if (typeof value === 'boolean') {
            score += value ? 100 : 0;
            count++;
        }
    }
    
    return count > 0 ? score / count : 0;
}

// Initialize
console.log('TransparentML URL Diagnostics initialized');
