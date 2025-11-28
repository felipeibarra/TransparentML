#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Running All Tests - TransparentML${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

FAILED=0
PASSED=0

# Test Linear Regression
echo -e "${YELLOW}[1/2] Testing Linear Regression...${NC}"
if cd algorithms/linear-regression && make test 2>&1; then
    echo -e "${GREEN}  ✓ Linear Regression tests passed${NC}"
    ((PASSED++))
else
    echo -e "${RED}  ✗ Linear Regression tests failed${NC}"
    ((FAILED++))
fi
cd ../..

echo ""

# Test PCA
echo -e "${YELLOW}[2/2] Testing PCA Analysis...${NC}"
if cd algorithms/pca-analysis && make test 2>&1; then
    echo -e "${GREEN}  ✓ PCA Analysis tests passed${NC}"
    ((PASSED++))
else
    echo -e "${RED}  ✗ PCA Analysis tests failed${NC}"
    ((FAILED++))
fi
cd ../..

# Summary
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Test Summary${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "  Passed: ${GREEN}${PASSED}${NC}"
echo -e "  Failed: ${RED}${FAILED}${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi
