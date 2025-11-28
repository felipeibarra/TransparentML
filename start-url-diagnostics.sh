#!/bin/bash

# ============================================
# TransparentML URL Diagnostics Startup
# ============================================

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  🚀 TransparentML URL Diagnostics${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Docker is not running${NC}"
    echo -e "${YELLOW}Please start Docker Desktop and try again${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker is running${NC}"
echo ""

# Create network if it doesn't exist
echo -e "${YELLOW}[1/5] Creating Docker network...${NC}"
docker network create transparentml-network 2>/dev/null || echo "Network already exists"

# Navigate to url-diagnostics directory
cd "$(dirname "$0")/url-diagnostics" || exit

# Check if Dockerfile exists
if [ ! -f "Dockerfile" ]; then
    echo -e "${RED}❌ Error: Dockerfile not found${NC}"
    echo -e "${YELLOW}Please run this script from the TransparentML root directory${NC}"
    exit 1
fi

# Build the image
echo -e "${YELLOW}[2/5] Building Docker image...${NC}"
docker-compose build

# Stop any existing container
echo -e "${YELLOW}[3/5] Stopping existing container...${NC}"
docker-compose down 2>/dev/null

# Start the service
echo -e "${YELLOW}[4/5] Starting URL Diagnostics service...${NC}"
docker-compose up -d

# Wait for service to be ready
echo -e "${YELLOW}[5/5] Waiting for service to be ready...${NC}"
sleep 5

# Health check
for i in {1..10}; do
    if curl -s http://localhost:8003/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Service is healthy!${NC}"
        break
    fi
    if [ $i -eq 10 ]; then
        echo -e "${RED}⚠️  Service might not be ready yet${NC}"
    else
        sleep 2
    fi
done

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  📊 SERVICE INFORMATION${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}🌐 Web Interface:${NC}"
echo -e "   ${GREEN}http://localhost:8003/static/index.html${NC}"
echo ""
echo -e "${YELLOW}📚 API Documentation:${NC}"
echo -e "   http://localhost:8003/docs"
echo ""
echo -e "${YELLOW}🏥 Health Check:${NC}"
echo -e "   http://localhost:8003/health"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  🎯 QUICK START${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "1. Open your browser and visit:"
echo -e "   ${GREEN}http://localhost:8003/static/index.html${NC}"
echo ""
echo "2. Enter a URL to analyze (e.g., https://www.google.com)"
echo ""
echo "3. Click 'Analyze URL' and watch the magic happen! ✨"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}  💡 USEFUL COMMANDS${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${YELLOW}View logs:${NC}          docker-compose -f url-diagnostics/docker-compose.yml logs -f"
echo -e "  ${YELLOW}Stop service:${NC}       docker-compose -f url-diagnostics/docker-compose.yml down"
echo -e "  ${YELLOW}Restart service:${NC}    ./start-url-diagnostics.sh"
echo ""
echo -e "${GREEN}🎉 Ready to analyze URLs! Open your browser now!${NC}"
echo ""

# Optionally open browser (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${YELLOW}Opening browser in 3 seconds...${NC}"
    sleep 3
    open "http://localhost:8003/static/index.html" 2>/dev/null
fi
