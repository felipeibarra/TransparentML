# 🚀 Quick Start Guide

Get TransparentML up and running in 5 minutes.

## Prerequisites

Before starting, ensure you have:

- ✅ Docker (version 20.10+)
- ✅ Docker Compose (version 2.0+)
- ✅ Make
- ✅ Python 3.11+ (for local development)
- ✅ Git

### Verify Prerequisites

```bash
docker --version
docker-compose --version
make --version
python3 --version
```

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/TransparentML.git
cd TransparentML
```

### 2. Run Complete Setup

```bash
make setup-all
```

This will:
- Check prerequisites
- Create directory structure
- Setup shared utilities
- Configure API Gateway
- Create Jupyter Dockerfile
- Initialize git repository

### 3. Build Docker Images

```bash
make build-all
```

Expected time: 5-10 minutes (first time)

### 4. Start All Services

```bash
make up-all
```

You should see:
```
✓ Services running:
  - API Gateway:        http://localhost
  - Linear Regression:  http://localhost:8001
  - PCA Analysis:       http://localhost:8002
  - Jupyter Lab:        http://localhost:8888
```

---

## Verify Installation

### Check Service Health

```bash
make health-check-all
```

Expected output:
```
✓ API Gateway         : Healthy
✓ Linear Regression   : Healthy
✓ PCA Analysis        : Healthy
✓ Jupyter Lab         : Healthy
✓ Documentation       : Healthy
```

### Run Quick Tests

```bash
make quick-test
```

---

## First API Calls

### Test Linear Regression

```bash
curl -X POST http://localhost:8001/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [[1,2,3,4,5]]}'
```

### Test PCA

```bash
curl -X POST http://localhost:8002/api/v1/transform \
  -H "Content-Type: application/json" \
  -d '{"data": [[5.1, 3.5, 1.4, 0.2]]}'
```

---

## Access Jupyter Lab

1. Open http://localhost:8888
2. Enter token: `ml-suite-2024`
3. Navigate to `examples/` folder
4. Open `quick-predictions.ipynb`

---

## Common Commands

```bash
# View all commands
make help

# Check status
make status

# View logs
make logs-all

# Stop all services
make down-all

# Restart services
make restart-all

# Run tests
make test-all
```

---

## Project Structure

```
TransparentML/
├── algorithms/           # Algorithm implementations
│   ├── linear-regression/
│   └── pca-analysis/
├── shared/              # Shared components
├── examples/            # Usage examples
├── docs/               # Documentation
└── scripts/            # Automation scripts
```

---

## Next Steps

1. **Explore Algorithms**:
   ```bash
   cd algorithms/linear-regression
   cat README.md
   ```

2. **Read Documentation**:
   - [Architecture](ARCHITECTURE.md)
   - [API Reference](API_REFERENCE.md)
   - [Contributing](CONTRIBUTING.md)

3. **Try Examples**:
   - Open Jupyter Lab
   - Run example notebooks

4. **Customize**:
   - Add your own datasets
   - Modify algorithms
   - Create new algorithms

---

## Troubleshooting

### Port Already in Use

```bash
# Stop all services
make down-all

# Or change ports in docker-compose.yml
```

### Build Errors

```bash
# Clean and rebuild
make clean-all
make build-all
```

### Service Not Starting

```bash
# Check logs
make logs-all

# Check Docker
docker ps -a
```

### Reset Everything

```bash
# Nuclear reset (careful!)
make reset-all
```

---

## Getting Help

- **Documentation**: Browse `docs/` folder
- **Issues**: https://github.com/yourusername/TransparentML/issues
- **Examples**: Check `examples/` folder
- **Commands**: Run `make help`

---

**🎉 You're all set! Start exploring TransparentML.**
