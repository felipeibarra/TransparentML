#!/bin/bash

# Script de verificación de la configuración Docker
# Tarea 1 - Regresión Lineal

# No detener en errores - queremos ver todos los checks
set +e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "════════════════════════════════════════════════════════"
echo "   VERIFICACIÓN DE CONFIGURACIÓN - TAREA 1 ML"
echo "════════════════════════════════════════════════════════"
echo -e "${NC}\n"

# Contador de checks
TOTAL_CHECKS=0
PASSED_CHECKS=0

check() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if eval "$1" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $2"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        echo -e "${RED}✗${NC} $2"
        if [ ! -z "$3" ]; then
            echo -e "  ${YELLOW}→ $3${NC}"
        fi
        return 1
    fi
}

# 1. Verificar Docker
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}1. Prerequisitos${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

check "command -v docker" "Docker instalado" "Instala Docker desde https://docker.com"
check "command -v docker-compose" "Docker Compose instalado" "Instala Docker Compose"
check "docker ps" "Docker daemon corriendo" "Inicia Docker Desktop o el daemon"

# 2. Verificar archivos de configuración
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}2. Archivos de Configuración${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

check "test -f docker-compose.yml" "docker-compose.yml existe"
check "test -f Dockerfile" "Dockerfile existe"
check "test -f Dockerfile.api" "Dockerfile.api existe"
check "test -f Dockerfile.training" "Dockerfile.training existe"
check "test -f Dockerfile.jupyter" "Dockerfile.jupyter existe"
check "test -f requirements.txt" "requirements.txt existe"
check "test -f nginx/nginx.conf" "nginx.conf existe"

# 3. Verificar scripts
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}3. Scripts${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

check "test -f docker-start.sh" "docker-start.sh existe"
check "test -x docker-start.sh" "docker-start.sh es ejecutable" "Ejecuta: chmod +x docker-start.sh"
check "test -f scripts/api/main.py" "API main.py existe"

# 4. Verificar directorios
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}4. Estructura de Directorios${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

check "test -d data" "Directorio data/ existe"
check "test -d results" "Directorio results/ existe"
check "test -d scripts" "Directorio scripts/ existe"
check "test -d src" "Directorio src/ existe"
check "test -d nginx" "Directorio nginx/ existe"

# Crear directorio models si no existe
if [ ! -d "models" ]; then
    mkdir -p models
    echo -e "${YELLOW}ℹ${NC} Directorio models/ creado"
fi
check "test -d models" "Directorio models/ existe"

# 5. Validar docker-compose.yml
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}5. Validación de Configuración${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

check "docker-compose config > /dev/null" "docker-compose.yml es válido"

# 6. Verificar documentación
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}6. Documentación${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

check "test -f README_DOCKER.md" "README_DOCKER.md existe"
check "test -f DOCKER_GUIDE.md" "DOCKER_GUIDE.md existe"
check "test -f API_EXAMPLES.md" "API_EXAMPLES.md existe"
check "test -f RESUMEN_SOLUCION.md" "RESUMEN_SOLUCION.md existe"

# Resumen
echo -e "\n${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}Resumen${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}\n"

PERCENTAGE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))

if [ $PASSED_CHECKS -eq $TOTAL_CHECKS ]; then
    echo -e "${GREEN}🎉 ¡Perfecto! Todos los checks pasaron (${PASSED_CHECKS}/${TOTAL_CHECKS})${NC}\n"
    
    echo -e "${GREEN}✅ Tu proyecto está listo para usar con Docker${NC}\n"
    
    echo -e "${YELLOW}📝 Próximos pasos:${NC}"
    echo -e "   1. Ejecuta: ${BLUE}./docker-start.sh${NC}"
    echo -e "   2. Selecciona opción ${BLUE}1${NC} para construir e iniciar servicios"
    echo -e "   3. Accede a:"
    echo -e "      • API Docs: ${BLUE}http://localhost:8000/docs${NC}"
    echo -e "      • JupyterLab: ${BLUE}http://localhost:8888${NC}"
    echo -e "      • Nginx Gateway: ${BLUE}http://localhost${NC}"
    echo ""
    echo -e "${YELLOW}📚 Lee la documentación en:${NC}"
    echo -e "   • ${BLUE}README_DOCKER.md${NC} - Inicio rápido"
    echo -e "   • ${BLUE}DOCKER_GUIDE.md${NC} - Guía completa"
    echo -e "   • ${BLUE}API_EXAMPLES.md${NC} - Ejemplos de API"
    echo ""
    
elif [ $PERCENTAGE -ge 80 ]; then
    echo -e "${YELLOW}⚠ Casi listo: ${PASSED_CHECKS}/${TOTAL_CHECKS} checks pasaron (${PERCENTAGE}%)${NC}\n"
    echo -e "Revisa los checks fallidos arriba y corrígelos.\n"
    
else
    echo -e "${RED}❌ Hay problemas: Solo ${PASSED_CHECKS}/${TOTAL_CHECKS} checks pasaron (${PERCENTAGE}%)${NC}\n"
    echo -e "Revisa los checks fallidos arriba y corrígelos.\n"
    exit 1
fi

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}\n"
