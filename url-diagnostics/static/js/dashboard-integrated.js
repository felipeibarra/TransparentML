// ============================================================================
// TransparentML Central Dashboard - Integrated with All ML Services + AI
// ============================================================================

// API Endpoints Configuration
const API_ENDPOINTS = {
    linearRegression: 'http://localhost:8001',
    pca: 'http://localhost:8002',
    urlDiagnostics: 'http://localhost:8003',
    knn: 'http://localhost:8004',
    vectorMemory: 'http://localhost:8005'  // NEW: Vector Memory Service
};

// AI Provider Configuration
const AI_CONFIG = {
    // Choose provider: 'ollama', 'groq', 'openai', or 'lmstudio'
    provider: 'ollama',  // DEFAULT: Ollama (100% free, local)
    
    // 🧠 NEW: Metacognition Configuration (AI that thinks about thinking)
    metacognition: {
        enabled: true,  // Enable metacognitive mode
        showConfidence: true,  // Show AI confidence scores (0-100%)
        showReasoning: true,  // Display step-by-step reasoning
        showKnowledgeGaps: true,  // Highlight what AI doesn't know
        showCorrections: true,  // Show self-corrections from past mistakes
        confidenceThreshold: 70,  // Warn if confidence below this %
        detailLevel: 'standard'  // 'minimal', 'standard', 'detailed'
    },
    
    // Vector Memory Configuration (Persistent Learning)
    vectorMemory: {
        enabled: true,  // Store all analyses and conversations
        autoStore: true,  // Automatically save ML results
        searchBeforeRespond: true,  // Search memory before AI responds
        maxSearchResults: 5  // Number of past results to consider
    },
    
    // Ollama Configuration (Recommended - Free & Local)
    ollama: {
        apiUrl: 'http://localhost:11434/api/chat',
        model: 'gemma:2b',  // FAST! 1.5GB, perfect for quick responses
        metacognitionModel: 'phi3',  // For deep analysis (separate panel)
        // No API key needed - runs in Docker container!
    },
    
    // Groq Configuration (Free Tier - Cloud)
    groq: {
        apiUrl: 'https://api.groq.com/openai/v1/chat/completions',
        apiKey: 'YOUR_GROQ_API_KEY_HERE',
        model: 'llama3-8b-8192'
    },
    
    // LM Studio Configuration (Free & Local)
    lmstudio: {
        apiUrl: 'http://localhost:1234/v1/chat/completions',
        model: 'local-model',  // Uses whatever model is loaded
        // No API key needed
    },
    
    // OpenAI Configuration (Paid)
    openai: {
        apiUrl: 'https://api.openai.com/v1/chat/completions',
        apiKey: 'YOUR_OPENAI_API_KEY',
        model: 'gpt-3.5-turbo'
    }
};

// Global State
let state = {
    currentModel: 'url-diagnostics',
    currentAnalysisId: null,
    mainChart: null,
    logsPaused: false,
    logsData: [],
    logStats: { total: 0, info: 0, warning: 0, error: 0 },
    mlContext: {}, // Stores ML results for AI chatbot
    chatHistory: [],
    metacognitionEnabled: AI_CONFIG.metacognition.enabled,  // Track metacognition mode
    memoryStats: { total_ml: 0, total_conversations: 0 }  // Vector memory stats
};

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 TransparentML Dashboard Initialized');
    initializeEventListeners();
    initializeCharts();
    updateChatProviderInfo();
    checkServicesHealth();
    
    // 💾 Load memory stats if enabled
    if (AI_CONFIG.vectorMemory.enabled) {
        getMemoryStats().then(() => updateMemoryStatsUI());
        // Update stats every 30 seconds
        setInterval(() => {
            getMemoryStats().then(() => updateMemoryStatsUI());
        }, 30000);
    }
    
    // 🎨 Load theme from localStorage
    loadTheme();
    
    // 📊 Load demo data for professional first-impression
    loadDemoData();
    
    // 📈 Update KPIs periodically
    updateKPIs();
    setInterval(updateKPIs, 5000);
});

function initializeEventListeners() {
    // Model Selection
    document.getElementById('modelSelect')?.addEventListener('change', handleModelChange);
    
    // URL Diagnostics
    document.getElementById('analyzeUrlBtn')?.addEventListener('click', handleUrlAnalysis);
    
    // Linear Regression
    document.getElementById('trainLrBtn')?.addEventListener('click', handleLinearRegressionDemo);
    
    // PCA
    document.getElementById('runPcaBtn')?.addEventListener('click', handlePCAAnalysis);
    
    // KNN - Add button to HTML first
    const knnConfig = document.getElementById('pcaConfig').parentElement;
    if (!document.getElementById('knnConfig')) {
        const knnConfigHTML = `
            <div id="knnConfig" class="model-config hidden">
                <h3>K-Nearest Neighbors</h3>
                <div class="form-group">
                    <label>Dataset:</label>
                    <select id="knnDataset" class="input-field">
                        <option value="iris">Iris Dataset</option>
                        <option value="random">Random Dataset</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>K Neighbors:</label>
                    <input type="number" id="knnNeighbors" value="5" min="1" max="20" class="input-field">
                </div>
                <button id="runKnnBtn" class="btn btn-primary">🎯 Run KNN</button>
            </div>
        `;
        document.getElementById('pcaConfig').insertAdjacentHTML('afterend', knnConfigHTML);
    }
    document.getElementById('runKnnBtn')?.addEventListener('click', handleKNNAnalysis);
    
    // Update model select to include KNN
    const modelSelect = document.getElementById('modelSelect');
    if (modelSelect && !modelSelect.querySelector('[value="knn"]')) {
        const knnOption = document.createElement('option');
        knnOption.value = 'knn';
        knnOption.textContent = '🎯 K-Nearest Neighbors';
        modelSelect.insertBefore(knnOption, modelSelect.querySelector('[value="all"]'));
    }
    
    // Log Controls
    document.getElementById('clearLogsBtn')?.addEventListener('click', clearLogs);
    document.getElementById('pauseLogsBtn')?.addEventListener('click', togglePauseLogs);
    document.getElementById('exportLogsBtn')?.addEventListener('click', exportLogs);
    
    // Clear All
    document.getElementById('clearBtn')?.addEventListener('click', clearAll);
    
    // Graph Controls
    document.querySelectorAll('.graph-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.graph-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            updateMainChart(e.target.dataset.chart);
        });
    });
    
    // AI Chatbot
    document.getElementById('sendChatBtn')?.addEventListener('click', handleSendMessage);
    document.getElementById('chatInput')?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSendMessage();
    });
    document.getElementById('toggleChatbot')?.addEventListener('click', toggleChatbot);
    
    // 🧠 AI Analyst Panel
    document.getElementById('toggleAnalyst')?.addEventListener('click', toggleAnalyst);
    
    // Theme Toggle
    document.getElementById('themeToggle')?.addEventListener('click', toggleTheme);
}

