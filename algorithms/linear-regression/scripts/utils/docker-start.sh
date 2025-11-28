#!/bin/bash

# Script para iniciar arquitectura de microservicios Docker
# Tarea 1 - Regresión Lineal

set -e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "════════════════════════════════════════════════════════"
echo "   INICIO DE SERVICIOS DOCKER - TAREA 1 ML"
echo "════════════════════════════════════════════════════════"
echo -e "${NC}"

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose no está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker y Docker Compose detectados${NC}\n"

# Crear directorio de modelos si no existe
mkdir -p models

# Opciones
echo -e "${BLUE}Selecciona una opción:${NC}"
echo "1) Construir y levantar todos los servicios"
echo "2) Solo levantar servicios (sin rebuild)"
echo "3) Levantar servicios sin Nginx gateway"
echo "4) Solo API de predicción"
echo "5) Solo JupyterLab"
echo "6) Parar todos los servicios"
echo "7) Reiniciar todos los servicios"
echo "8) Ver logs de servicios"
echo "9) Ver estado de servicios"

read -p "Opción [1-9]: " option

case $option in
    1)
        echo -e "\n${YELLOW}📦 Construyendo imágenes...${NC}"
        docker-compose build
        
        echo -e "\n${YELLOW}🚀 Iniciando servicios...${NC}"
        docker-compose up -d
        
        echo -e "\n${GREEN}✅ Servicios iniciados correctamente${NC}"
        ;;
    
    2)
        echo -e "\n${YELLOW}🚀 Iniciando servicios...${NC}"
        docker-compose up -d
        
        echo -e "\n${GREEN}✅ Servicios iniciados${NC}"
        ;;
    
    3)
        echo -e "\n${YELLOW}🚀 Iniciando servicios sin Nginx...${NC}"
        docker-compose up -d prediction-api training-service jupyter-lab
        
        echo -e "\n${GREEN}✅ Servicios iniciados${NC}"
        ;;
    
    4)
        echo -e "\n${YELLOW}🚀 Iniciando API de predicción...${NC}"
        docker-compose up -d prediction-api training-service
        
        echo -e "\n${GREEN}✅ API iniciada${NC}"
        ;;
    
    5)
        echo -e "\n${YELLOW}🚀 Iniciando JupyterLab...${NC}"
        docker-compose up -d jupyter-lab
        
        echo -e "\n${GREEN}✅ JupyterLab iniciado${NC}"
        ;;
    
    6)
        echo -e "\n${YELLOW}🛑 Deteniendo servicios...${NC}"
        docker-compose down
        
        echo -e "\n${GREEN}✅ Servicios detenidos${NC}"
        ;;
    
    7)
        echo -e "\n${YELLOW}🔄 Reiniciando servicios...${NC}"
        docker-compose restart
        
        echo -e "\n${GREEN}✅ Servicios reiniciados${NC}"
        ;;
    
    8)
        echo -e "\n${BLUE}📋 Logs de servicios (Ctrl+C para salir):${NC}\n"
        docker-compose logs -f
        ;;
    
    9)
        echo -e "\n${BLUE}📊 Estado de servicios:${NC}\n"
        docker-compose ps
        ;;
    
    *)
        echo -e "${RED}❌ Opción inválida${NC}"
        exit 1
        ;;
esac

# Mostrar información de acceso si se iniciaron servicios
if [ $option -le 5 ]; then
    sleep 3
    
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}📍 URLs de acceso:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    if docker-compose ps | grep -q "prediction-api"; then
        echo -e "\n${GREEN}🔮 API de Predicción:${NC}"
        echo "   → http://localhost:8000"
        echo "   → http://localhost:8000/docs (Swagger UI)"
        echo "   → http://localhost:8000/health (Health check)"
    fi
    
    if docker-compose ps | grep -q "jupyter-lab"; then
        echo -e "\n${GREEN}📓 JupyterLab:${NC}"
        echo "   → http://localhost:8888"
    fi
    
    if docker-compose ps | grep -q "nginx-gateway"; then
        echo -e "\n${GREEN}🌐 Nginx Gateway:${NC}"
        echo "   → http://localhost (redirect a API docs)"
        echo "   → http://localhost/api/ (API a través de gateway)"
        echo "   → http://localhost/jupyter/ (Jupyter a través de gateway)"
    fi
    
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}💡 Comandos útiles:${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "# Ver logs en tiempo real"
    echo "docker-compose logs -f"
    echo ""
    echo "# Ejecutar entrenamiento"
    echo "docker-compose exec training-service python scripts/train.py"
    echo ""
    echo "# Acceder a shell del servicio"
    echo "docker-compose exec prediction-api bash"
    echo ""
    echo "# Parar servicios"
    echo "docker-compose down"
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    echo -e "\n${GREEN}✨ Para más información consulta: DOCKER_GUIDE.md${NC}\n"
fi
