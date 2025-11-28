#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Performance Benchmarks - TransparentML${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}Running benchmarks for all algorithms...${NC}"
echo ""

# Linear Regression Benchmark
echo -e "${BLUE}Linear Regression:${NC}"
curl -s -w "\nTime: %{time_total}s\n" \
  -X POST http://localhost:8001/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [[1,2,3,4,5]]}' 2>/dev/null || echo "Service not available"

echo ""

# PCA Benchmark
echo -e "${BLUE}PCA Analysis:${NC}"
curl -s -w "\nTime: %{time_total}s\n" \
  -X POST http://localhost:8002/api/v1/transform \
  -H "Content-Type: application/json" \
  -d '{"data": [[5.1, 3.5, 1.4, 0.2]]}' 2>/dev/null || echo "Service not available"

echo ""
echo -e "${GREEN}✅ Benchmark complete${NC}"