// ============================================================================
// SERVICE HEALTH CHECKS
// ============================================================================

async function checkServicesHealth() {
    addLog('🔍 Checking ML services health...', 'info');
    
    const services = [
        { name: 'Linear Regression', url: `${API_ENDPOINTS.linearRegression}/health` },
        { name: 'PCA', url: `${API_ENDPOINTS.pca}/health` },
        { name: 'URL Diagnostics', url: `${API_ENDPOINTS.urlDiagnostics}/health` },
        { name: 'KNN', url: `${API_ENDPOINTS.knn}/health` },
        { name: '💾 Vector Memory', url: `${API_ENDPOINTS.vectorMemory}/health` }
    ];
    
    for (const service of services) {
        try {
            const response = await fetch(service.url);
            if (response.ok) {
                addLog(`✅ ${service.name} service is healthy`, 'info');
            } else {
                addLog(`⚠️ ${service.name} service returned ${response.status}`, 'warning');
            }
        } catch (error) {
            addLog(`❌ ${service.name} service is down`, 'error');
        }
    }
}

// ============================================================================
// MODEL SELECTION
// ============================================================================

function handleModelChange(e) {
    const model = e.target.value;
    state.currentModel = model;
    
    // Hide all configs
    document.querySelectorAll('.model-config').forEach(config => {
        config.classList.add('hidden');
    });
    
    // Show selected config
    switch(model) {
        case 'url-diagnostics':
            document.getElementById('urlDiagConfig').classList.remove('hidden');
            document.getElementById('currentModel').textContent = 'URL Diagnostics';
            break;
        case 'linear-regression':
            document.getElementById('linearRegConfig').classList.remove('hidden');
            document.getElementById('currentModel').textContent = 'Linear Regression';
            break;
        case 'pca':
            document.getElementById('pcaConfig').classList.remove('hidden');
            document.getElementById('currentModel').textContent = 'PCA Analysis';
            break;
        case 'knn':
            document.getElementById('knnConfig').classList.remove('hidden');
            document.getElementById('currentModel').textContent = 'K-Nearest Neighbors';
            break;
        case 'all':
            document.querySelectorAll('.model-config').forEach(config => {
                config.classList.remove('hidden');
            });
            document.getElementById('currentModel').textContent = 'All Models';
            break;
    }
    
    addLog(`📊 Switched to ${document.getElementById('currentModel').textContent}`, 'info');
}

// ============================================================================
// URL DIAGNOSTICS HANDLER
// ============================================================================

async function handleUrlAnalysis() {
    const url = document.getElementById('urlInput').value.trim();
    const analysisType = document.getElementById('analysisType').value;
    
    if (!url) {
        addLog('❌ Please enter a URL', 'error');
        return;
    }
    
    addLog(`🚀 Starting URL analysis for: ${url}`, 'info');
    updateStatus('running');
    updateProgress(10);
    
    try {
        const response = await fetch(`${API_ENDPOINTS.urlDiagnostics}/api/v1/analyze/sync`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, analysis_type: analysisType })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const results = await response.json();
        
        addLog('✅ URL analysis completed!', 'info');
        updateProgress(100);
        updateStatus('complete');
        
        // Store results for AI
        state.mlContext.urlDiagnostics = results;
        
        // 💾 Store in vector memory
        await storeMLResult('url_diagnostics', results, { url, analysis_type: analysisType });
        
        // Display results
        displayUrlDiagnostics(results);
        
        // 🧠 Trigger AI Analyst auto-analysis
        triggerAutoAnalysis('URL Diagnostics', results);
        
        // Enable chatbot
        enableChatbot();
        
    } catch (error) {
        addLog(`❌ Error: ${error.message}`, 'error');
        updateStatus('error');
    }
}

function displayUrlDiagnostics(results) {
    // Update stats
    document.getElementById('statScore').textContent = results.health_score?.toFixed(1) || '--';
    document.getElementById('statTime').textContent = `${results.metrics?.load_time?.toFixed(2) || 0}s`;
    document.getElementById('statDataPoints').textContent = '41';
    document.getElementById('statAccuracy').textContent = results.grade || '--';
    
    // Display results
    const resultsHtml = `
        <div class="result-score">
            <div class="grade-badge">${results.grade}</div>
            <div class="score-big">${results.health_score?.toFixed(1) || 0}</div>
            <div class="score-label">Health Score</div>
        </div>
        <div class="result-metrics">
            <div class="metric-item">
                <span class="metric-label">Load Time</span>
                <span class="metric-value">${results.metrics?.load_time?.toFixed(2) || 0}s</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">Status Code</span>
                <span class="metric-value">${results.metrics?.status_code || '--'}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">SSL Enabled</span>
                <span class="metric-value">${results.metrics?.ssl_enabled ? '✅' : '❌'}</span>
            </div>
        </div>
    `;
    document.getElementById('resultsContainer').innerHTML = resultsHtml;
    
    // Display recommendations
    if (results.recommendations && results.recommendations.length > 0) {
        const recsHtml = results.recommendations.map(rec => `
            <div class="rec-item priority-${rec.priority?.toLowerCase()}">
                <div class="rec-header">
                    <span class="rec-category">${rec.category}</span>
                    <span class="rec-priority">${rec.priority}</span>
                </div>
                <div class="rec-issue">${rec.issue}</div>
                <div class="rec-action">${rec.action}</div>
            </div>
        `).join('');
        document.getElementById('recommendationsContainer').innerHTML = recsHtml;
    }
    
    // Update chart
    updateChartWithData([
        results.health_score,
        results.metrics?.load_time * 10,
        results.metrics?.response_size_kb / 10
    ]);
}

