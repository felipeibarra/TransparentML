# 🔬 TransparentML v1.1 - Enterprise ML Platform

> **Machine Learning with Nothing to Hide** • Built from scratch with NumPy • Production-Ready Microservices

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)](https://docker.com)
[![NumPy](https://img.shields.io/badge/NumPy-Core-013243?style=for-the-badge&logo=numpy)](https://numpy.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

---

## 🎯 What is TransparentML?

TransparentML is an **enterprise-grade machine learning platform** where every algorithm is implemented **from scratch using only NumPy**. Perfect for:

- 🏢 **Organizations** that need explainable AI and auditable models
- 🎓 **Educational institutions** teaching ML fundamentals  
- 👨‍💻 **Developers** who want complete control over their ML stack
- 🔍 **Researchers** requiring transparency and reproducibility

### Core Principles

✨ **Zero Black Boxes** - Every line of code is visible and auditable  
🎯 **NumPy Only** - Core algorithms use pure NumPy (no sklearn for ML logic)  
🐳 **Microservices** - Each algorithm runs as an independent REST API service  
🌐 **Centralized Dashboard** - Web interface with real-time visualizations + AI assistant  
📊 **Production-Ready** - Docker orchestration, health checks, and monitoring

---

## 🚀 Quick Start

### One-Command Deployment

```bash
# Clone the repository
git clone https://github.com/yourusername/TransparentML.git
cd TransparentML

# Start ALL ML services (4 services on ports 8001-8004)
make start-all-ml
```

### Access the Platform

| Service | URL | Description |
|---------|-----|-------------|
| **🌐 Central Dashboard** | http://localhost:8003/static/dashboard.html | Main UI + AI Chatbot |
| 📈 Linear Regression | http://localhost:8001/docs | FastAPI docs |
| 🌈 PCA Analysis | http://localhost:8002/docs | FastAPI docs |
| 🔍 URL Diagnostics | http://localhost:8003/docs | FastAPI docs |
| 🎯 KNN Classifier | http://localhost:8004/docs | FastAPI docs |

---

## 🧠 ML Algorithms

### 1. Linear Regression (Port 8001)

**Pure NumPy implementation with gradient descent**

```python
# API Example
POST http://localhost:8001/api/v1/demo/analyze
{
  "n_samples": 100,
  "noise": 10.0
}
```

**Features:**
- ✅ Train, Predict, Score
- ✅ Multiple regression types (Linear, Ridge, Polynomial)
- ✅ R², RMSE, MAE metrics
- ✅ Model coefficients extraction

**Location:** `algorithms/linear-regression/`

---

### 2. PCA Analysis (Port 8002)

**Principal Component Analysis from scratch**

```python
# API Example
GET http://localhost:8002/analysis
```

**Features:**
- ✅ Manual eigenvalue decomposition
- ✅ Variance explained calculation
- ✅ Component loadings and biplots
- ✅ Iris dataset demo (4D → 2D)

**Location:** `algorithms/pca-analysis/`

---

### 3. URL Health Diagnostics (Port 8003)

**ML-powered website analysis combining Linear Regression + PCA**

```python
# API Example
POST http://localhost:8003/api/v1/analyze/sync
{
  "url": "https://example.com",
  "analysis_type": "comprehensive"
}
```

**Features:**
- ✅ 41+ URL metrics extraction
- ✅ Health score (0-100) + letter grade (A-F)
- ✅ Anomaly detection with PCA
- ✅ Prioritized recommendations

**Location:** `url-diagnostics/`

---

### 4. K-Nearest Neighbors (Port 8004)

**Classification and regression with distance metrics**

```python
# API Example
POST http://localhost:8004/api/v1/demo/analyze
{
  "dataset": "iris",
  "n_neighbors": 5,
  "test_size": 0.3
}
```

**Features:**
- ✅ KNNClassifier and KNNRegressor
- ✅ 3 distance metrics (Euclidean, Manhattan, Minkowski)
- ✅ Uniform and distance-weighted predictions
- ✅ Probability estimates

**Location:** `algorithms/knn/`

---

## 🌐 Centralized Dashboard

### Real-Time Web Interface

Access at: **http://localhost:8003/static/dashboard.html**

![Dashboard Features](https://via.placeholder.com/800x400?text=Dashboard+Screenshot)

**Features:**

| Panel | Description |
|-------|-------------|
| 🎛️ **Configuration** | Select models, input parameters, run analyses |
| 📊 **Statistics** | Real-time metrics: scores, accuracy, processing time |
| 📉 **Visualizations** | Interactive charts (Bar, Line, Radar, Scatter) |
| 📋 **Live Logs** | Server-Sent Events streaming with filters |
| 📈 **Log Analytics** | Timeline, error rates, event statistics |
| 🎯 **Results** | Formatted results with health scores and grades |
| 💡 **Recommendations** | Prioritized improvement suggestions |
| 🤖 **AI Assistant** | Context-aware chatbot powered by Groq (FREE) |

### 🤖 AI Chatbot Integration

The dashboard includes an **AI-powered assistant** that interprets ML results:

**How it works:**
1. Run any ML analysis (Linear Reg, PCA, URL Diag, or KNN)
2. Chatbot automatically gets enabled with context
3. Ask questions like:
   - *"Explain my R² score"*
   - *"What does 72% variance mean?"*
   - *"Why is my URL health score low?"*
   - *"What's the difference between my training and test accuracy?"*

**Powered by:** Groq API (free tier) with Llama 3 or Mixtral models

**Setup:**
```javascript
// Edit: url-diagnostics/static/js/dashboard-integrated.js
const GROQ_CONFIG = {
    apiKey: 'YOUR_FREE_API_KEY', // Get at https://console.groq.com
    model: 'llama3-8b-8192'
};
```

---

## 🏗️ Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│              🌐 CENTRALIZED DASHBOARD                   │
│   • Model Selection  • Charts  • Logs  • AI Chatbot    │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP/REST APIs
                 ▼
┌────────────────────────────────────────────────────────┐
│                  ML SERVICES LAYER                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ Linear   │ │   PCA    │ │   URL    │ │   KNN    │ │
│  │ Reg 8001 │ │   8002   │ │ Diag 8003│ │   8004   │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└────────────────────────────────────────────────────────┘
                 │ NumPy Operations
                 ▼
┌────────────────────────────────────────────────────────┐
│              🔬 NUMPY ML ENGINE                         │
│  • Matrix Ops  • Linear Algebra  • Statistics          │
└────────────────────────────────────────────────────────┘
```

### Microservices Architecture

Each ML algorithm runs in its own **Docker container** with:

- ✅ Independent scaling
- ✅ Health checks
- ✅ REST API (FastAPI + Uvicorn)
- ✅ Isolated dependencies
- ✅ Bridge network communication

**Network:** `transparentml-network` (172.20.0.0/16)

---

## 📦 Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Backend** | Python 3.11+, NumPy, FastAPI, Uvicorn, Pandas |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript, Chart.js |
| **Infrastructure** | Docker, Docker Compose, Custom Networks |
| **AI** | Groq API (free), Llama 3 / Mixtral models |
| **Orchestration** | GNU Make (40+ commands) |

---

## 🛠️ Development Commands

### Service Management

```bash
# Start ALL services (recommended)
make start-all-ml

# Health check all services
make health-all-ml

# View logs from all services
make logs-all-ml

# Stop all services
make stop-all-ml

# Restart all services
make restart-all-ml
```

### Individual Services

```bash
# Start specific service
make up-linear-regression
make up-pca
make up-url-diagnostics

# View service logs
make logs-linear-regression
make logs-pca
```

### Testing & Quality

```bash
# Run all tests
make test-all

# Linting
make lint-all

# Type checking
make type-check-all

# Coverage report
make coverage-all
```

---

## 📁 Project Structure

```
TransparentML/
├── algorithms/
│   ├── linear-regression/
│   │   ├── src/
│   │   │   ├── api.py              ← FastAPI service
│   │   │   ├── models.py           ← ML implementations
│   │   │   └── ...
│   │   ├── Dockerfile.api
│   │   └── requirements.txt
│   │
│   ├── pca-analysis/
│   │   ├── src/
│   │   │   ├── api.py
│   │   │   ├── pca_manual.py       ← NumPy PCA
│   │   │   └── ...
│   │   └── Dockerfile
│   │
│   └── knn/
│       ├── src/
│       │   ├── api.py
│       │   ├── knn_model.py        ← NumPy KNN
│       │   └── ...
│       └── docker-compose.yml
│
├── url-diagnostics/
│   ├── src/
│   │   ├── api.py
│   │   ├── url_scraper.py
│   │   └── ml_analyzer.py
│   ├── static/
│   │   ├── dashboard.html          ← MAIN DASHBOARD
│   │   ├── css/dashboard.css
│   │   └── js/dashboard-integrated.js  ← Full integration + AI
│   └── Dockerfile
│
├── docker-compose.all.yml          ← Orchestrates all services
├── Makefile                        ← 40+ automation commands
├── ARCHITECTURE.txt                ← Complete architecture docs
├── README.md                       ← This file
└── ROADMAP-IMPLEMENTATION.md       ← Development roadmap
```

---

## 🔌 API Reference

### Linear Regression (8001)

```bash
# Train model
POST /api/v1/train
{
  "X": [[1.0, 2.0], [2.0, 3.0]],
  "y": [3.0, 5.0],
  "model_type": "linear"
}

# Make predictions
POST /api/v1/predict
{
  "X": [[1.5, 2.5]]
}

# Run demo analysis
POST /api/v1/demo/analyze
{
  "n_samples": 100,
  "noise": 10.0
}
```

### PCA (8002)

```bash
# Get full analysis (Iris dataset)
GET /analysis

# Refresh analysis
POST /refresh
```

### URL Diagnostics (8003)

```bash
# Analyze URL (synchronous)
POST /api/v1/analyze/sync
{
  "url": "https://example.com",
  "analysis_type": "comprehensive"
}

# Analyze URL (async with streaming logs)
POST /api/v1/analyze
GET  /api/v1/status/{analysis_id}
GET  /api/v1/logs/{analysis_id}     # Server-Sent Events
GET  /api/v1/results/{analysis_id}
```

### KNN (8004)

```bash
# Train KNN model
POST /api/v1/train
{
  "X": [[1.0, 2.0], [2.0, 3.0], [3.0, 3.5]],
  "y": [0, 0, 1],
  "n_neighbors": 3,
  "task": "classification"
}

# Make predictions
POST /api/v1/predict
{
  "X": [[1.5, 2.5]],
  "task": "classification"
}

# Run demo (Iris dataset)
POST /api/v1/demo/analyze
{
  "dataset": "iris",
  "n_neighbors": 5,
  "test_size": 0.3
}
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **ARCHITECTURE.txt** | Complete system architecture with ASCII diagrams |
| **ROADMAP-IMPLEMENTATION.md** | Development roadmap (v1.0 → v2.5) |
| **IMPLEMENTATION-STATUS.md** | Current progress and next steps |
| **QUICKSTART.md** | Detailed setup and usage guide |
| **algorithms/README.md** | Algorithm-specific documentation |

---

## 🎯 Roadmap

### ✅ v1.0 - Enterprise Core (COMPLETE)
- 3 ML algorithms (Linear Reg, PCA, URL Diagnostics)
- Microservices architecture
- Basic dashboard

### ✅ v1.1 - Enterprise Basic (CURRENT - 100%)
- ✅ 4 ML algorithms (+ KNN)
- ✅ Centralized dashboard with real-time logs
- ✅ AI chatbot integration (Groq API)
- ✅ Full REST APIs for all services
- ✅ Docker orchestration
- ✅ Comprehensive documentation

### 📋 v1.2 - Upcoming
- 5+ new algorithms (SVM, Decision Trees, K-Means, Logistic Reg)
- XAI suite (SHAP, LIME, Permutation Importance)
- Benchmarking vs scikit-learn
- >80% test coverage
- CI/CD pipeline (GitHub Actions)

### 🚀 v2.0 - Future
- One-click deployment
- Mobile responsive dashboard
- 100+ beta testers
- Public demos

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Guidelines:**
- Follow existing code style
- Add tests for new features
- Update documentation
- Use NumPy for core ML implementations (no sklearn)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **NumPy** - The foundation of all our ML implementations
- **FastAPI** - Modern, fast web framework
- **Docker** - Containerization and orchestration
- **Groq** - Free AI inference for chatbot
- **Chart.js** - Beautiful data visualizations

---

## 📞 Contact & Support

- 📧 Email: support@transparentml.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/TransparentML/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/TransparentML/discussions)
- 📖 Docs: [Full Documentation](https://transparentml.readthedocs.io)

---

<div align="center">

### ⭐ If you find TransparentML useful, please star the repository! ⭐

**Built with ❤️ by the TransparentML Team**

</div>
