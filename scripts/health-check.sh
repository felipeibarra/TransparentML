#!/bin/bash

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Health Check - TransparentML${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

check_service() {
    local name=$1
    local url=$2
    
    if curl -s -f "$url" > /dev/null 2>&1; then
        echo -e "  ${name}: ${GREEN}✓ Healthy${NC}"
        return 0
    else
        echo -e "  ${name}: ${RED}✗ Unhealthy${NC}"
        return 1
    fi
}

HEALTHY=0
UNHEALTHY=0

# Check API Gateway
if check_service "API Gateway         " "http://localhost/health"; then
    ((HEALTHY++))
else
    ((UNHEALTHY++))
fi

# Check Linear Regression
if check_service "Linear Regression   " "http://localhost:8001/health"; then
    ((HEALTHY++))
else
    ((UNHEALTHY++))
fi

# Check PCA
if check_service "PCA Analysis        " "http://localhost:8002/health"; then
    ((HEALTHY++))
else
    ((UNHEALTHY++))
fi

# Check Jupyter
if check_service "Jupyter Lab         " "http://localhost:8888"; then
    ((HEALTHY++))
else
    ((UNHEALTHY++))
fi

# Check Docs
if check_service "Documentation       " "http://localhost:8080"; then
    ((HEALTHY++))
else
    ((UNHEALTHY++))
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "  Healthy:   ${GREEN}${HEALTHY}${NC}"
echo -e "  Unhealthy: ${RED}${UNHEALTHY}${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"

if [ $UNHEALTHY -eq 0 ]; then
    echo -e "${GREEN}✅ All services are healthy${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some services are unhealthy${NC}"
    exit 1
fi