// ============================================================================
// LINEAR REGRESSION HANDLER
// ============================================================================

async function handleLinearRegressionDemo() {
    addLog('🎯 Training Linear Regression model...', 'info');
    updateStatus('running');
    updateProgress(25);
    
    try {
        const response = await fetch(`${API_ENDPOINTS.linearRegression}/api/v1/demo/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ n_samples: 100, noise: 10.0 })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const results = await response.json();
        
        addLog(`✅ Model trained! R² = ${results.metrics.r2_score.toFixed(4)}`, 'info');
        updateProgress(100);
        updateStatus('complete');
        
        // Store results for AI
        state.mlContext.linearRegression = results;
        
        // 💾 Store in vector memory
        await storeMLResult('linear_regression', results, { n_samples: 100, noise: 10.0 });
        
        // Display results
        displayLinearRegression(results);
        
        // 🧠 Trigger AI Analyst auto-analysis
        triggerAutoAnalysis('Linear Regression', results);
        
        // Enable chatbot
        enableChatbot();
        
    } catch (error) {
        addLog(`❌ Error: ${error.message}`, 'error');
        updateStatus('error');
    }
}

function displayLinearRegression(results) {
    const metrics = results.metrics;
    
    // Update stats
    document.getElementById('statScore').textContent = (metrics.r2_score * 100).toFixed(1);
    document.getElementById('statTime').textContent = '--';
    document.getElementById('statDataPoints').textContent = metrics.n_train_samples + metrics.n_test_samples;
    document.getElementById('statAccuracy').textContent = `R²: ${metrics.r2_score.toFixed(3)}`;
    
    // Display results
    const resultsHtml = `
        <div class="result-score">
            <div class="score-big">${metrics.r2_score.toFixed(4)}</div>
            <div class="score-label">R² Score</div>
        </div>
        <div class="result-metrics">
            <div class="metric-item">
                <span class="metric-label">RMSE</span>
                <span class="metric-value">${metrics.rmse.toFixed(2)}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">MAE</span>
                <span class="metric-value">${metrics.mae.toFixed(2)}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">Slope</span>
                <span class="metric-value">${results.model_coefficients.slope.toFixed(2)}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">Intercept</span>
                <span class="metric-value">${results.model_coefficients.intercept.toFixed(2)}</span>
            </div>
        </div>
    `;
    document.getElementById('resultsContainer').innerHTML = resultsHtml;
    
    // Update chart with scatter data
    updateChartWithData([
        metrics.r2_score * 100,
        100 - metrics.rmse,
        100 - metrics.mae
    ]);
}

// ============================================================================
// PCA HANDLER
// ============================================================================

async function handlePCAAnalysis() {
    addLog('🌈 Running PCA analysis on Iris dataset...', 'info');
    updateStatus('running');
    updateProgress(30);
    
    try {
        const response = await fetch(`${API_ENDPOINTS.pca}/analysis`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const results = await response.json();
        
        addLog(`✅ PCA completed! Variance explained: ${(results.manual_variance_ratio[0] * 100).toFixed(1)}%`, 'info');
        updateProgress(100);
        updateStatus('complete');
        
        // Store results for AI
        state.mlContext.pca = results;
        
        // 💾 Store in vector memory
        await storeMLResult('pca', results, { dataset: 'iris' });
        
        // Display results
        displayPCA(results);
        
        // 🧠 Trigger AI Analyst auto-analysis
        triggerAutoAnalysis('PCA', results);
        
        // Enable chatbot
        enableChatbot();
        
    } catch (error) {
        addLog(`❌ Error: ${error.message}`, 'error');
        updateStatus('error');
    }
}

function displayPCA(results) {
    const variance = results.manual_variance_ratio;
    const totalVariance = variance.reduce((a, b) => a + b, 0) * 100;
    
    // Update stats
    document.getElementById('statScore').textContent = totalVariance.toFixed(1);
    document.getElementById('statTime').textContent = '--';
    document.getElementById('statDataPoints').textContent = results.samples;
    document.getElementById('statAccuracy').textContent = `${totalVariance.toFixed(1)}%`;
    
    // Display results
    const resultsHtml = `
        <div class="result-score">
            <div class="score-big">${totalVariance.toFixed(1)}%</div>
            <div class="score-label">Variance Explained</div>
        </div>
        <div class="result-metrics">
            <div class="metric-item">
                <span class="metric-label">PC1 Variance</span>
                <span class="metric-value">${(variance[0] * 100).toFixed(1)}%</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">PC2 Variance</span>
                <span class="metric-value">${(variance[1] * 100).toFixed(1)}%</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">Components</span>
                <span class="metric-value">${variance.length}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">Features</span>
                <span class="metric-value">${results.features.length}</span>
            </div>
        </div>
    `;
    document.getElementById('resultsContainer').innerHTML = resultsHtml;
    
    // Update chart
    updateChartWithData(variance.map(v => v * 100));
}

// ============================================================================
// KNN HANDLER
// ============================================================================

async function handleKNNAnalysis() {
    const dataset = document.getElementById('knnDataset').value;
    const nNeighbors = parseInt(document.getElementById('knnNeighbors').value);
    
    addLog(`🎯 Training KNN classifier with k=${nNeighbors}...`, 'info');
    updateStatus('running');
    updateProgress(35);
    
    try {
        const response = await fetch(`${API_ENDPOINTS.knn}/api/v1/demo/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dataset, n_neighbors: nNeighbors, test_size: 0.3 })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const results = await response.json();
        
        addLog(`✅ KNN trained! Accuracy: ${(results.metrics.accuracy * 100).toFixed(1)}%`, 'info');
        updateProgress(100);
        updateStatus('complete');
        
        // Store results for AI
        state.mlContext.knn = results;
        
        // 💾 Store in vector memory
        await storeMLResult('knn', results, { dataset, n_neighbors: nNeighbors });
        
        // Display results
        displayKNN(results);
        
        // 🧠 Trigger AI Analyst auto-analysis
        triggerAutoAnalysis('KNN', results);
        
        // Enable chatbot
        enableChatbot();
        
    } catch (error) {
        addLog(`❌ Error: ${error.message}`, 'error');
        updateStatus('error');
    }
}

