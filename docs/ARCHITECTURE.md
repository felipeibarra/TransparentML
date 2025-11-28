# 🏗️ Architecture Overview

## System Architecture

TransparentML is built with a microservices architecture, where each algorithm is an independent service with its own API.

```
┌─────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                           │
│  (Browser, curl, Python clients, Mobile apps, etc.)             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (Nginx)                        │
│                        Port: 80/443                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Routing:                                                 │  │
│  │  /api/v1/linear-regression/* → linear-regression-api     │  │
│  │  /api/v1/pca/*              → pca-api                    │  │
│  │  Load Balancing | SSL Termination | Rate Limiting        │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────┬──────────────────────┬──────────────────────────────────┘
        │                      │
        ▼                      ▼
┌──────────────────┐   ┌──────────────────┐
│ Linear Regression│   │   PCA Analysis   │
│     Service      │   │     Service      │
│   Port: 8001     │   │   Port: 8002     │
├──────────────────┤   ├──────────────────┤
│ FastAPI/Flask    │   │ FastAPI/Flask    │
│ NumPy Core       │   │ NumPy Core       │
│ Model Storage    │   │ Model Storage    │
└──────┬───────────┘   └──────┬───────────┘
       │                      │
       └──────────┬───────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SHARED COMPONENTS LAYER                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐    │
│  │   Logging   │  │ Validation  │  │  Metrics & Monitoring│    │
│  └─────────────┘  └─────────────┘  └─────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   DEVELOPMENT & ANALYSIS LAYER                  │
│  ┌──────────────────┐           ┌──────────────────────┐       │
│  │  Jupyter Lab     │           │  Documentation Server│       │
│  │  Port: 8888      │           │  Port: 8080          │       │
│  └──────────────────┘           └──────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        STORAGE LAYER                            │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐      │
│  │  Raw Data   │  │    Models    │  │     Results      │      │
│  │  (Volumes)  │  │   (Volumes)  │  │    (Volumes)     │      │
│  └─────────────┘  └──────────────┘  └──────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. API Gateway (Nginx)

**Purpose**: Single entry point for all services

**Features**:
- Reverse proxy to backend services
- Load balancing (future: multiple instances)
- SSL/TLS termination
- Rate limiting
- Request logging
- Health check endpoint

**Configuration**: `shared/api-gateway/nginx.conf`

**Ports**: 80 (HTTP), 443 (HTTPS)

---

### 2. Linear Regression Service

**Purpose**: Multivariate linear regression predictions

**Components**:
```
linear-regression/
├── src/
│   ├── model.py           # Core algorithm implementation
│   ├── training.py        # Training logic
│   └── preprocessing.py   # Data preprocessing
├── api/
│   ├── main.py           # FastAPI application
│   ├── routes.py         # API endpoints
│   └── schemas.py        # Request/response models
├── models/               # Trained models
├── data/                 # Dataset
└── tests/               # Unit & integration tests
```

**API Endpoints**:
- `POST /train` - Train new model
- `POST /predict` - Make predictions
- `GET /metrics` - Get model metrics
- `GET /health` - Health check

**Technologies**:
- Python 3.11
- NumPy (no scikit-learn)
- FastAPI
- Uvicorn

---

### 3. PCA Analysis Service

**Purpose**: Principal Component Analysis and dimensionality reduction

**Components**:
```
pca-analysis/
├── src/
│   ├── pca_manual.py     # Manual PCA implementation
│   ├── data_loader.py    # Data loading
│   └── visualization.py  # Plotting functions
├── api/
│   ├── main.py          # FastAPI application
│   └── routes.py        # API endpoints
├── models/              # PCA models
├── data/                # Iris dataset
└── tests/              # Tests
```

**API Endpoints**:
- `POST /fit` - Fit PCA
- `POST /transform` - Transform data
- `GET /explained-variance` - Get variance explained
- `GET /health` - Health check

**Technologies**:
- Python 3.11
- NumPy (manual covariance calculation)
- FastAPI
- Matplotlib/Seaborn

---

### 4. Shared Components

**Location**: `shared/common-utils/`

**Modules**:

#### Logging (`logger.py`)
```python
from shared.logger import get_logger

logger = get_logger(__name__)
logger.info("Processing request")
```

#### Validation (`validators.py`)
```python
from shared.validators import validate_features

validate_features(data, min_features=4)
```

#### Metrics (`metrics.py`)
```python
from shared.metrics import calculate_mse, calculate_r2

