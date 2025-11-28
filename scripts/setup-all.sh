#!/bin/bash
set -e

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  TransparentML - Complete Setup${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}[1/8] Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Docker found: $(docker --version)${NC}"

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Docker Compose found: $(docker-compose --version)${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.11+ first.${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Python found: $(python3 --version)${NC}"

# Create necessary directories
echo -e "${YELLOW}[2/8] Creating directory structure...${NC}"
mkdir -p algorithms/linear-regression/{models,results}
mkdir -p algorithms/pca-analysis/{models,results}
mkdir -p shared/{common-utils,api-gateway,base-images,testing-framework}
mkdir -p examples
mkdir -p notebooks
mkdir -p docs
mkdir -p .backups
echo -e "${GREEN}  ✓ Directories created${NC}"

# Setup shared utilities
echo -e "${YELLOW}[3/8] Setting up shared utilities...${NC}"
if [ ! -f "shared/common-utils/__init__.py" ]; then
    touch shared/common-utils/__init__.py
fi
echo -e "${GREEN}  ✓ Shared utilities initialized${NC}"

# Setup API Gateway configuration
echo -e "${YELLOW}[4/8] Configuring API Gateway...${NC}"
if [ ! -f "shared/api-gateway/nginx.conf" ]; then
    cat > shared/api-gateway/nginx.conf <<'EOF'
events {
    worker_connections 1024;
}

http {
    upstream linear-regression {
        server linear-regression-api:8000;
    }

    upstream pca-analysis {
        server pca-api:8000;
    }

    server {
        listen 80;
        server_name localhost;

        # Health check endpoint
        location /health {
            access_log off;
            return 200 "OK\n";
            add_header Content-Type text/plain;
        }

        # Linear Regression API
        location /api/v1/linear-regression/ {
            proxy_pass http://linear-regression/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # PCA API
        location /api/v1/pca/ {
            proxy_pass http://pca-analysis/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Default route
        location / {
            return 200 "TransparentML API Gateway\n\nAvailable endpoints:\n- /api/v1/linear-regression/\n- /api/v1/pca/\n";
            add_header Content-Type text/plain;
        }
    }
}
EOF
    echo -e "${GREEN}  ✓ Nginx configuration created${NC}"
else
    echo -e "${GREEN}  ✓ Nginx configuration already exists${NC}"
fi

# Create base Jupyter Dockerfile
echo -e "${YELLOW}[5/8] Creating Jupyter Lab Dockerfile...${NC}"
if [ ! -f "shared/base-images/Dockerfile.jupyter" ]; then
    cat > shared/base-images/Dockerfile.jupyter <<'EOF'
FROM python:3.11-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir \
    jupyterlab \
    numpy \
    pandas \
    matplotlib \
    seaborn \
    scikit-learn \
    scipy \
    ipywidgets

# Expose Jupyter Lab port
EXPOSE 8888

# Start Jupyter Lab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
EOF
    echo -e "${GREEN}  ✓ Jupyter Dockerfile created${NC}"
else
    echo -e "${GREEN}  ✓ Jupyter Dockerfile already exists${NC}"
fi

# Create .gitignore
echo -e "${YELLOW}[6/8] Creating .gitignore...${NC}"
if [ ! -f ".gitignore" ]; then
    cat > .gitignore <<'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.pytest_cache/
.coverage
htmlcov/
*.egg-info/

# Jupyter
.ipynb_checkpoints
*.ipynb_checkpoints

# Docker
.dockerignore

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Results
algorithms/*/results/*
!algorithms/*/results/.gitkeep
algorithms/*/models/*
!algorithms/*/models/.gitkeep

# Data (keep raw, ignore processed)
algorithms/*/data/processed/
algorithms/*/data/cache/

# Backups
.backups/

# Logs
*.log
logs/
EOF
    echo -e "${GREEN}  ✓ .gitignore created${NC}"
else
    echo -e "${GREEN}  ✓ .gitignore already exists${NC}"
fi

# Create requirements.txt
echo -e "${YELLOW}[7/8] Creating requirements.txt...${NC}"
if [ ! -f "requirements.txt" ]; then
    cat > requirements.txt <<'EOF'
# Core ML libraries
numpy>=1.24.0
pandas>=2.0.0
scipy>=1.10.0

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0

# API
fastapi>=0.100.0
uvicorn>=0.23.0
pydantic>=2.0.0

# Utilities
python-dotenv>=1.0.0
pyyaml>=6.0
requests>=2.31.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-asyncio>=0.21.0

# Development
black>=23.0.0
flake8>=6.0.0
mypy>=1.4.0
pre-commit>=3.3.0
EOF
    echo -e "${GREEN}  ✓ requirements.txt created${NC}"
else
    echo -e "${GREEN}  ✓ requirements.txt already exists${NC}"
fi

# Initialize git repository
echo -e "${YELLOW}[8/8] Initializing git repository...${NC}"
if [ ! -d ".git" ]; then
    git init
    echo -e "${GREEN}  ✓ Git repository initialized${NC}"
else
    echo -e "${GREEN}  ✓ Git repository already exists${NC}"
fi

# Final message
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ Setup Complete!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Run: ${GREEN}make build-all${NC}"
echo -e "  2. Run: ${GREEN}make up-all${NC}"
echo -e "  3. Access services:"
echo -e "     - API Gateway:        ${BLUE}http://localhost${NC}"
echo -e "     - Linear Regression:  ${BLUE}http://localhost:8001${NC}"
echo -e "     - PCA Analysis:       ${BLUE}http://localhost:8002${NC}"
echo -e "     - Jupyter Lab:        ${BLUE}http://localhost:8888${NC} (token: ml-suite-2024)"
echo -e "     - Documentation:      ${BLUE}http://localhost:8080${NC}"
echo ""
echo -e "  Run ${GREEN}make help${NC} to see all available commands"
echo ""