function displayKNN(results) {
    const metrics = results.metrics;
    
    // Update stats
    document.getElementById('statScore').textContent = (metrics.accuracy * 100).toFixed(1);
    document.getElementById('statTime').textContent = '--';
    document.getElementById('statDataPoints').textContent = metrics.n_train_samples + metrics.n_test_samples;
    document.getElementById('statAccuracy').textContent = `${(metrics.accuracy * 100).toFixed(1)}%`;
    
    // Display results
    const resultsHtml = `
        <div class="result-score">
            <div class="score-big">${(metrics.accuracy * 100).toFixed(1)}%</div>
            <div class="score-label">Accuracy</div>
        </div>
        <div class="result-metrics">
            <div class="metric-item">
                <span class="metric-label">K Neighbors</span>
                <span class="metric-value">${metrics.n_neighbors}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">Classes</span>
                <span class="metric-value">${metrics.n_classes}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">Features</span>
                <span class="metric-value">${metrics.n_features}</span>
            </div>
            <div class="metric-item">
                <span class="metric-label">Test Samples</span>
                <span class="metric-value">${metrics.n_test_samples}</span>
            </div>
        </div>
    `;
    document.getElementById('resultsContainer').innerHTML = resultsHtml;
    
    // Update chart with class accuracies
    if (results.class_metrics) {
        updateChartWithData(results.class_metrics.map(cm => cm.accuracy * 100));
    }
}

// ============================================================================
// AI CHATBOT INTEGRATION
// ============================================================================

function enableChatbot() {
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendChatBtn');
    
    if (chatInput && sendBtn) {
        chatInput.disabled = false;
        sendBtn.disabled = false;
        chatInput.placeholder = 'Ask about your ML results...';
        addLog('🤖 AI Assistant enabled - ask questions about your results!', 'info');
        
        // Show available ML context in chatbot
        const context = buildMLContext();
        if (Object.keys(state.mlContext).length > 0) {
            addChatMessage(`📊 New analysis results available! ${context}`, 'assistant');
        }
    }
}

async function handleSendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Add user message
    addChatMessage(message, 'user');
    chatInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    // Get AI response
    try {
        const aiResponse = await getAIResponse(message);
        removeTypingIndicator();
        addChatMessage(aiResponse, 'assistant');
        
        // 🧠 Store conversation in vector memory if enabled
        if (AI_CONFIG.vectorMemory.enabled && AI_CONFIG.vectorMemory.autoStore) {
            await storeConversation(message, aiResponse);
        }
    } catch (error) {
        removeTypingIndicator();
        addChatMessage(`Sorry, I encountered an error: ${error.message}`, 'assistant');
        addLog(`❌ Chatbot error: ${error.message}`, 'error');
    }
}

async function getAIResponse(userMessage) {
    const context = buildMLContext();
    const provider = AI_CONFIG.provider;
    const config = AI_CONFIG[provider];
    
    // 🔍 Search vector memory for relevant past information
    let memoryContext = '';
    if (AI_CONFIG.vectorMemory.enabled && AI_CONFIG.vectorMemory.searchBeforeRespond) {
        memoryContext = await searchVectorMemory(userMessage);
    }
    
    // 🧠 Build system message with metacognition if enabled
    let systemMessage;
    if (state.metacognitionEnabled) {
        systemMessage = buildMetacognitivePrompt(context, memoryContext);
    } else {
        systemMessage = `You are an ML analysis assistant for TransparentML platform. You help users interpret results from Linear Regression, PCA, URL Diagnostics, and KNN algorithms. Be concise, technical but accessible. Current context: ${context}`;
        if (memoryContext) {
            systemMessage += `\n\nRelevant past information: ${memoryContext}`;
        }
    }
    
    try {
        let aiMessage;
        
        if (provider === 'ollama') {
            aiMessage = await getOllamaResponse(userMessage, systemMessage, config);
        } else if (provider === 'groq') {
            aiMessage = await getGroqResponse(userMessage, systemMessage, config);
        } else if (provider === 'lmstudio') {
            aiMessage = await getLMStudioResponse(userMessage, systemMessage, config);
        } else if (provider === 'openai') {
            aiMessage = await getOpenAIResponse(userMessage, systemMessage, config);
        } else {
            throw new Error(`Unknown provider: ${provider}`);
        }
        
        // Update chat history
        state.chatHistory.push(
            { role: 'user', content: userMessage },
            { role: 'assistant', content: aiMessage }
        );
        
        return aiMessage;
        
    } catch (error) {
        console.error('AI Error:', error);
        return `⚠️ Error: ${error.message}\n\n💡 Tip: Make sure ${provider} is running and accessible.\n\nContext available: ${Object.keys(state.mlContext).join(', ')}`;
    }
}

// Ollama API Call (Local, Free)
async function getOllamaResponse(userMessage, systemMessage, config) {
    const messages = [
        { role: 'system', content: systemMessage },
        ...state.chatHistory,
        { role: 'user', content: userMessage }
    ];
    
    const response = await fetch(config.apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            model: config.model,
            messages: messages,
            stream: false
        })
    });
    
    if (!response.ok) {
        throw new Error(`Ollama not running or model not available. Run: ollama run ${config.model}`);
    }
    
    const data = await response.json();
    return data.message.content;
}