mse = calculate_mse(y_true, y_pred)
```

---

### 5. Jupyter Lab

**Purpose**: Interactive development and analysis

**Features**:
- Access to all algorithms
- Shared notebooks
- Live data exploration
- Algorithm comparison
- Visualization tools

**Access**: http://localhost:8888 (token: `ml-suite-2024`)

---

### 6. Documentation Server

**Purpose**: Serve static documentation

**Content**:
- API documentation
- Architecture guides
- Tutorials
- Algorithm explanations

**Access**: http://localhost:8080

---

## Data Flow

### Training Flow

```
1. Client Request
   └─→ API Gateway
       └─→ Algorithm Service
           ├─→ Load Raw Data
           ├─→ Preprocess
           ├─→ Train Model (NumPy)
           ├─→ Calculate Metrics
           ├─→ Save Model
           └─→ Return Results

2. Results stored in:
   ├─→ models/ (serialized model)
   ├─→ results/ (metrics, plots)
   └─→ Response (JSON)
```

### Prediction Flow

```
1. Client Request (JSON)
   └─→ API Gateway
       └─→ Algorithm Service
           ├─→ Validate Input
           ├─→ Load Model
           ├─→ Transform Features
           ├─→ Predict (NumPy)
           ├─→ Format Response
           └─→ Return Predictions (JSON)
```

---

## Communication Patterns

### Synchronous (REST APIs)

```
Client → API Gateway → Service → Response
```

**Use cases**:
- Real-time predictions
- Model training (small datasets)
- Metrics retrieval

### Asynchronous (Future)

```
Client → API Gateway → Queue → Worker → Callback
```

**Use cases**:
- Large dataset training
- Batch predictions
- Long-running jobs

---

## Scalability

### Horizontal Scaling

Each service can scale independently:

```yaml
# docker-compose.yml
linear-regression-api:
  deploy:
    replicas: 3
  
pca-api:
  deploy:
    replicas: 2
```

### Load Balancing

Nginx handles distribution:

```nginx
upstream linear-regression {
    server linear-regression-api-1:8000;
    server linear-regression-api-2:8000;
    server linear-regression-api-3:8000;
}
```

---

## Security

### Current Implementation

1. **Network Isolation**: Services in private network
2. **Read-only Mounts**: Source code mounted as read-only
3. **No Root User**: Containers run as non-root
4. **Health Checks**: Continuous monitoring

### Future Enhancements

1. **Authentication**: JWT tokens
2. **Authorization**: Role-based access control
3. **Rate Limiting**: Per-user quotas
4. **Encryption**: TLS for all connections
5. **API Keys**: Service-to-service auth

---

## Monitoring & Observability

### Health Checks

All services expose `/health` endpoint:

```json
{
  "status": "healthy",
  "service": "linear-regression",
  "version": "1.0.0",
  "uptime": "2h 15m"
}
```

### Logging

Structured JSON logs:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "linear-regression",
  "message": "Prediction completed",
  "duration_ms": 45
}
```

### Metrics (Future)

- Request rate
- Response time
- Error rate
- Model performance
- Resource usage

---

## Deployment Strategies

### Development

```bash
make dev-setup
make up-all
```

- Hot reload enabled
- Debug logging
- Local volumes
- No optimization

### Staging

```bash
make build-all ENVIRONMENT=staging
make up-all
```

- Optimized builds
- Production-like config
- Testing data
- Monitoring enabled

### Production

```bash
make prod-build
make prod-up
```

- Multi-stage Docker builds
- Production data
- SSL/TLS enabled
- Full monitoring
- Auto-restart
- Resource limits

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API Gateway | Nginx | Reverse proxy, load balancing |
| APIs | FastAPI | REST endpoints |
| Core ML | NumPy | Algorithm implementation |
| Data | Pandas | Data manipulation |
| Viz | Matplotlib/Seaborn | Plotting |
| Dev | Jupyter Lab | Interactive analysis |
| Container | Docker | Isolation |
| Orchestration | Docker Compose | Multi-container |
| Automation | Make | Build automation |
| Testing | Pytest | Unit & integration |

---

## Design Principles

1. **Separation of Concerns**: Each service has single responsibility
2. **No External ML Libraries**: Core algorithms use only NumPy
3. **API-First**: All functionality accessible via REST
4. **Container-Native**: Designed for containerized deployment
5. **Observable**: Comprehensive logging and health checks
6. **Scalable**: Horizontal scaling capability
7. **Educational**: Code clarity over optimization
8. **Production-Ready**: Can be deployed commercially

---

## Future Architecture

### Planned Enhancements

1. **Message Queue**: RabbitMQ/Redis for async tasks
2. **Database**: PostgreSQL for metadata storage
3. **Caching**: Redis for frequent predictions
4. **Monitoring**: Prometheus + Grafana
5. **Tracing**: Jaeger for distributed tracing
6. **CI/CD**: GitHub Actions automation
7. **Kubernetes**: Production orchestration
8. **API Gateway**: Kong/Traefik for advanced features

---

## References

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Microservices Patterns](https://microservices.io/patterns/index.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Nginx Reverse Proxy Guide](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
