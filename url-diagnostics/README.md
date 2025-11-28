# 🔍 TransparentML URL Diagnostics

> **ML-Powered Website Health Analysis**

Professional URL health diagnostics service using Linear Regression and PCA for comprehensive website analysis.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Web Interface](#web-interface)
- [How It Works](#how-it-works)
- [Use Cases](#use-cases)

---

## 🎯 Overview

The URL Diagnostics service analyzes websites and provides:
- **Health Score** (0-100) using Machine Learning
- **Performance Metrics** (load time, page size, compression)
- **Security Analysis** (SSL, headers, vulnerabilities)
- **SEO Evaluation** (meta tags, mobile-friendliness)
- **Anomaly Detection** using PCA
- **Actionable Recommendations** prioritized by impact

```
┌─────────────────────────────────────────────────────────┐
│  📊 URL Diagnostics Service Architecture                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  🌐 Web Interface → FastAPI → URL Scraper → ML Analyzer │
│       (Port 8003)    (REST)    (Metrics)     (Scoring)  │
│                                                          │
│  Features: Real-time logs • Charts • Recommendations    │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 🔬 **Analysis Capabilities**

| Feature | Description |
|---------|-------------|
| **HTTP Metrics** | Status codes, load time, redirects, caching |
| **SSL/TLS Analysis** | Certificate validation, expiration, cipher strength |
| **Content Analysis** | HTML structure, meta tags, image/script counts |
| **DNS Metrics** | Resolution time, IP address |
| **Security Headers** | CSP, HSTS, X-Frame-Options |
| **Mobile Optimization** | Viewport meta, responsive design detection |
| **SEO Elements** | Meta description, structured data, Open Graph |

### 🤖 **ML-Powered Insights**

- **Linear Regression**: Predicts health score based on 41 extracted features
- **PCA**: Detects anomalies and unusual patterns
- **Feature Importance**: Identifies which metrics impact score most
- **Transparent**: Every calculation is explainable and auditable

### 🎨 **Professional Web Interface**

- Real-time analysis progress
- Live log streaming (Server-Sent Events)
- Interactive charts (Chart.js)
- Responsive design
- Dark theme optimized for developers

---

## 🏗️ Architecture

```
url-diagnostics/
├── src/
│   ├── url_scraper.py      # URL metrics extraction
│   ├── ml_analyzer.py      # ML-based health scoring
│   └── api.py              # FastAPI application
├── static/
│   ├── index.html          # Web interface
│   ├── css/styles.css      # Professional styling
│   └── js/app.js           # Frontend logic
├── Dockerfile              # Container definition
├── docker-compose.yml      # Service orchestration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Data Flow

```
User Input (URL)
    ↓
URL Scraper
    ├─→ HTTP Request
    ├─→ SSL Analysis
    ├─→ Content Parsing
    └─→ DNS Lookup
    ↓
Feature Extraction (41 features)
    ↓
ML Analyzer
    ├─→ Linear Regression (Health Score)
    ├─→ PCA (Anomaly Detection)
    └─→ Rule-Based (Recommendations)
    ↓
Results Display
    ├─→ Score & Grade
    ├─→ Charts
    ├─→ Recommendations
    └─→ Raw Data
```

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Port 8003 available

### 1. Build & Run

```bash
# From project root
make up-url-diagnostics

# Or from url-diagnostics directory
docker-compose up -d
```

### 2. Access the Interface

Open your browser:
```
http://localhost:8003/static/index.html
```

### 3. Analyze a URL

1. Enter a URL (e.g., `https://www.google.com`)
2. Select analysis type (Comprehensive/Quick/Security)
3. Click "Analyze URL"
4. Watch real-time logs
5. View results with interactive charts

---

## 📚 API Documentation

### Base URL
```
http://localhost:8003
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "url-diagnostics",
  "timestamp": "2025-11-28T21:00:00",
  "version": "1.0.0"
}
```

#### 2. Start Analysis (Async)
```http
POST /api/v1/analyze
Content-Type: application/json

{
  "url": "https://example.com",
  "analysis_type": "comprehensive"
}
```

**Response:**
```json
{
  "analysis_id": "abc123-def456-...",
  "status": "started",
  "message": "Analysis started...",
  "url": "https://example.com"
}
```

#### 3. Get Analysis Status
```http
GET /api/v1/status/{analysis_id}
```

**Response:**
```json
{
  "status": "completed",
  "progress": 100,
  "url": "https://example.com",
  "started_at": "2025-11-28T21:00:00"
}
```

#### 4. Get Results
```http
GET /api/v1/results/{analysis_id}
```

**Response:**
```json
{
  "url": "https://example.com",
  "health_score": 85.5,
  "grade": "A",
  "metrics": {
    "load_time": 1.2,
    "response_size_kb": 350,
    "ssl_enabled": true,
    "mobile_friendly": true
  },
  "anomalies": ["✅ No anomalies detected"],
  "recommendations": [
    {
      "category": "Performance",
      "priority": "medium",
      "issue": "Page size could be optimized",
      "current": "350KB",
      "target": "< 500KB",
      "action": "Compress images"
    }
  ]
}
```

#### 5. Stream Logs (SSE)
```http
GET /api/v1/logs/{analysis_id}
```

**Response:** Server-Sent Events stream
```
data: {"log": "[21:00:00] 🚀 Starting analysis...", "index": 0}

data: {"log": "[21:00:01] ✓ URL fetched successfully", "index": 1}

data: {"status": "completed", "done": true}
```

#### 6. Synchronous Analysis
```http
POST /api/v1/analyze/sync
Content-Type: application/json

{
  "url": "https://example.com",
  "analysis_type": "comprehensive"
}
```

Returns complete results immediately (may timeout for slow URLs).

---

## 🎨 Web Interface

### Features

#### 1. **Input Form**
- URL input with validation
- Analysis type selection (Comprehensive/Quick/Security)
- One-click analysis

#### 2. **Progress Tracking**
- Visual progress bar (0-100%)
- Real-time status updates

#### 3. **Live Logs**
- Terminal-style log display
- Auto-scrolling
- Timestamped entries

#### 4. **Results Dashboard**

**Health Score Card**
- Large circular progress indicator
- Letter grade (A+ to F)
- Color-coded by performance
- Interpretation message

**Metrics Grid**
- Load Time
- Page Size
- SSL Status
- Mobile Friendliness

**Interactive Charts**
- Bar chart: Feature analysis
- Radar chart: Category scores

**Anomalies Section**
- Detected issues
- Visual indicators

**Recommendations Panel**
- Priority-based sorting (Critical/High/Medium/Low)
- Current vs Target values
- Actionable suggestions

**Raw Data Viewer**
- Collapsible JSON display
- Complete analysis output

---

## 🧠 How It Works

### 1. URL Scraping

The service extracts **30+ metrics**:

```python
# Performance
- Load time (seconds)
- Response size (KB)
- Compression enabled
- Cache headers present

# Security
- SSL/TLS enabled
- Certificate expiration
- Security headers (CSP, HSTS, X-Frame-Options)

# SEO
- Meta description
- Viewport meta tag
- Title tag
- Structured data (Schema.org, Open Graph)

# Content
- Images count
- Scripts count
- External resources
- HTML-to-text ratio
```

### 2. Feature Engineering

Converts raw metrics to **41 numerical features**:

```python
features = [
    status_code,           # 200, 404, etc.
    load_time_seconds,     # 0.5, 2.3, etc.
    response_size_kb,      # 350, 1200, etc.
    ssl_enabled,           # 0 or 1
    mobile_friendly,       # 0 or 1
    ... # 36 more features
]
```

### 3. ML Analysis

**Linear Regression Model:**
```python
health_score = Σ(weight[i] * feature[i]) for i in 0..40
normalized_score = normalize(health_score, 0, 100)
```

**PCA Anomaly Detection:**
```python
projected = features × PCA_components
reconstructed = projected × PCA_components.T
error = mean((features - reconstructed)²)
if error > threshold: flag_anomaly()
```

### 4. Recommendations Engine

Rule-based system generates actionable advice:

```python
if load_time > 3.0:
    recommend("Optimize images, minify CSS/JS", priority="high")

if ssl_enabled == False:
    recommend("Install SSL certificate", priority="critical")

if mobile_friendly == False:
    recommend("Add viewport meta tag", priority="high")
```

---

## 💼 Use Cases

### 1. **Digital Marketing Agency**
- Audit client websites before proposals
- Generate professional reports
- Identify improvement opportunities
- Track optimization progress

### 2. **Web Development Team**
- Pre-deployment health checks
- Performance monitoring
- Security audits
- SEO optimization tracking

### 3. **Freelance Consultants**
- Quick site assessments
- Data-driven recommendations
- Client presentations
- Competitive analysis

### 4. **DevOps/SRE Teams**
- Continuous monitoring
- Anomaly detection
- Performance baselines
- Incident investigation

---

## 🔧 Configuration

### Environment Variables

```bash
# Application
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1

# Ports
PORT=8003

# Timeouts
REQUEST_TIMEOUT=10
ANALYSIS_TIMEOUT=60
```

### Customization

**Adjust ML Weights:**
Edit `src/ml_analyzer.py`:
```python
def _initialize_lr_weights(self):
    weights = np.array([
        0.5,   # status_code weight
        -2.0,  # load_time weight (negative = lower is better)
        ...
    ])
```

**Add Custom Metrics:**
Edit `src/url_scraper.py`:
```python
def _get_custom_metrics(self, url: str) -> Dict:
    # Your custom analysis
    return {
        'custom_metric': value
    }
```

---

## 📊 Example Output

```json
{
  "url": "https://www.google.com",
  "health_score": 92.5,
  "grade": "A+",
  "metrics": {
    "load_time": 0.8,
    "response_size_kb": 125,
    "status_code": 200,
    "ssl_enabled": true,
    "mobile_friendly": true
  },
  "anomalies": [
    "✅ No anomalies detected"
  ],
  "recommendations": [
    {
      "category": "SEO",
      "priority": "low",
      "issue": "No structured data",
      "action": "Add Schema.org markup"
    }
  ]
}
```

---

## 🛠️ Development

### Running Locally (without Docker)

```bash
cd url-diagnostics

# Install dependencies
pip install -r requirements.txt

# Run the API
cd src
uvicorn api:app --reload --port 8003

# Access at http://localhost:8003/static/index.html
```

### Testing

```bash
# Test URL scraper
python src/url_scraper.py

# Test ML analyzer
python src/ml_analyzer.py

# Test API endpoint
curl -X POST http://localhost:8003/api/v1/analyze/sync \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

---

## 📝 License

Part of the TransparentML project - MIT License

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Add more ML models (Random Forest, Neural Networks)
- [ ] Implement caching (Redis)
- [ ] Add user authentication
- [ ] Export reports to PDF
- [ ] Historical tracking & trends
- [ ] Webhook notifications
- [ ] Rate limiting
- [ ] API key management

---

## 📞 Support

- **Documentation**: `/docs` endpoint
- **Issues**: GitHub Issues
- **API Docs**: http://localhost:8003/docs (Swagger UI)

---

**Built with ❤️ by the TransparentML Team**

*ML-powered insights you can understand and trust.*