// Groq API Call (Cloud, Free Tier)
async function getGroqResponse(userMessage, systemMessage, config) {
    if (!config.apiKey || config.apiKey === 'YOUR_GROQ_API_KEY_HERE') {
        throw new Error('Groq API key not set. Get free key at https://console.groq.com');
    }
    
    const messages = [
        { role: 'system', content: systemMessage },
        ...state.chatHistory,
        { role: 'user', content: userMessage }
    ];
    
    const response = await fetch(config.apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${config.apiKey}`
        },
        body: JSON.stringify({
            model: config.model,
            messages: messages,
            temperature: 0.7,
            max_tokens: 500
        })
    });
    
    if (!response.ok) {
        throw new Error(`Groq API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.choices[0].message.content;
}

// LM Studio API Call (Local, Free)
async function getLMStudioResponse(userMessage, systemMessage, config) {
    const messages = [
        { role: 'system', content: systemMessage },
        ...state.chatHistory,
        { role: 'user', content: userMessage }
    ];
    
    const response = await fetch(config.apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            model: config.model,
            messages: messages,
            temperature: 0.7,
            max_tokens: 500
        })
    });
    
    if (!response.ok) {
        throw new Error('LM Studio not running. Start LM Studio and load a model.');
    }
    
    const data = await response.json();
    return data.choices[0].message.content;
}

// OpenAI API Call (Cloud, Paid)
async function getOpenAIResponse(userMessage, systemMessage, config) {
    if (!config.apiKey || config.apiKey === 'YOUR_OPENAI_API_KEY') {
        throw new Error('OpenAI API key not set.');
    }
    
    const messages = [
        { role: 'system', content: systemMessage },
        ...state.chatHistory,
        { role: 'user', content: userMessage }
    ];
    
    const response = await fetch(config.apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${config.apiKey}`
        },
        body: JSON.stringify({
            model: config.model,
            messages: messages,
            temperature: 0.7,
            max_tokens: 500
        })
    });
    
    if (!response.ok) {
        throw new Error(`OpenAI API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.choices[0].message.content;
}

function buildMLContext() {
    let context = 'Available ML results: ';
    
    if (state.mlContext.urlDiagnostics) {
        context += `URL Diagnostics (health score: ${state.mlContext.urlDiagnostics.health_score}, grade: ${state.mlContext.urlDiagnostics.grade}), `;
    }
    if (state.mlContext.linearRegression) {
        context += `Linear Regression (R²: ${state.mlContext.linearRegression.metrics.r2_score.toFixed(3)}), `;
    }
    if (state.mlContext.pca) {
        context += `PCA (variance: ${(state.mlContext.pca.manual_variance_ratio[0] * 100).toFixed(1)}%), `;
    }
    if (state.mlContext.knn) {
        context += `KNN (accuracy: ${(state.mlContext.knn.metrics.accuracy * 100).toFixed(1)}%), `;
    }
    
    return context || 'No analyses run yet';
}

function addChatMessage(content, role) {
    const messagesContainer = document.getElementById('chatMessages');
    const avatar = role === 'user' ? '👤' : '🤖';
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}`;
    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <p>${content}</p>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    const indicator = document.createElement('div');
    indicator.id = 'typing-indicator';
    indicator.className = 'chat-message assistant';
    indicator.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    messagesContainer.appendChild(indicator);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
}

function updateChatProviderInfo() {
    const provider = AI_CONFIG.provider;
    const providerEl = document.getElementById('chatProvider');
    
    if (!providerEl) return;
    
    const providerInfo = {
        ollama: 'Powered by Ollama (Local & Free) • 100% Private',
        groq: 'Powered by Groq (Cloud & Free) • Fast Inference',
        lmstudio: 'Powered by LM Studio (Local & Free) • 100% Private',
        openai: 'Powered by OpenAI (Cloud & Paid) • GPT Models'
    };
    
    providerEl.textContent = providerInfo[provider] || 'AI Assistant';
}

function toggleChatbot() {
    const panel = document.querySelector('.chatbot-panel');
    const toggle = document.getElementById('toggleChatbot');
    
    if (panel.classList.contains('minimized')) {
        panel.classList.remove('minimized');
        toggle.textContent = '▼';
        toggle.title = 'Minimize chatbot';
    } else {
        panel.classList.add('minimized');
        toggle.textContent = '▲';
        toggle.title = 'Expand chatbot';
    }
}

// ============================================================================
// CHARTS
// ============================================================================

function initializeCharts() {
    // Main chart
    const mainCtx = document.getElementById('mainChart');
    if (mainCtx) {
        state.mainChart = new Chart(mainCtx, {
            type: 'bar',
            data: {
                labels: ['Metric 1', 'Metric 2', 'Metric 3', 'Metric 4'],
                datasets: [{
                    label: 'Analysis Results',
                    data: [0, 0, 0, 0],
                    backgroundColor: 'rgba(59, 130, 246, 0.6)',
                    borderColor: 'rgba(59, 130, 246, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }
    
    // Timeline chart removed - now available on dedicated /timeline page
}

function updateMainChart(type) {
    if (!state.mainChart) return;
    
    state.mainChart.config.type = type;
    state.mainChart.update();
}

function updateChartWithData(data) {
    if (!state.mainChart) return;
    
    state.mainChart.data.datasets[0].data = data;
    state.mainChart.update();
}

// ============================================================================
// LOGGING & UI UTILITIES
// ============================================================================

function addLog(message, level = 'info') {
    if (state.logsPaused) return;
    
    const logsContainer = document.getElementById('logsContainer');
    if (!logsContainer) return;
    
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${level}`;
    logEntry.textContent = `[${timestamp}] ${message}`;
    
    logsContainer.appendChild(logEntry);
    logsContainer.scrollTop = logsContainer.scrollHeight;
    
    // Update stats
    state.logStats.total++;
    state.logStats[level]++;
    updateLogStats();
    
    // Store log
    state.logsData.push({ timestamp, message, level });
}

