# 🧮 Algorithms Directory

## 📊 Purpose

This directory contains all machine learning algorithm implementations built from scratch using only NumPy. Each algorithm is designed as an independent microservice with its own API, tests, and documentation.

---

## 🏗️ Architecture Diagram

```
algorithms/
│
├── linear-regression/          🔹 Multivariate Linear Regression
│   ├── src/                    → Core implementation (NumPy only)
│   ├── scripts/                → Training & prediction scripts
│   ├── notebooks/              → Jupyter analysis
│   ├── data/                   → KDD Cup 1999 dataset
│   ├── models/                 → Trained model artifacts
│   ├── results/                → Visualizations & metrics
│   ├── tests/                  → Unit & integration tests
│   └── docker-compose.yml      → Service orchestration
│
├── pca-analysis/               🔹 Principal Component Analysis
│   ├── src/                    → PCA implementation from scratch
│   ├── notebooks/              → Interactive demos
│   ├── data/                   → Iris dataset
│   ├── results/                → 2D/3D visualizations
│   └── docker-compose.yml      → Service orchestration
│
└── url-diagnostics/            🔹 URL Health Analysis (NEW)
    ├── src/                    → Scraper + ML analyzer
    ├── static/                 → Web dashboard
    ├── tests/                  → Test suite
    └── docker-compose.yml      → Service orchestration
```

---

## 🔄 Data Flow

```
┌─────────────────────────────────────────────────────┐
│              Input Data Layer                        │
├─────────────────────────────────────────────────────┤
│  • datasets/ (CSV, JSON)                             │
│  • API requests (REST)                               │
│  • Jupyter notebooks                                 │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│           Algorithm Services                         │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │   Linear     │  │     PCA      │  │    URL    │ │
│  │  Regression  │  │   Analysis   │  │Diagnostics│ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│         │                  │                │        │
│         ▼                  ▼                ▼        │
│  ┌──────────────────────────────────────────────┐  │
│  │      NumPy Core Implementations              │  │
│  │  • Manual gradient descent                   │  │
│  │  • Covariance matrices                       │  │
│  │  • Feature engineering                       │  │
│  └──────────────────────────────────────────────┘  │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              Output Layer                            │
├─────────────────────────────────────────────────────┤
│  • REST API responses (JSON)                         │
│  • Visualizations (PNG, HTML)                        │
│  • Metrics & reports                                 │
│  • Model artifacts                                   │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Algorithm Structure (Standard)

Each algorithm follows this structure:

```
algorithm-name/
├── README.md                   # Algorithm documentation
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Service orchestration
├── Makefile                    # Build & run commands
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── model.py                # Core algorithm
│   ├── data_loader.py          # Data handling
│   ├── preprocessing.py        # Data preparation
│   ├── evaluation.py           # Metrics calculation
│   └── api.py                  # REST API (FastAPI)
│
├── scripts/                    # Executable scripts
│   ├── train.py                # Training script
│   ├── predict.py              # Prediction script
│   └── evaluate.py             # Evaluation script
│
├── notebooks/                  # Jupyter notebooks
│   ├── exploration.ipynb       # Data exploration
│   └── analysis.ipynb          # Results analysis
│
├── data/                       # Datasets
│   ├── raw/                    # Original data
│   └── processed/              # Preprocessed data
│
├── models/                     # Trained models
│   └── .gitkeep
│
├── results/                    # Outputs
│   ├── visualizations/         # Charts & plots
│   └── metrics/                # Performance metrics
│
└── tests/                      # Test suite
    ├── test_model.py
    ├── test_api.py
    └── test_integration.py
```

---

## 🚀 Quick Start

### Run Specific Algorithm

```bash
# Linear Regression
make up-linear-regression
make test-linear-regression
make logs-linear-regression

# PCA Analysis
make up-pca
make test-pca
make logs-pca

# URL Diagnostics
make up-url-diagnostics
make logs-url-diagnostics
```

### Run All Algorithms

```bash
make start-complete
```

---

## 🔗 Service Ports

| Algorithm | Port | API Docs | Purpose |
|-----------|------|----------|---------|
| **Linear Regression** | 8001 | `/docs` | Multivariate regression |
| **PCA Analysis** | 8002 | `/docs` | Dimensionality reduction |
| **URL Diagnostics** | 8003 | `/docs` | Website health analysis |
| **API Gateway** | 80 | - | Unified entry point |
| **Jupyter Lab** | 8888 | - | Interactive development |

---

## 🧪 Testing

Each algorithm includes comprehensive tests:

```bash
# Unit tests
make test-unit

# Integration tests
make test-integration

# All tests
make test-all

# Coverage report
make coverage-all
```

---

## 📊 Performance Benchmarks

All algorithms are benchmarked against scikit-learn:

```bash
make benchmark-all
make benchmark-vs-sklearn
```

Expected results:
- **Accuracy**: Within 0.01% of sklearn
- **Speed**: 2-3x slower (acceptable for transparency)
- **Memory**: Similar or better

---

## 🔍 Algorithm Status

| Algorithm | Status | Version | Lines of Code | Tests |
|-----------|--------|---------|---------------|-------|
| Linear Regression | ✅ Production | 1.0.0 | ~500 | 15 |
| PCA Analysis | ✅ Production | 1.0.0 | ~400 | 12 |
| URL Diagnostics | ✅ Production | 1.0.0 | ~800 | 8 |

---

## 📝 Adding New Algorithms

To add a new algorithm:

1. Create directory structure
2. Implement core algorithm in `src/model.py`
3. Add REST API in `src/api.py`
4. Write tests in `tests/`
5. Create Docker configuration
6. Add Makefile commands
7. Update main README

See `docs/ADDING_ALGORITHMS.md` for detailed guide.

---

## 🎓 Educational Value

Each implementation is designed for:
- **Learning**: Clear code with extensive comments
- **Teaching**: Step-by-step notebooks
- **Research**: Modifiable and extensible
- **Production**: Performance-optimized

---

## 📚 Documentation

- Algorithm theory: `docs/theory/`
- Implementation details: `docs/implementation/`
- API reference: `docs/api/`
- Tutorials: `examples/`

---

## 🤝 Contributing

When adding algorithms:
1. Follow existing structure
2. Include comprehensive tests
3. Add docstrings (NumPy style)
4. Benchmark against sklearn
5. Update this README

---

## 📞 Support

- Issues: GitHub Issues
- Documentation: `/docs`
- Examples: `/examples`

**Built with ❤️ for transparency in AI**