function updateLogStats() {
    document.getElementById('logStatTotal').textContent = state.logStats.total;
    document.getElementById('logStatInfo').textContent = state.logStats.info;
    document.getElementById('logStatWarning').textContent = state.logStats.warning;
    document.getElementById('logStatError').textContent = state.logStats.error;
    
    const errorRate = state.logStats.total > 0 
        ? (state.logStats.error / state.logStats.total * 100).toFixed(1) 
        : 0;
    document.getElementById('logStatErrorRate').textContent = `${errorRate}%`;
    
    // Update logs count display
    const logsCount = document.getElementById('logsCount');
    if (logsCount) {
        logsCount.textContent = `${state.logStats.total} log${state.logStats.total !== 1 ? 's' : ''}`;
    }
}

// Timeline chart removed - now available on dedicated /timeline page

function clearLogs() {
    document.getElementById('logsContainer').innerHTML = '';
    state.logsData = [];
    state.logStats = { total: 0, info: 0, warning: 0, error: 0 };
    updateLogStats();
}

function togglePauseLogs() {
    state.logsPaused = !state.logsPaused;
    const btn = document.getElementById('pauseLogsBtn');
    btn.textContent = state.logsPaused ? '▶️' : '⏸️';
    btn.title = state.logsPaused ? 'Resume logs' : 'Pause logs';
}

function exportLogs() {
    const content = state.logsData.map(log => 
        `[${log.timestamp}] [${log.level.toUpperCase()}] ${log.message}`
    ).join('\n');
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `transparentml-logs-${new Date().toISOString()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    
    addLog('💾 Logs exported successfully', 'info');
}

function updateProgress(percent) {
    const fill = document.getElementById('progressFill');
    const text = document.getElementById('progressPercent');
    if (fill && text) {
        fill.style.width = `${percent}%`;
        text.textContent = `${percent}%`;
    }
}

function updateStatus(status) {
    const statusEl = document.getElementById('modelStatus');
    if (statusEl) {
        statusEl.className = `status-value status-${status}`;
        statusEl.textContent = status.charAt(0).toUpperCase() + status.slice(1);
    }
}

function updateLastRun() {
    document.getElementById('lastRun').textContent = new Date().toLocaleTimeString();
}

function clearAll() {
    clearLogs();
    document.getElementById('resultsContainer').innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">📊</div>
            <p>No results yet</p>
        </div>
    `;
    document.getElementById('recommendationsContainer').innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">💡</div>
            <p>No recommendations</p>
        </div>
    `;
    document.getElementById('statScore').textContent = '--';
    document.getElementById('statTime').textContent = '--';
    document.getElementById('statDataPoints').textContent = '--';
    document.getElementById('statAccuracy').textContent = '--';
    updateProgress(0);
    updateStatus('idle');
    
    addLog('🗑️ Dashboard cleared', 'info');
}

// ============================================================================
// 🧠 METACOGNITION SYSTEM - AI That Thinks About Thinking
// ============================================================================

function buildMetacognitivePrompt(currentContext, memoryContext) {
    const detailLevel = AI_CONFIG.metacognition.detailLevel;
    const showConfidence = AI_CONFIG.metacognition.showConfidence;
    const showReasoning = AI_CONFIG.metacognition.showReasoning;
    const showGaps = AI_CONFIG.metacognition.showKnowledgeGaps;
    
    let prompt = `You are an AI with METACOGNITIVE ABILITIES for the TransparentML platform. 
You help users interpret results from Linear Regression, PCA, URL Diagnostics, and KNN algorithms.

📊 CURRENT ML CONTEXT:
${currentContext}

`;
    
    if (memoryContext) {
        prompt += `💾 PAST EXPERIENCES (from vector memory):
${memoryContext}

`;
    }
    
    prompt += `🧠 METACOGNITIVE INSTRUCTIONS:

For EVERY response, you must:

1. ANALYZE YOUR KNOWLEDGE
   - What do you know about this topic?
   - What relevant past experiences do you have?
   - What are you uncertain about?

2. SHOW YOUR REASONING (if enabled: ${showReasoning})
   - Explain your thought process step-by-step
   - Show how you arrived at your conclusion
   - Identify assumptions you're making

3. ASSESS YOUR CONFIDENCE (if enabled: ${showConfidence})
   - Rate your certainty as a percentage (0-100%)
   - Explain why you're confident or uncertain
   - Identify what would increase your confidence

4. ACKNOWLEDGE GAPS (if enabled: ${showGaps})
   - What information are you missing?
   - What could you learn to improve?
   - What questions should you ask the user?

5. BE TRANSPARENT
   - Show your reasoning chains
   - Admit when you're guessing
   - Explain trade-offs in recommendations

`;
    
    // Adjust detail level
    if (detailLevel === 'minimal') {
        prompt += `RESPONSE FORMAT (MINIMAL):
- Brief answer
- Confidence: X%
- One key uncertainty`;
    } else if (detailLevel === 'standard') {
        prompt += `RESPONSE FORMAT (STANDARD):
📊 Answer: [Your main response]

🧠 My Reasoning:
- [Key reasoning steps]

⚡ Confidence: X%
- [Why this confidence level]

🎯 What I'm unsure about:
- [Key uncertainties or missing info]`;
    } else { // detailed
        prompt += `RESPONSE FORMAT (DETAILED):
📊 Answer: [Your main response]

🧠 My Reasoning:
Step 1: [First reasoning step]
Step 2: [Second reasoning step]
Step 3: [Conclusion]

💾 Past Experience:
- [Relevant past analyses from memory]

⚡ Confidence: X%
- [Detailed confidence explanation]

🎯 What I'm unsure about:
- [Key uncertainties]

💡 How I can improve:
- [What additional info would help]`;
    }
    
    prompt += `\n\nALWAYS use emojis to make sections clear. Be technical but accessible.`;
    
    return prompt;
}

function toggleMetacognition() {
    state.metacognitionEnabled = !state.metacognitionEnabled;
    const btn = document.getElementById('toggleMetacognition');
    
    if (btn) {
        if (state.metacognitionEnabled) {
            btn.textContent = '🧠 Metacognition: ON';
            btn.classList.add('active');
            addLog('🧠 Metacognition mode enabled - AI will explain its reasoning', 'info');
            addChatMessage('🧠 Metacognition mode activated! I will now show my reasoning process, confidence levels, and knowledge gaps.', 'assistant');
        } else {
            btn.textContent = '🧠 Metacognition: OFF';
            btn.classList.remove('active');
            addLog('ℹ️ Standard mode enabled - concise responses', 'info');
            addChatMessage('ℹ️ Standard mode activated. I\'ll provide concise responses without detailed reasoning.', 'assistant');
        }
    }
}

// ============================================================================
// 💾 VECTOR MEMORY INTEGRATION - Persistent Learning
// ============================================================================

// Store ML analysis results in vector memory
async function storeMLResult(algorithmType, results, metadata = {}) {
    if (!AI_CONFIG.vectorMemory.enabled) return;
    
    try {
        const payload = {
            algorithm_type: algorithmType,
            results: results,
            metadata: {
                timestamp: new Date().toISOString(),
                model: state.currentModel,
                ...metadata
            }
        };
        
        const response = await fetch(`${API_ENDPOINTS.vectorMemory}/api/v1/memory/ml-result`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            const data = await response.json();
            state.memoryStats.total_ml++;
            addLog(`💾 Stored ${algorithmType} results in memory`, 'info');
            return data;
        }
    } catch (error) {
        console.error('Vector memory storage error:', error);
        // Don't fail the main flow if memory storage fails
    }
}

// Store conversation in vector memory
async function storeConversation(userMessage, aiResponse) {
    if (!AI_CONFIG.vectorMemory.enabled) return;
    
    try {
        const payload = {
            user_message: userMessage,
            ai_response: aiResponse,
            context: buildMLContext(),
            metadata: {
                timestamp: new Date().toISOString(),
                metacognition_enabled: state.metacognitionEnabled
            }
        };
        
        const response = await fetch(`${API_ENDPOINTS.vectorMemory}/api/v1/memory/conversation`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            state.memoryStats.total_conversations++;
            console.log('💾 Conversation stored in memory');
        }
    } catch (error) {
        console.error('Conversation storage error:', error);
    }
}

// Search vector memory for relevant information
async function searchVectorMemory(query) {
    if (!AI_CONFIG.vectorMemory.enabled) return '';
    
    try {
        // Search both ML results and past conversations
        const [mlResults, convResults] = await Promise.all([
            fetch(`${API_ENDPOINTS.vectorMemory}/api/v1/search/ml`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: query,
                    n_results: AI_CONFIG.vectorMemory.maxSearchResults
                })
            }),
            fetch(`${API_ENDPOINTS.vectorMemory}/api/v1/search/conversations`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: query,
                    n_results: AI_CONFIG.vectorMemory.maxSearchResults
                })
            })
        ]);
        
        let memoryContext = '';
        
        if (mlResults.ok) {
            const mlData = await mlResults.json();
            if (mlData.results && mlData.results.length > 0) {
                memoryContext += 'Past ML Analyses: ';
                mlData.results.forEach((result, i) => {
                    memoryContext += `(${i+1}) ${result.algorithm_type} - ${JSON.stringify(result.results).substring(0, 100)}... `;
                });
            }
        }
        
        if (convResults.ok) {
            const convData = await convResults.json();
            if (convData.results && convData.results.length > 0) {
                memoryContext += 'Past Conversations: ';
                convData.results.forEach((conv, i) => {
                    memoryContext += `(${i+1}) Q: "${conv.user_message.substring(0, 50)}..." A: "${conv.ai_response.substring(0, 50)}..." `;
                });
            }
        }
        
        return memoryContext;
        
    } catch (error) {
        console.error('Vector memory search error:', error);
        return '';
    }
}

// Get memory statistics
async function getMemoryStats() {
    if (!AI_CONFIG.vectorMemory.enabled) return null;
    
    try {
        const response = await fetch(`${API_ENDPOINTS.vectorMemory}/api/v1/stats`);
        if (response.ok) {
            const stats = await response.json();
            state.memoryStats = stats;
            return stats;
        }
    } catch (error) {
        console.error('Memory stats error:', error);
    }
    return null;
}

// Update UI with memory stats
function updateMemoryStatsUI() {
    const statsEl = document.getElementById('memoryStats');
    if (statsEl && state.memoryStats) {
        statsEl.innerHTML = `
            💾 Memory: ${state.memoryStats.total_ml || 0} ML | ${state.memoryStats.total_conversations || 0} Chats
        `;
    }
}

// ============================================================================
// 🧠 AI ANALYST - Automatic Deep Analysis Panel
// ============================================================================

// Toggle AI Analyst panel
function toggleAnalyst() {
    const panel = document.querySelector('.analyst-panel');
    const toggle = document.getElementById('toggleAnalyst');
    
    if (panel.classList.contains('minimized')) {
        panel.classList.remove('minimized');
        toggle.textContent = '▼';
        toggle.title = 'Minimize analyst';
    } else {
        panel.classList.add('minimized');
        toggle.textContent = '▲';
        toggle.title = 'Expand analyst';
    }
}

// Update AI Analyst status
function updateAnalystStatus(status, text) {
    const statusEl = document.querySelector('.status-indicator');
    const textEl = document.getElementById('analystStatus');
    
    statusEl.className = `status-indicator ${status}`;
    textEl.textContent = text;
}

// Add message to AI Analyst panel
function addAnalystMessage(title, content, icon = '🧠') {
    const messagesContainer = document.getElementById('analystMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'analyst-message';
    messageDiv.innerHTML = `
        <div class="message-header">
            <span class="message-icon">${icon}</span>
            <span class="message-title">${title}</span>
        </div>
        <div class="message-content">
            ${content}
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Generate automatic analysis using phi3 (deep analysis model)
async function generateAutoAnalysis(algorithmType, results) {
    updateAnalystStatus('thinking', 'Analyzing results...');
    
    try {
        // Build analysis prompt
        const prompt = `Analyze these ${algorithmType} results and provide deep insights:

Results: ${JSON.stringify(results, null, 2)}

Provide:
1. Key findings and patterns
2. Performance assessment
3. Potential issues or concerns
4. Specific recommendations for improvement
5. Next steps

Be technical but clear. Focus on actionable insights.`;
        
        // Use phi3 for deep analysis (separate model from quick chat)
        const config = AI_CONFIG[AI_CONFIG.provider];
        const response = await fetch(config.apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: config.metacognitionModel || 'phi3',
                messages: [
                    { role: 'system', content: 'You are an expert ML analyst. Provide deep, technical analysis of ML results.' },
                    { role: 'user', content: prompt }
                ],
                stream: false
            })
        });
        
        if (!response.ok) {
            throw new Error('Analysis failed');
        }
        
        const data = await response.json();
        const analysis = data.message.content;
        
        // Format analysis into HTML
        const formattedAnalysis = analysis
            .split('\n\n')
            .map(para => `<p>${para}</p>`)
            .join('');
        
        addAnalystMessage(
            `${algorithmType} Analysis`,
            formattedAnalysis,
            '📊'
        );
        
        updateAnalystStatus('idle', 'Ready for next analysis');
        addLog(`🧠 AI Analyst completed analysis of ${algorithmType}`, 'info');
        
    } catch (error) {
        console.error('Auto-analysis error:', error);
        updateAnalystStatus('idle', 'Analysis failed');
        addAnalystMessage(
            'Analysis Error',
            `<p>Could not complete analysis: ${error.message}</p><p class="message-hint">The AI model may still be loading. Try again in a moment.</p>`,
            '⚠️'
        );
    }
}

// Trigger automatic analysis when ML results are available
function triggerAutoAnalysis(algorithmType, results) {
    if (AI_CONFIG.metacognition.enabled) {
        addAnalystMessage(
            'New Analysis Detected',
            `<p>Detected new <strong>${algorithmType}</strong> results.</p><p class="message-hint">Generating deep analysis...</p>`,
            '💻'
        );
        
        // Small delay to let user see the detection message
        setTimeout(() => {
            generateAutoAnalysis(algorithmType, results);
        }, 500);
    }
}

// ============================================================================
// 🎨 THEME TOGGLE - Dark/Light Mode
// ============================================================================

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update theme icon
    const themeIcon = document.querySelector('.theme-icon');
    if (themeIcon) {
        themeIcon.textContent = newTheme === 'light' ? '☀️' : '🌙';
    }
    
    addLog(`🎨 Theme switched to ${newTheme} mode`, 'info');
}

function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    const themeIcon = document.querySelector('.theme-icon');
    if (themeIcon) {
        themeIcon.textContent = savedTheme === 'light' ? '☀️' : '🌙';
    }
}

// ============================================================================
// 📊 DEMO DATA LOADER - Professional First Impression
// ============================================================================

function loadDemoData() {
    if (typeof DEMO_DATA === 'undefined') {
        console.warn('Demo data not loaded');
        return;
    }
    
    // Load demo KPIs
    updateKPIsWithData(DEMO_DATA.systemKPIs);
    
    // Show sample timeline events
    loadDemoTimeline();
    
    addLog('📊 Demo data loaded - showing sample results', 'info');
}

function loadDemoTimeline() {
    if (typeof DEMO_DATA === 'undefined' || !DEMO_DATA.timelineEvents) return;
    
    DEMO_DATA.timelineEvents.forEach(event => {
        addLog(
            `${event.icon} ${event.model}: ${event.message} (${event.duration})`,
            event.type
        );
    });
}

// ============================================================================
// 📈 KPI UPDATER - Real-time System Stats
// ============================================================================

function updateKPIs() {
    // Calculate real stats from state
    const totalRuns = Object.keys(state.mlContext).length;
    const activeModels = Object.keys(state.mlContext).length;
    
    // Calculate average accuracy from available results
    let totalAccuracy = 0;
    let accuracyCount = 0;
    
    if (state.mlContext.linearRegression?.metrics?.r2_score) {
        totalAccuracy += state.mlContext.linearRegression.metrics.r2_score * 100;
        accuracyCount++;
    }
    if (state.mlContext.knn?.metrics?.accuracy) {
        totalAccuracy += state.mlContext.knn.metrics.accuracy * 100;
        accuracyCount++;
    }
    
    const avgAccuracy = accuracyCount > 0 ? (totalAccuracy / accuracyCount).toFixed(1) + '%' : '--';
    
    // Update KPI display
    const kpis = {
        uptime: '99.2%',  // Static for demo (could be calculated from server start time)
        totalRuns: totalRuns > 0 ? totalRuns : (DEMO_DATA?.systemKPIs?.totalRuns || '--'),
        avgAccuracy: avgAccuracy !== '--' ? avgAccuracy : (DEMO_DATA?.systemKPIs?.avgAccuracy || '--'),
        activeModels: activeModels > 0 ? activeModels : 4
    };
    
    updateKPIsWithData(kpis);
}

function updateKPIsWithData(kpis) {
    document.getElementById('kpiUptime').textContent = kpis.uptime || '--';
    document.getElementById('kpiTotalRuns').textContent = kpis.totalRuns || '--';
    document.getElementById('kpiAvgAccuracy').textContent = kpis.avgAccuracy || '--';
    document.getElementById('kpiActiveModels').textContent = kpis.activeModels || '--';
}

console.log('✅ TransparentML Dashboard fully loaded with AI integration!');
